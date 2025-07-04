# control_brazo_qr_gui.py
# ─────────────────────────────────────────────────────────────────────────────
# Versión depuración — Julio 2025
#
# Flujo resumido
# ──────────────
# 1. INICIAR  →  "CAJA"            (⏱ 30 s)
# 2. Busca QR
#    ├─ ✓ Encontrado → lee fecha
#    │                • fecha > hoy   → "NO_VENCIDO", "HOME"
#    │                • fecha ≤ hoy   → "VENCIDO",     "HOME"
#    └─ ✗ No QR  (2 intentos) → "SUBIR"  (⏱ 45 s) … repite búsqueda
#          ├─ ✓ Encontrado → (mismo test de fecha) + "HOME"
#          └─ ✗ No QR  (2 intentos) → "HOME" y termina
#
# 3. STOP → corta todo y envía "HOME".
#
# Todos los prints de depuración empiezan con >>>.

import serial, time, json, datetime as dt
import serial.tools.list_ports as list_ports
import threading
import cv2
from PIL import Image, ImageTk
import tkinter as tk
import tkinter.font as tkFont

# ────── SERIAL ───────────────────────────────────────────────────────────────
def connect_arduino(baud=9600, handshake=b"READY", timeout=2):
    for port in list_ports.comports():
        try:
            ser = serial.Serial(port.device, baudrate=baud, timeout=timeout)
            time.sleep(2)
            line = ser.readline().strip()
            print(f">>> Escuchando {port.device} → {line}")
            if line == handshake:
                print(f">>> Arduino OK  →  {port.device}")
                return ser
            ser.close()
        except (OSError, serial.SerialException):
            pass
    print(">>> Arduino NO encontrado")
    return None

arduino = connect_arduino()

def send_cmd(cmd: str):
    """Envía un comando al Arduino y lo muestra por consola."""
    if not arduino:
        print(f">>> Arduino no conectado (no se envió {cmd})")
        return
    arduino.write(cmd.encode() + b'\n')
    arduino.flush()
    print(f">>> {cmd} enviado al Arduino")

# ───── OPEN-CV QR DETECTOR ───────────────────────────────────────────────────
qr_detector = cv2.QRCodeDetector()
def decode_qr(frame):
    data, pts, _ = qr_detector.detectAndDecode(frame)
    if not data:
        return None, None
    try:
        return json.loads(data), pts
    except json.JSONDecodeError:
        return None, None

# ───── CONFIG VISUAL ─────
BG_MAIN, BG_PANEL = "#181818", "#181818"
ACCENT, COLOR_TXT = "#3dbc95", "#ffffff"
DISPLAY_W, DISPLAY_H = 400, 300
INFO_W             = 320
CAM_URL = "http://10.1.19.196:8080/video"

root = tk.Tk()
root.title("Control Brazo QR (debug)")
root.configure(bg=BG_MAIN)
root.geometry("930x520")
root.minsize(850, 480)
root.columnconfigure(0, weight=1, minsize=INFO_W + 40)
root.columnconfigure(1, weight=3)
root.rowconfigure(0, weight=1)

# ───── PANEL IZQ ─────
panel = tk.Frame(root, bg=BG_MAIN)
panel.grid(row=0, column=0, sticky="nsew", padx=40, pady=40)
panel.rowconfigure((0, 3), weight=1)
panel.columnconfigure(0, weight=1)

info_frame = tk.Frame(panel, width=INFO_W, bg=BG_PANEL,
                      highlightbackground="#ffffff", highlightthickness=2)
info_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=10)
info_frame.columnconfigure(0, weight=1)

tk.Label(info_frame, text="INFORMACIÓN OBTENIDA", bg=BG_PANEL, fg=ACCENT,
         font=("Segoe UI", 12, "bold"), anchor="w").pack(padx=(10, 0), pady=(8, 10))

raw = {"ID":"ID:\t\t","Nombre":"Nombre:\t\t","Categoria":"Categoría:\t",
       "Destino":"Destino:\t\t","Fecha":"Fecha:\t\t"}
labels = {k: tk.Label(info_frame, text=v, font=("Roboto", 10),
                      bg=BG_PANEL, fg=COLOR_TXT, anchor="w")
          for k, v in raw.items()}
for lbl in labels.values():
    lbl.pack(fill="x", padx=10, pady=(2, 4))

def set_labels(data):
    for k,lbl in labels.items():
        lbl.config(text=f"{raw[k]}{data.get(k,'')}")

# ───── BOTONES Y CÁMARA ─────
frame_btns = tk.Frame(panel, bg=BG_MAIN)
frame_btns.grid(row=2, column=0, pady=(30, 0))
frame_btns.columnconfigure((0,1), weight=1)
btn_font = tkFont.Font(family="Segoe UI", size=11, weight="bold")

frame_cam = tk.Frame(root, width=DISPLAY_W, height=DISPLAY_H,
                     bg=BG_PANEL, highlightbackground="#ffffff",
                     highlightthickness=2)
