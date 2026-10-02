import pandas as pd
import sqlite3
import os

carpeta = "Scr/Archivos_limpios"
base_datos = "Scr/Base_de_datos/ecommerce.db"

os.makedirs("Scr/Base_de_datos", exist_ok=True)

conexion = sqlite3.connect(base_datos)

clientes = pd.read_csv(
    f"{carpeta}/clientes_limpios.csv"
)

productos = pd.read_csv(
    f"{carpeta}/productos_limpios.csv"
)

pedidos = pd.read_csv(
    f"{carpeta}/pedidos_limpios.csv"
)

detalle_pedidos = pd.read_csv(
    f"{carpeta}/detalle_pedidos_limpios.csv"
)

envios = pd.read_csv(
    f"{carpeta}/envios_limpios.csv"
)

canal_pago = pd.read_csv(
    f"{carpeta}/canal_pago_limpio.csv"
)

clientes.to_sql(
    "clientes",
    conexion,
    if_exists="replace",
    index=False
)

productos.to_sql(
    "productos",
    conexion,
    if_exists="replace",
    index=False
)

pedidos.to_sql(
    "pedidos",
    conexion,
    if_exists="replace",
    index=False
)

detalle_pedidos.to_sql(
    "detalle_pedidos",
    conexion,
    if_exists="replace",
    index=False
)

envios.to_sql(
    "envios",
    conexion,
    if_exists="replace",
    index=False
)

canal_pago.to_sql(
    "canal_pago",
    conexion,
    if_exists="replace",
    index=False
)

conexion.close()

print("Base de datos creada correctamente.")
print("Archivo: Scr/Base_de_datos/ecommerce.db")