import time, json, datetime as dt, threading, queue, sys, csv
from pathlib import Path
import cv2
from PIL import Image, ImageTk
import tkinter as tk
import tkinter.font as tkFont
import serial
import numpy as np

# Constantes
SERIAL_PORT = "COM3"
BAUDRATE    = 9600
CAM_URL     = "http://192.168.0.128:8080/video"  # IP Webcam

DISPLAY_W, DISPLAY_H = 400, 300
INFO_W               = 320

BG_MAIN, BG_PANEL = "#181818", "#181818"
ACCENT, COLOR_TXT = "#3dbc95", "#ffffff"

FRAME_QUEUE_MAX = 5
VISION_FPS      = 0.07          # ~14 fps

# Párametros de tiempo
WAIT_CAJA   = 12 
WAIT_ROT    =  8   
WAIT_ROT4   = 20   
SEARCH_WINDOW = 3               # segundos de búsqueda del QR

# Comandos de rotación
ROTACIONES = ["ROTACION_1", "ROTACION_2", "ROTACION_3", "ROTACION_4"]

# ─── Evento que enciende/apaga la decodificación ────────────────────────────
vision_active = threading.Event()

# ──────── SERIAL ─────────────────────────────────────────────────────────────
try:
    arduino = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=2)
    time.sleep(2)
    print(f">>> Conectado a Arduino en {SERIAL_PORT}")
except serial.SerialException as e:
    print(">>> ERROR: no se abrió", SERIAL_PORT, e)
    arduino = None

def send_cmd(cmd: str):
    if not arduino:
        print(f">>> Arduino no conectado (ignorado {cmd})"); return
    arduino.write(cmd.encode() + b"\n")
    arduino.flush()
    print(">>> →", cmd)

# Inventario CSV

INV_PATH = Path(__file__).parent.parent / "Data" / "inventario.csv"
inventario = {}
with open(INV_PATH, newline='', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        inventario[str(row["ID"])] = row
print(f">>> Inventario cargado ({len(inventario)} ítems)")

# Detectar el QR
qr_det = cv2.QRCodeDetector().setEpsX(0.4).setEpsY(0.4)

def try_decode_qr(frame):
    """Devuelve (info_dict, bbox) o (None, None)."""
    try:
        data, pts, _ = qr_det.detectAndDecode(frame)
        if not data and hasattr(qr_det, "detectAndDecodeCurved"):
            try:
                data, pts, _ = qr_det.detectAndDecodeCurved(frame)
            except cv2.error:
                return None, None
        if not data:
            return None, None

        # Interpretar payload
        try:
            parsed = json.loads(data)
            if isinstance(parsed, dict):
                if "ID" in parsed:
                    id_val = str(parsed["ID"])
                else:
                    return parsed, pts         # venían 5 campos completos
            else:
                id_val = str(parsed)           # JSON numérico
        except json.JSONDecodeError:
            id_val = data.strip()              # solo ID como texto

        info = inventario.get(id_val)
        return (info, pts) if info else (None, None)
    except Exception as e:
        print(">>> Error en try_decode_qr:", e)
        return None, None

# Colas
frames_q  = queue.Queue(maxsize=FRAME_QUEUE_MAX)
results_q = queue.Queue()
stop_all  = threading.Event()
fsm_idle  = threading.Event(); fsm_idle.set()


# 1. HILO VISIÓN

def vision_worker():
    while not stop_all.is_set():
        try:
            frame = frames_q.get(timeout=0.1)
        except queue.Empty:
            continue

        if vision_active.is_set():
            info, pts = try_decode_qr(frame)
            if info:
                results_q.put((info, pts))

        time.sleep(VISION_FPS if vision_active.is_set() else 0.02)
threading.Thread(target=vision_worker, daemon=True).start()

# 2. HILO FSM

def fsm_worker():
    fsm_worker.state, fsm_worker.deadline = "IDLE", 0
    fsm_worker.search_dl, fsm_worker.rot_index = 0, 0  # rot_index 0‑4

    while not stop_all.is_set():
        now, st = time.monotonic(), fsm_worker.state

        # Fin de espera mecánica (CAJA o ROTACIÓN_i)
        if st in ("CAJA_WAIT", "ROT_WAIT") and now >= fsm_worker.deadline:
            fsm_worker.state = "BUSCANDO"
            vision_active.set()
            fsm_worker.search_dl = now + SEARCH_WINDOW
            print(f">>> {st} terminado → buscando QR durante {SEARCH_WINDOW}s")

        # Resultado visión
        try:
            info, pts = results_q.get_nowait()
        except queue.Empty:
            info = None

        if info:
            vision_active.clear()
            gui_set_labels(info)
            global qr_bbox, qr_info
            qr_bbox, qr_info = pts, info

            fecha_txt = info.get("Fecha", "")
            try:
                fecha_qr = dt.datetime.strptime(fecha_txt, "%Y-%m-%d").date()
            except ValueError:
                print(">>> Fecha inválida → VENCIDO")
                send_cmd("VENCIDO"); send_cmd("HOME")
                fsm_worker.state = "IDLE"; fsm_idle.set(); continue

            send_cmd("NO_VENCIDO" if fecha_qr > dt.date.today() else "VENCIDO")
            send_cmd("HOME"); fsm_worker.state = "IDLE"; fsm_idle.set(); continue

        # Ventana de búsqueda agotada
        if st == "BUSCANDO" and now >= fsm_worker.search_dl:
            vision_active.clear()

            if fsm_worker.rot_index < len(ROTACIONES):
                cmd = ROTACIONES[fsm_worker.rot_index]
                fsm_worker.rot_index += 1
                print(f">>> No QR → {cmd}"); send_cmd(cmd)

                wait = WAIT_ROT4 if cmd == "ROTACION_4" else WAIT_ROT
                fsm_worker.state, fsm_worker.deadline = "ROT_WAIT", now + wait
            else:
                print(">>> No QR tras 4 rotaciones → HOME")
                send_cmd("HOME"); fsm_worker.state = "IDLE"; fsm_idle.set()

        time.sleep(0.05)
threading.Thread(target=fsm_worker, daemon=True).start()

# 3. GUI - Sistema Completo

root = tk.Tk()
root.title("Control Brazo QR (debug)")
root.configure(bg=BG_MAIN)
root.geometry("930x520"); root.minsize(850,480)
root.columnconfigure(0, weight=1, minsize=INFO_W+40)
root.columnconfigure(1, weight=3); root.rowconfigure(0, weight=1)

panel = tk.Frame(root, bg=BG_MAIN)
panel.grid(row=0, column=0, sticky="nsew", padx=40, pady=40)
panel.rowconfigure((0,3), weight=1); panel.columnconfigure(0, weight=1)

info_frame = tk.Frame(panel, width=INFO_W, bg=BG_PANEL,
                      highlightbackground="#fff", highlightthickness=2)
info_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=10)
info_frame.columnconfigure(0, weight=1)

