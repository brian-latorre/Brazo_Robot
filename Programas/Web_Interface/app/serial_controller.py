import serial
import time
from threading import Lock

class SerialController:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._init_serial()
        return cls._instance

    def _init_serial(self):
        self.port = "COM3"
        self.baudrate = 9600

        try:
            print("✅ Conectado a COM3")
            self.ser = serial.Serial(self.port, self.baudrate, timeout=2)
            time.sleep(2)

            while True:
                line = self.ser.readline().decode(errors="ignore").strip()
                print(f"[Serial] ← {line}")
                if line == "READY":
                    print("[Serial] Arduino está listo.")
                    break
        except Exception as e:
            print(f"[Serial Error] {e}")
            self.ser = None

    def send(self, cmd: str) -> str:
        if not self.ser:
            return "ERR: Arduino no conectado"

        try:
            self.ser.write((cmd + '\n').encode())
            print(f"[Serial] → {cmd}")
            response = self.ser.readline().decode(errors="ignore").strip()
            print(f"[Serial] ← {response}")
            return response if response else "ERR: Sin respuesta"
        except Exception as e:
            return f"ERR: {e}"
