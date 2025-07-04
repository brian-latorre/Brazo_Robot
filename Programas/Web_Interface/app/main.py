from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from pathlib import Path
from app.serial_controller import SerialController

app = FastAPI(title="Robotic‑Arm API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

serial_link = SerialController()

@app.get("/")
async def index(request: Request, ack: str = "", color: str = ""):
    return templates.TemplateResponse("index.html", {"request": request, "ack": ack, "color": color})


@app.post("/send")
async def send_command(request: Request, command: str = Form(...)):
    ack = serial_link.send(command.strip())

    # Determinar el color basado en el mensaje
    if ack.startswith(("OK", "ACK", "Listo")):
        color = "limegreen"
    elif ack.startswith(("ERR", "ERROR")):
        color = "tomato"
    else:
        color = "#f0f0f0"

    # Redirigir con parámetros en la URL (ack y color)
    url = app.url_path_for("index") + f"?ack={ack}&color={color}"
    return RedirectResponse(url, status_code=303)