tk.Label(info_frame, text="INFORMACIÓN OBTENIDA", bg=BG_PANEL, fg=ACCENT,
         font=("Segoe UI",12,"bold"), anchor="w").pack(padx=(10,0), pady=(8,10))

raw_lbl = {"ID":"ID:\t\t","Nombre":"Nombre:\t\t","Categoria":"Categoría:\t",
           "Destino":"Destino:\t\t","Fecha":"Fecha:\t\t"}
labels = {k: tk.Label(info_frame, text=v, font=("Roboto",10),
                      bg=BG_PANEL, fg=COLOR_TXT, anchor="w")
          for k,v in raw_lbl.items()}
for lbl in labels.values(): lbl.pack(fill="x", padx=10, pady=(2,4))

def gui_set_labels(data):
    for k,lbl in labels.items():
        lbl.config(text=f"{raw_lbl[k]}{data.get(k,'')}")

frame_btns = tk.Frame(panel, bg=BG_MAIN)
frame_btns.grid(row=2, column=0, pady=(30,0))
frame_btns.columnconfigure((0,1), weight=1)
btn_font = tkFont.Font(family="Segoe UI", size=11, weight="bold")

frame_cam = tk.Frame(root, width=DISPLAY_W, height=DISPLAY_H,
                     bg=BG_PANEL, highlightbackground="#fff", highlightthickness=2)
frame_cam.grid(row=0, column=1, padx=40, pady=40); frame_cam.grid_propagate(False)
lbl_cam = tk.Label(frame_cam, bg=BG_PANEL, bd=0); lbl_cam.pack(fill='both', expand=True)

cap = cv2.VideoCapture(1)
if not cap.isOpened():
    print(">>> ERROR: no se pudo abrir la cámara", CAM_URL); sys.exit(1)

qr_bbox, qr_info = None, None

def update_camera():
    ret, frame = cap.read()
    if ret:
        if not frames_q.full(): frames_q.put(frame.copy())
        prev = cv2.resize(frame, (DISPLAY_W, DISPLAY_H))
        prev_rgb = cv2.cvtColor(prev, cv2.COLOR_BGR2RGB)

        if qr_bbox is not None and isinstance(qr_bbox, np.ndarray) and qr_bbox.shape[0]>=4:
            sx, sy = DISPLAY_W/frame.shape[1], DISPLAY_H/frame.shape[0]
            pts = qr_bbox.copy(); pts[:,0]*=sx; pts[:,1]*=sy; pts=pts.astype(int)
            cv2.polylines(prev_rgb, [pts.reshape(-1,1,2)], True, (0,255,0), 2)

        img = ImageTk.PhotoImage(Image.fromarray(prev_rgb))
        lbl_cam.imgtk = img; lbl_cam.config(image=img)
        if qr_info: gui_set_labels(qr_info)

    if not stop_all.is_set(): lbl_cam.after(20, update_camera)

def task_iniciar():
    if not fsm_idle.is_set():
        print(">>> Ya hay una operación en curso"); return
    global qr_bbox, qr_info
    qr_bbox = qr_info = None; gui_set_labels({k:"" for k in raw_lbl})

    send_cmd("CAJA"); fsm_idle.clear()
    now = time.monotonic()
    fsm_worker.state, fsm_worker.deadline = "CAJA_WAIT", now + WAIT_CAJA
    fsm_worker.rot_index = 0; vision_active.clear()

def task_stop():
    stop_all.set(); send_cmd("HOME"); root.destroy()

tk.Button(frame_btns, text="INICIAR", font=btn_font, bg=ACCENT, fg="white",
          padx=20, pady=10, bd=0, activebackground="#246f58",
          command=task_iniciar).grid(row=0,column=0,sticky="e",padx=(0,20))
tk.Button(frame_btns, text="STOP", font=btn_font, bg="#f53b4b", fg="white",
          padx=20, pady=10, bd=0, activebackground="#a82833",
          command=task_stop).grid(row=0,column=1,sticky="w",padx=(20,0))

# Ejecutar
update_camera()
root.mainloop()
