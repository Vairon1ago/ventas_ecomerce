import pandas as pd
import os

archivo = "Scr/Entrada_de_datos/ecommerce_datos_crudos_sucios_400_filas-1.csv"
carpeta_salida = "Scr/Archivos_sucios"

os.makedirs(carpeta_salida, exist_ok=True)

print("PROCESAMIENTO DE DATOS E-COMMERCE")
print()
print("Cargando archivo...")

df = pd.read_csv(archivo)

print("Archivo cargado correctamente.")
print("Filas:", len(df))
print("Columnas:", len(df.columns))
print()

print("TABLAS ENCONTRADAS")
print(df["tabla_origen"].value_counts())
print()

clientes = df[df["tabla_origen"] == "raw_clientes"].copy()
productos = df[df["tabla_origen"] == "raw_productos"].copy()
pedidos = df[df["tabla_origen"] == "raw_pedidos"].copy()
detalle_pedidos = df[df["tabla_origen"] == "raw_detalle_pedidos"].copy()
envios = df[df["tabla_origen"] == "raw_envios"].copy()
canal_pago = df[df["tabla_origen"] == "raw_canal_pago"].copy()

clientes.to_csv(
    f"{carpeta_salida}/clientes.csv",
    index=False,
    encoding="utf-8-sig"
)

productos.to_csv(
    f"{carpeta_salida}/productos.csv",
    index=False,
    encoding="utf-8-sig"
)

pedidos.to_csv(
    f"{carpeta_salida}/pedidos.csv",
    index=False,
    encoding="utf-8-sig"
)

detalle_pedidos.to_csv(
    f"{carpeta_salida}/detalle_pedidos.csv",
    index=False,
    encoding="utf-8-sig"
)

envios.to_csv(
    f"{carpeta_salida}/envios.csv",
    index=False,
    encoding="utf-8-sig"
)

canal_pago.to_csv(
    f"{carpeta_salida}/canal_pago.csv",
    index=False,
    encoding="utf-8-sig"
)

print("TABLAS GENERADAS")
print()
print("Clientes:", len(clientes))
print("Productos:", len(productos))
print("Pedidos:", len(pedidos))
print("Detalle pedidos:", len(detalle_pedidos))
print("Envíos:", len(envios))
print("Canal de pago:", len(canal_pago))
print()
print("Los archivos fueron guardados en:")
print("Scr/Archivos_sucios/")