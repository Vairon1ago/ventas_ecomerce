import pandas as pd

archivo = "datos/ecommerce_datos_crudos_sucios_400_filas.csv"

df = pd.read_csv(archivo)

print("Archivo cargado correctamente")
print("Cantidad de filas:", len(df))
print("Cantidad de columnas:", len(df.columns))

print("\nTablas encontradas:")
print(df["tabla_origen"].value_counts())