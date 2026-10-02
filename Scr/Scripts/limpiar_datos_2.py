import pandas as pd
import os

entrada = "Scr/Archivos_limpios"

clientes = pd.read_csv(f"{entrada}/clientes.csv")
productos = pd.read_csv(f"{entrada}/productos.csv")
pedidos = pd.read_csv(f"{entrada}/pedidos.csv")
detalle = pd.read_csv(f"{entrada}/detalle_pedidos.csv")
envios = pd.read_csv(f"{entrada}/envios.csv")
pagos = pd.read_csv(f"{entrada}/canal_pago.csv")

print("LIMPIEZA DE DATOS E-COMMERCE")
print()

for columna in [
    "id_cliente",
    "nombre_completo",
    "documento_identidad",
    "correo_electronico",
    "telefono",
    "direccion"
]:
    clientes[columna] = (
        clientes[columna]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
    )

clientes["correo_electronico"] = (
    clientes["correo_electronico"]
    .str.lower()
)

clientes["telefono"] = (
    clientes["telefono"]
    .str.replace(r"\D", "", regex=True)
    .str.replace(r"^57", "", regex=True)
)

clientes["correo_valido"] = clientes[
    "correo_electronico"
].str.match(
    r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
)

clientes.loc[
    ~clientes["correo_valido"],
    "correo_electronico"
] = ""

clientes.drop(
    columns=["correo_valido"],
    inplace=True
)

clientes["fecha_registro"] = pd.to_datetime(
    clientes["fecha_registro"],
    dayfirst=True,
    errors="coerce"
)

clientes["fecha_registro"] = (
    clientes["fecha_registro"]
    .dt.strftime("%Y-%m-%d")
)

clientes = clientes.drop_duplicates(
    subset=["documento_identidad"],
    keep="first"
)

for columna in [
    "id_producto",
    "sku_codigo",
    "nombre_producto",
    "categoria",
    "marca"
]:
    productos[columna] = (
        productos[columna]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
    )

def normalizar_categoria(valor):
    valor = valor.lower().strip()

    if valor in [
        "electronica",
        "electrónica",
        "electronics"
    ]:
        return "Electrónica"

    if valor == "ropa":
        return "Ropa"

    if valor == "audio":
        return "Audio"

    if valor == "calzado":
        return "Calzado"

    if valor == "accesorios":
        return "Accesorios"

    if valor in [
        "tecnología",
        "tecnologia"
    ]:
        return "Tecnología"

    return valor.title()

productos["categoria"] = productos[
    "categoria"
].apply(normalizar_categoria)

productos["marca"] = productos["marca"].replace(
    ["", "nan", "None"],
    pd.NA
)

def limpiar_precio(valor):
    if pd.isna(valor):
        return None

    valor = str(valor).strip()
    valor = valor.replace("USD", "")
    valor = valor.replace("$", "")
    valor = valor.replace(" ", "")
    valor = valor.replace(",", "")

    try:
        return float(valor)
    except:
        return None

productos["precio_unitario"] = productos[
    "precio_unitario"
].apply(limpiar_precio)

productos["stock_disponible"] = pd.to_numeric(
    productos["stock_disponible"],
    errors="coerce"
)

productos.loc[
    productos["stock_disponible"] < 0,
    "stock_disponible"
] = 0

productos["stock_disponible"] = (
    productos["stock_disponible"]
    .fillna(0)
    .astype(int)
)

productos = productos.drop_duplicates(
    subset=["id_producto"],
    keep="first"
)

for columna in [
    "id_pedido",
    "id_cliente",
    "canal_venta",
    "metodo_pago",
    "estado_pedido"
]:
    pedidos[columna] = (
        pedidos[columna]
        .fillna("")
        .astype(str)
        .str.strip()
    )

pedidos["canal_venta"] = (
    pedidos["canal_venta"]
    .str.lower()
    .str.title()
)

pedidos["metodo_pago"] = (
    pedidos["metodo_pago"]
    .str.lower()
    .str.title()
)

def normalizar_estado(valor):
    valor = valor.lower().strip()

    if valor in [
        "completado",
        "paid"
    ]:
        return "Completado"

    if valor in [
        "cancel",
        "cancelado"
    ]:
        return "Cancelado"

    if valor == "pendiente":
        return "Pendiente"

    return valor.title()

pedidos["estado_pedido"] = (
    pedidos["estado_pedido"]
    .apply(normalizar_estado)
)

pedidos["fecha_pedido"] = pd.to_datetime(
    pedidos["fecha_pedido"],
    dayfirst=True,
    errors="coerce"
)

hoy = pd.Timestamp.today().normalize()

pedidos.loc[
    pedidos["fecha_pedido"] > hoy,
    "fecha_pedido"
] = pd.NaT

pedidos["fecha_pedido"] = (
    pedidos["fecha_pedido"]
    .dt.strftime("%Y-%m-%d")
)

pedidos["monto_total"] = (
    pedidos["monto_total"]
    .astype(str)
    .str.replace("$", "", regex=False)
    .str.replace(",", "", regex=False)
)

pedidos["monto_total"] = pd.to_numeric(
    pedidos["monto_total"],
    errors="coerce"
)

pedidos = pedidos[
    pedidos["id_pedido"].ne("")
]

