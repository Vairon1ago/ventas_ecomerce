import os
import shutil

nueva_carpeta = "mis_tablas"

if not os.path.exists(nueva_carpeta):
    os.makedirs(nueva_carpeta)
    print(f"Carpeta '{nueva_carpeta}' creada.")

archivo_origen = "datos.csv" # Nombre o ruta de tu tabla
archivo_destino = os.path.join(nueva_carpeta, "datos.csv")

if os.path.exists(archivo_origen):
    shutil.move(archivo_origen, archivo_destino)
    print(f"Archivo movido a: {archivo_destino}")
else:
    print(f"El archivo '{archivo_origen}' no existe.")