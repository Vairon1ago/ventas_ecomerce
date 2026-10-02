import pandas as pd
import os

entrada = "Scr/Archivos_limpios"
salida = "Scr/Archivos_limpios"

os.makedirs(salida, exist_ok=True)

clientes = pd.read_csv(
    f"{entrada}/clientes.csv"
)

productos = pd.read_csv(
    f"{entrada}/productos.csv"
)

pedidos = pd.read_csv(
    f"{entrada}/pedidos.csv"
)

detalle = pd.read_csv(
    f"{entrada}/detalle_pedidos.csv"
)

envios = pd.read_csv(
    f"{entrada}/envios.csv"
)

pagos = pd.read_csv(
    f"{entrada}/canal_pago.csv"
)

clientes.to_csv(
    f"{salida}/clientes_limpios.csv",
    index=False,
    encoding="utf-8-sig"
)

productos.to_csv(
    f"{salida}/productos_limpios.csv",
    index=False,
    encoding="utf-8-sig"
)

pedidos.to_csv(
    f"{salida}/pedidos_limpios.csv",
    index=False,
    encoding="utf-8-sig"
)

detalle.to_csv(
    f"{salida}/detalle_pedidos_limpios.csv",
    index=False,
    encoding="utf-8-sig"
)

envios.to_csv(
    f"{salida}/envios_limpios.csv",
    index=False,
    encoding="utf-8-sig"
)

pagos.to_csv(
    f"{salida}/canal_pago_limpio.csv",
    index=False,
    encoding="utf-8-sig"
)

print("TABLAS LIMPIAS GENERADAS")
print()
print("Clientes:", len(clientes))
print("Productos:", len(productos))
print("Pedidos:", len(pedidos))
print("Detalle:", len(detalle))
print("Envíos:", len(envios))
print("Pagos:", len(pagos))
print()
print("Archivos guardados en:")
print("Scr/Archivos_limpios/")