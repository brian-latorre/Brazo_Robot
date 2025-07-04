import json
import qrcode
import os

# Carpeta donde están todos los archivos JSON
carpeta_data = '../data'
# Carpeta donde se guardarán las imágenes PNG del QR
carpeta_qr = '../qr_codes_new'

# Crear la carpeta de salida si no existe
os.makedirs(carpeta_qr, exist_ok=True)

# Obtener lista de todos los archivos JSON en la carpeta data
archivos_json = [f for f in os.listdir(carpeta_data) if f.endswith('.json')]

# Recorrer cada archivo JSON
for archivo in archivos_json:
    ruta_completa = os.path.join(carpeta_data, archivo)
    
    # Abrir y leer el contenido del archivo JSON
    with open(ruta_completa, 'r', encoding='utf-8') as f:
        datos = json.load(f)
    
    # Convertir el diccionario a texto JSON
    contenido_qr = json.dumps(datos, ensure_ascii=False)

    # Generar el código QR
    qr = qrcode.make(contenido_qr)
    
    # Obtener el nombre del archivo de salida (ej. A00100.png)
    nombre_archivo_salida = f"{datos['ID']}.png"
    ruta_salida = os.path.join(carpeta_qr, nombre_archivo_salida)
    
    # Guardar la imagen del QR
    qr.save(ruta_salida)
    
    print(f"✅ QR generado: {ruta_salida}")