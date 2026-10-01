import pandas as pd
import os


archivo = "Datos/ecommerce_datos_crudos_sucios_400_filas-1.csv"

carpeta_salida = "Salida"


print("     PROCESAMIENTO DE DATOS E-COMMERCE")

print("\nCargando archivo...")

df = pd.read_csv(archivo)

print("Archivo cargado correctamente.")
print("Filas:", len(df))
print("Columnas:", len(df.columns))


print("TABLAS ENCONTRADAS")

print(df["tabla_origen"].value_counts())


print("\nSeparando tablas...")


clientes = df[
    df["tabla_origen"] == "raw_clientes"
].copy()


productos = df[
    df["tabla_origen"] == "raw_productos"
].copy()


pedidos = df[
    df["tabla_origen"] == "raw_pedidos"
].copy()


detalle_pedidos = df[
    df["tabla_origen"] == "raw_detalle_pedidos"
].copy()


envios = df[
    df["tabla_origen"] == "raw_envios"
].copy()


canal_pago = df[
    df["tabla_origen"] == "raw_canal_pago"
].copy()


os.makedirs(carpeta_salida, exist_ok=True)



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

print("Clientes:", len(clientes))
print("Productos:", len(productos))
print("Pedidos:", len(pedidos))
print("Detalle pedidos:", len(detalle_pedidos))
print("Envíos:", len(envios))
print("Canal de pago:", len(canal_pago))


print("PROCESO TERMINADO CORRECTAMENTE")

print("\nLos archivos fueron guardados en:")
print("Salida/")