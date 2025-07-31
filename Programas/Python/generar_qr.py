import pandas as pd
import qrcode
import os

# Leer el .csv
csv_file = "D:/2025-II/General_System/Data/inventario.csv"
df = pd.read_csv(csv_file)

# Creación de la carpeta de salida
carpeta_salida = "Images_QR"
os.makedirs(carpeta_salida, exist_ok=True)

# Generar un QR para cada ID
for id_valor in df["ID"]:
    id_str = str(id_valor)  # Asegurarse de que sea texto

    # Creación del QR solo con el ID
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=16,
        border=2
    )
    qr.add_data(id_str)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Guardar la imagen
    ruta_png = os.path.join(carpeta_salida, f"{id_str}.png")
    img.save(ruta_png)
    print(f"✅ QR generado: {ruta_png}")

print("\nTodos los QR fueron generados correctamente.")
