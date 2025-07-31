import pandas as pd
from pathlib import Path

# Definición de los datos
# Cada fila es un diccionario. Aquí es donde podemos agregar más datos.
datos = [
    {"ID": 100100, "Nombre": "Pasta Dental", "Categoria": "Cuidado personal",
     "Destino": "Zona 2", "Fecha": "2025-07-10"},
    {"ID": 100101, "Nombre": "Harina", "Categoria": "Alimentos",
     "Destino": "Zona 1", "Fecha": "2025-04-10"},
    {"ID": 100102, "Nombre": "Mascarillas", "Categoria": "Salud",
     "Destino": "Zona 3", "Fecha": "2025-07-11"},
    {"ID": 100103, "Nombre": "Aceite", "Categoria": "Alimentos",
     "Destino": "Zona 1", "Fecha": "2025-08-21"},
    {"ID": 100104, "Nombre": "Alcohol", "Categoria": "Salud",
     "Destino": "Zona 3", "Fecha": "2025-12-30"},
]

# Se crea el Dataframe
df = pd.DataFrame(datos)

# Aseguramos el tipo de dato
df["ID"]    = df["ID"].astype(int)
df["Fecha"] = pd.to_datetime(df["Fecha"])        # la mantienes como datetime64[ns]

# Ruta de salida. Aquí se genera el archivo
ruta_csv = Path(__file__).with_name("inventario.csv")  # mismo dir que el script

# Guardamos el .csv
df.to_csv(ruta_csv, index=False, date_format="%Y-%m-%d", encoding="utf-8")

print(f"Archivo generado en: {ruta_csv.resolve()}")