frame_cam.grid(row=0, column=1, padx=40, pady=40)
frame_cam.grid_propagate(False)
lbl_cam = tk.Label(frame_cam, bg=BG_PANEL, bd=0)
lbl_cam.pack(fill='both', expand=True)

cap = cv2.VideoCapture(CAM_URL)
if not cap.isOpened():
    print(">>> ERROR: No se pudo abrir la cámara en", CAM_URL)

last_frame = None
qr_bbox    = None
scanning   = False

# ───── LOOP DE VÍDEO ─────
def update_camera():
    global last_frame
    ret, frame = cap.read()
    if ret:
        frame_r = cv2.resize(frame, (DISPLAY_W, DISPLAY_H))
        last_frame = frame_r.copy()
        frame_rgb = cv2.cvtColor(frame_r, cv2.COLOR_BGR2RGB)
        if qr_bbox is not None:
            import numpy as np
            pts = qr_bbox.astype(int).reshape(-1,1,2)
            cv2.polylines(frame_rgb, [pts], True, (0,255,0), 2)
        img = ImageTk.PhotoImage(Image.fromarray(frame_rgb))
        lbl_cam.imgtk = img
        lbl_cam.config(image=img)
    lbl_cam.after(20, update_camera)

# ───── LÓGICA DE BÚSQUEDA DE QR ─────
def evaluate_qr(info):
    """Procesa la fecha y envía el comando apropiado."""
    fecha_txt = info.get("Fecha","")
    try:
        fecha_qr = dt.datetime.strptime(fecha_txt, "%Y-%m-%d").date()
    except ValueError:
        print(">>> Formato de fecha inválido:", fecha_txt)
        send_cmd("VENCIDO")          # cuidador: tratar como vencido
        send_cmd("HOME")
        return
    hoy = dt.date.today()
    if fecha_qr > hoy:
        print(">>> Producto NO vencido (", fecha_txt, ")")
        send_cmd("NO_VENCIDO")
    else:
        print(">>> Producto VENCIDO (", fecha_txt, ")")
        send_cmd("VENCIDO")
    send_cmd("HOME")

def search_qr_loop(stage=0, attempt=0):
    """
    stage 0 → después de CAJA
    stage 1 → después de SUBIR
    attempt 0/1 → primer intento / reintento tras 4 s
    """
    global scanning, qr_bbox, last_frame
    if not scanning:
        return
    if last_frame is None:
        root.after(100, lambda: search_qr_loop(stage, attempt))
        return

    info, pts = decode_qr(last_frame)
    if info:
        qr_bbox = pts
        set_labels(info)
        scanning = False
        print(">>> QR ENCONTRADO ✅  Información:", info)
        evaluate_qr(info)
        return

    print(">>> QR no encontrado (stage", stage, "attempt", attempt, ")")
    if attempt == 0:
        root.after(4000, lambda: search_qr_loop(stage, 1))
        return

    # falló el segundo intento
    if stage == 0:
        # --- pasar a SUBIR ---
        print(">>> Dos intentos fallidos → ejecutando SUBIR")
        def subir_worker():
            send_cmd("SUBIR")
            print(">>> Esperando 45 s tras SUBIR …")
            time.sleep(45)
            root.after(0, lambda: search_qr_loop(1, 0))
        threading.Thread(target=subir_worker, daemon=True).start()
    else:
        # stage 1 y también falló → HOME y terminar
        print(">>> No se detectó QR tras SUBIR → HOME y fin")
        send_cmd("HOME")
        scanning = False

# ───── ACCIONES BOTONES ─────
def task_iniciar():
    """Envía CAJA, espera 30 s y lanza la búsqueda de QR (stage 0)."""
    global scanning, qr_bbox
    scanning = True
    qr_bbox  = None
    set_labels({k:"" for k in labels})

    def worker():
        send_cmd("CAJA")
        print(">>> Esperando 30 s tras CAJA …")
        time.sleep(30)
        print(">>> Iniciando búsqueda de QR (stage 0)")
        root.after(0, lambda: search_qr_loop(0, 0))
    threading.Thread(target=worker, daemon=True).start()

def task_stop():
    """Detiene todo y lleva el brazo a HOME."""
    global scanning, qr_bbox
    scanning = False
    qr_bbox  = None
    send_cmd("HOME")
    set_labels({k:"" for k in labels})

# ───── BOTONES ─────
tk.Button(frame_btns, text="INICIAR", font=btn_font, bg=ACCENT, fg="white",
          padx=20, pady=10, bd=0, activebackground="#246f58", cursor="hand2",
          command=task_iniciar).grid(row=0, column=0, sticky="e", padx=(0,20))
tk.Button(frame_btns, text="STOP", font=btn_font, bg="#f53b4b", fg="white",
          padx=20, pady=10, bd=0, activebackground="#a82833", cursor="hand2",
          command=task_stop).grid(row=0, column=1, sticky="w", padx=(20,0))

# ───── MAINLOOP ─────
update_camera()
root.mainloop()