pedidos = pedidos.drop_duplicates(
    subset=["id_pedido"],
    keep="first"
)

ids_clientes_validos = set(
    clientes["id_cliente"]
)

pedidos = pedidos[
    pedidos["id_cliente"].isin(
        ids_clientes_validos
    )
]

for columna in [
    "id_detalle",
    "id_pedido",
    "id_producto"
]:
    detalle[columna] = (
        detalle[columna]
        .fillna("")
        .astype(str)
        .str.strip()
    )

detalle["cantidad"] = pd.to_numeric(
    detalle["cantidad"],
    errors="coerce"
)

detalle = detalle[
    detalle["cantidad"] > 0
]

detalle["cantidad"] = (
    detalle["cantidad"]
    .astype(int)
)

detalle["precio_unitario"] = pd.to_numeric(
    detalle["precio_unitario"],
    errors="coerce"
)

detalle["descuento_aplicado"] = pd.to_numeric(
    detalle["descuento_aplicado"],
    errors="coerce"
)

detalle["descuento_aplicado"] = (
    detalle["descuento_aplicado"]
    .fillna(0)
)

detalle["total_linea"] = (
    detalle["cantidad"]
    * detalle["precio_unitario"]
    - detalle["descuento_aplicado"]
)

detalle = detalle[
    detalle["total_linea"] >= 0
]

ids_pedidos_validos = set(
    pedidos["id_pedido"]
)

detalle = detalle[
    detalle["id_pedido"].isin(
        ids_pedidos_validos
    )
]

ids_productos_validos = set(
    productos["id_producto"]
)

detalle = detalle[
    detalle["id_producto"].isin(
        ids_productos_validos
    )
]

detalle = detalle.drop_duplicates()

detalle.drop(
    columns=["total_linea"],
    inplace=True
)

for columna in [
    "id_envio",
    "id_pedido",
    "empresa_transporte",
    "codigo_rastreo",
    "direccion_entrega"
]:
    envios[columna] = (
        envios[columna]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
    )

def normalizar_transporte(valor):
    valor = valor.lower().strip()

    if (
        "servientrega" in valor
        or "servi-entrega" in valor
    ):
        return "Servientrega"

    if "coordinadora" in valor:
        return "Coordinadora"

    if "interrapid" in valor:
        return "Interrapidísimo"

    return valor.title()

envios["empresa_transporte"] = (
    envios["empresa_transporte"]
    .apply(normalizar_transporte)
)

envios["fecha_despacho"] = pd.to_datetime(
    envios["fecha_despacho"],
    errors="coerce"
)

envios["fecha_entrega"] = pd.to_datetime(
    envios["fecha_entrega"],
    errors="coerce"
)

envios.loc[
    envios["fecha_entrega"]
    < envios["fecha_despacho"],
    "fecha_entrega"
] = pd.NaT

envios["fecha_despacho"] = (
    envios["fecha_despacho"]
    .dt.strftime("%Y-%m-%d")
)

envios["fecha_entrega"] = (
    envios["fecha_entrega"]
    .dt.strftime("%Y-%m-%d")
)

envios = envios[
    envios["id_pedido"].isin(
        ids_pedidos_validos
    )
]

envios = envios.drop_duplicates(
    subset=["id_envio"],
    keep="first"
)

for columna in [
    "id_pago",
    "id_pedido",
    "pasarela",
    "tipo_tarjeta",
    "codigo_respuesta"
]:
    pagos[columna] = (
        pagos[columna]
        .fillna("")
        .astype(str)
        .str.strip()
    )

def normalizar_pasarela(valor):
    valor = valor.lower().strip()

    if valor == "mercadopago":
        return "Mercado Pago"

    if valor == "mercado pago":
        return "Mercado Pago"

    if valor == "payu":
        return "PayU"

    if valor == "wompi":
        return "Wompi"

    return valor.title()

pagos["pasarela"] = (
    pagos["pasarela"]
    .apply(normalizar_pasarela)
)

pagos["tipo_tarjeta"] = (
    pagos["tipo_tarjeta"]
    .replace("", pd.NA)
    .str.title()
)

pagos["monto_procesado"] = pd.to_numeric(
    pagos["monto_procesado"],
    errors="coerce"
)

pagos = pagos[
    pagos["id_pedido"].isin(
        ids_pedidos_validos
    )
]

pagos = pagos.drop_duplicates(
    subset=["id_pago"],
    keep="first"
)

clientes.to_csv(
    "Scr/Archivos_limpios/clientes_procesados.csv",
    index=False,
    encoding="utf-8-sig"
)

productos.to_csv(
    "Scr/Archivos_limpios/productos_procesados.csv",
    index=False,
    encoding="utf-8-sig"
)

pedidos.to_csv(
    "Scr/Archivos_limpios/pedidos_procesados.csv",
    index=False,
    encoding="utf-8-sig"
)

detalle.to_csv(
    "Scr/Archivos_limpios/detalle_pedidos_procesados.csv",
    index=False,
    encoding="utf-8-sig"
)

envios.to_csv(
    "Scr/Archivos_limpios/envios_procesados.csv",
    index=False,
    encoding="utf-8-sig"
)

pagos.to_csv(
    "Scr/Archivos_limpios/canal_pago_procesado.csv",
    index=False,
    encoding="utf-8-sig"
)

print("Limpieza completada.")