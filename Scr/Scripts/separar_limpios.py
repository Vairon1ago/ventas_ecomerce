import pandas as pd
import os

entrada = "Scr/Archivos_sucios"
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

clientes = clientes[
    [
        "id_cliente",
        "nombre_completo",
        "documento_identidad",
        "correo_electronico",
        "telefono",
        "direccion",
        "fecha_registro"
    ]
].copy()

productos = productos[
    [
        "id_producto",
        "sku_codigo",
        "nombre_producto",
        "categoria",
        "marca",
        "precio_unitario",
        "stock_disponible"
    ]
].copy()

pedidos = pedidos[
    [
        "id_pedido",
        "id_cliente",
        "fecha_pedido",
        "canal_venta",
        "metodo_pago",
        "estado_pedido",
        "monto_total"
    ]
].copy()

detalle = detalle[
    [
        "id_detalle",
        "id_pedido",
        "id_producto",
        "cantidad",
        "precio_unitario",
        "descuento_aplicado"
    ]
].copy()

envios = envios[
    [
        "id_envio",
        "id_pedido",
        "empresa_transporte",
        "codigo_rastreo",
        "direccion_entrega",
        "fecha_despacho",
        "fecha_entrega"
    ]
].copy()

pagos = pagos[
    [
        "id_pago",
        "id_pedido",
        "pasarela",
        "tipo_tarjeta",
        "monto_procesado",
        "codigo_respuesta"
    ]
].copy()

clientes.to_csv(
    f"{salida}/clientes.csv",
    index=False,
    encoding="utf-8-sig"
)

productos.to_csv(
    f"{salida}/productos.csv",
    index=False,
    encoding="utf-8-sig"
)

pedidos.to_csv(
    f"{salida}/pedidos.csv",
    index=False,
    encoding="utf-8-sig"
)

detalle.to_csv(
    f"{salida}/detalle_pedidos.csv",
    index=False,
    encoding="utf-8-sig"
)

envios.to_csv(
    f"{salida}/envios.csv",
    index=False,
    encoding="utf-8-sig"
)

pagos.to_csv(
    f"{salida}/canal_pago.csv",
    index=False,
    encoding="utf-8-sig"
)

print("Tablas separadas correctamente.")
print("Archivos preparados en Scr/Archivos_limpios/")