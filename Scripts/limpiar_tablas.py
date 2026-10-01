import pandas as pd
import os
import re

# CONFIGURACIÓN

ARCHIVO = "Datos/ecommerce_datos_crudos_sucios_400_filas-1.csv"
CARPETA_SALIDA = "Salida"


# Crear carpeta de salida si no existe
os.makedirs(CARPETA_SALIDA, exist_ok=True)


# CARGAR DATOS

print("       LIMPIEZA DE DATOS E-COMMERCE")

print("\nCargando archivo...")

df = pd.read_csv(ARCHIVO)

print("Archivo cargado correctamente.")
print("Total de registros:", len(df))


# SEPARAR LAS TABLAS

clientes = df[df["tabla_origen"] == "raw_clientes"].copy()

productos = df[df["tabla_origen"] == "raw_productos"].copy()

pedidos = df[df["tabla_origen"] == "raw_pedidos"].copy()

detalle = df[df["tabla_origen"] == "raw_detalle_pedidos"].copy()

envios = df[df["tabla_origen"] == "raw_envios"].copy()

pagos = df[df["tabla_origen"] == "raw_canal_pago"].copy()


# 1. LIMPIEZA DE CLIENTES

print("\n[1/6] Limpiando clientes...")


# Columnas que realmente pertenecen a clientes
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


# Eliminar espacios al principio y al final
clientes["id_cliente"] = clientes["id_cliente"].astype(str).str.strip()

clientes["nombre_completo"] = (
    clientes["nombre_completo"]
    .astype(str)
    .str.strip()
    .str.replace(r"\s+", " ", regex=True)
)


clientes["documento_identidad"] = (
    clientes["documento_identidad"]
    .astype(str)
    .str.strip()
)


clientes["correo_electronico"] = (
    clientes["correo_electronico"]
    .astype(str)
    .str.strip()
    .str.lower()
)


clientes["telefono"] = (
    clientes["telefono"]
    .astype(str)
    .str.strip()
)


clientes["direccion"] = (
    clientes["direccion"]
    .astype(str)
    .str.strip()
    .str.replace(r"\s+", " ", regex=True)
)


# Normalizar teléfonos
clientes["telefono"] = (
    clientes["telefono"]
    .str.replace(r"\D", "", regex=True)
)


# Si comienza con 57, quitarlo para dejar el número nacional
clientes["telefono"] = clientes["telefono"].str.replace(
    r"^57", "", regex=True
)


# Validar correos
clientes["correo_valido"] = clientes["correo_electronico"].str.match(
    r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
)


# Los correos incorrectos quedan vacíos
clientes.loc[
    ~clientes["correo_valido"],
    "correo_electronico"
] = ""


# Eliminar columna auxiliar
clientes.drop(
    columns=["correo_valido"],
    inplace=True
)


# Convertir fechas
clientes["fecha_registro"] = pd.to_datetime(
    clientes["fecha_registro"],
    dayfirst=True,
    errors="coerce"
)


# Formato único YYYY-MM-DD
clientes["fecha_registro"] = (
    clientes["fecha_registro"]
    .dt.strftime("%Y-%m-%d")
)


# Eliminar duplicados por documento
clientes = clientes.drop_duplicates(
    subset=["documento_identidad"],
    keep="first"
)


# Guardar
clientes.to_csv(
    f"{CARPETA_SALIDA}/clientes_limpios.csv",
    index=False,
    encoding="utf-8-sig"
)


print("Clientes limpios:", len(clientes))


# 2. LIMPIEZA DE PRODUCTOS

print("\n[2/6] Limpiando productos...")


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


# Limpiar textos
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


# Normalizar categorías
def normalizar_categoria(valor):

    valor = valor.lower().strip()

    if valor in ["electronica", "electrónica", "electronics"]:
        return "Electrónica"

    if valor in ["ropa"]:
        return "Ropa"

    if valor in ["audio"]:
        return "Audio"

    if valor in ["calzado"]:
        return "Calzado"

    if valor in ["accesorios"]:
        return "Accesorios"

    if valor in ["tecnología", "tecnologia"]:
        return "Tecnología"

    return valor.title()


productos["categoria"] = productos[
    "categoria"
].apply(normalizar_categoria)


# Limpiar marcas vacías
productos["marca"] = productos["marca"].replace(
    ["", "nan", "None"],
    pd.NA
)


# Limpiar precios
def limpiar_precio(valor):

    if pd.isna(valor):
        return None

    valor = str(valor).strip()

    # Quitar USD
    valor = valor.replace("USD", "")

    # Quitar símbolo $
    valor = valor.replace("$", "")

    # Quitar espacios
    valor = valor.replace(" ", "")

    # Quitar separadores de miles
    valor = valor.replace(",", "")

    try:
        return float(valor)

    except:
        return None


productos["precio_unitario"] = (
    productos["precio_unitario"]
    .apply(limpiar_precio)
)


# Convertir stock
productos["stock_disponible"] = pd.to_numeric(
    productos["stock_disponible"],
    errors="coerce"
)


# Stock negativo pasa a 0
productos.loc[
    productos["stock_disponible"] < 0,
    "stock_disponible"
] = 0


productos["stock_disponible"] = (
    productos["stock_disponible"]
    .fillna(0)
    .astype(int)
)


# Eliminar productos duplicados
productos = productos.drop_duplicates(
    subset=["id_producto"],
    keep="first"
)


productos.to_csv(
    f"{CARPETA_SALIDA}/productos_limpios.csv",
    index=False,
    encoding="utf-8-sig"
)


print("Productos limpios:", len(productos))


# 3. LIMPIEZA DE PEDIDOS

print("\n[3/6] Limpiando pedidos...")


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


# Limpiar textos
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


# Normalizar canal
pedidos["canal_venta"] = (
    pedidos["canal_venta"]
    .str.lower()
    .str.title()
)


# Normalizar métodos de pago
pedidos["metodo_pago"] = (
    pedidos["metodo_pago"]
    .str.lower()
    .str.title()
)


# Normalizar estados
def normalizar_estado(valor):

    valor = valor.lower().strip()

    if valor in ["completado", "paid"]:
        return "Completado"

    if valor in ["cancel", "cancelado"]:
        return "Cancelado"

    if valor in ["pendiente"]:
        return "Pendiente"

    return valor.title()


pedidos["estado_pedido"] = (
    pedidos["estado_pedido"]
    .apply(normalizar_estado)
)


# Fechas
pedidos["fecha_pedido"] = pd.to_datetime(
    pedidos["fecha_pedido"],
    dayfirst=True,
    errors="coerce"
)


# Eliminar pedidos con fechas futuras
hoy = pd.Timestamp.today().normalize()

pedidos.loc[
    pedidos["fecha_pedido"] > hoy,
    "fecha_pedido"
] = pd.NaT


pedidos["fecha_pedido"] = (
    pedidos["fecha_pedido"]
    .dt.strftime("%Y-%m-%d")
)


# Limpiar monto
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


# Quitar pedidos sin ID
pedidos = pedidos[
    pedidos["id_pedido"].ne("")
]


# Quitar duplicados
pedidos = pedidos.drop_duplicates(
    subset=["id_pedido"],
    keep="first"
)


# Validar clientes existentes
ids_clientes_validos = set(
    clientes["id_cliente"]
)


pedidos = pedidos[
    pedidos["id_cliente"].isin(ids_clientes_validos)
]


pedidos.to_csv(
    f"{CARPETA_SALIDA}/pedidos_limpios.csv",
    index=False,
    encoding="utf-8-sig"
)


print("Pedidos limpios:", len(pedidos))


# 4. LIMPIEZA DEL DETALLE DE PEDIDOS

print("\n[4/6] Limpiando detalle de pedidos...")


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


# Limpiar identificadores
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


# Convertir cantidades
detalle["cantidad"] = pd.to_numeric(
    detalle["cantidad"],
    errors="coerce"
)


# Eliminar cantidades inválidas
detalle = detalle[
    detalle["cantidad"] > 0
]


detalle["cantidad"] = (
    detalle["cantidad"]
    .astype(int)
)


# Convertir precios
detalle["precio_unitario"] = pd.to_numeric(
    detalle["precio_unitario"],
    errors="coerce"
)


detalle["descuento_aplicado"] = pd.to_numeric(
    detalle["descuento_aplicado"],
    errors="coerce"
)


# Descuento vacío = 0
detalle["descuento_aplicado"] = (
    detalle["descuento_aplicado"]
    .fillna(0)
)


# Evitar descuentos mayores al valor de la línea
detalle["total_linea"] = (
    detalle["cantidad"] *
    detalle["precio_unitario"]
    - detalle["descuento_aplicado"]
)


# Eliminar valores matemáticamente imposibles
detalle = detalle[
    detalle["total_linea"] >= 0
]


# Validar pedidos existentes
ids_pedidos_validos = set(
    pedidos["id_pedido"]
)


detalle = detalle[
    detalle["id_pedido"].isin(ids_pedidos_validos)
]


# Validar productos existentes
ids_productos_validos = set(
    productos["id_producto"]
)


detalle = detalle[
    detalle["id_producto"].isin(ids_productos_validos)
]


# Eliminar duplicados exactos
detalle = detalle.drop_duplicates()


# Quitar columna auxiliar
detalle.drop(
    columns=["total_linea"],
    inplace=True
)


detalle.to_csv(
    f"{CARPETA_SALIDA}/detalle_pedidos_limpios.csv",
    index=False,
    encoding="utf-8-sig"
)


print("Detalles limpios:", len(detalle))


# 5. LIMPIEZA DE ENVÍOS

print("\n[5/6] Limpiando envíos...")


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


# Limpiar textos
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


# Normalizar empresas
def normalizar_transporte(valor):

    valor = valor.lower().strip()

    if "servientrega" in valor or "servi-entrega" in valor:
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


# Fechas
envios["fecha_despacho"] = pd.to_datetime(
    envios["fecha_despacho"],
    errors="coerce"
)


envios["fecha_entrega"] = pd.to_datetime(
    envios["fecha_entrega"],
    errors="coerce"
)


# Si entrega es anterior al despacho,
# se elimina la fecha incorrecta
envios.loc[
    envios["fecha_entrega"] < envios["fecha_despacho"],
    "fecha_entrega"
] = pd.NaT


# Formato final
envios["fecha_despacho"] = (
    envios["fecha_despacho"]
    .dt.strftime("%Y-%m-%d")
)


envios["fecha_entrega"] = (
    envios["fecha_entrega"]
    .dt.strftime("%Y-%m-%d")
)


# Validar pedidos existentes
envios = envios[
    envios["id_pedido"].isin(ids_pedidos_validos)
]


# Eliminar duplicados
envios = envios.drop_duplicates(
    subset=["id_envio"],
    keep="first"
)


envios.to_csv(
    f"{CARPETA_SALIDA}/envios_limpios.csv",
    index=False,
    encoding="utf-8-sig"
)


print("Envíos limpios:", len(envios))


# 6. LIMPIEZA DEL CANAL DE PAGO

print("\n[6/6] Limpiando canal de pago...")


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


# Limpiar textos
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


# Normalizar pasarelas
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


# Normalizar tarjetas
pagos["tipo_tarjeta"] = (
    pagos["tipo_tarjeta"]
    .replace("", pd.NA)
    .str.title()
)


# Convertir montos
pagos["monto_procesado"] = pd.to_numeric(
    pagos["monto_procesado"],
    errors="coerce"
)


# Validar pedidos existentes
pagos = pagos[
    pagos["id_pedido"].isin(ids_pedidos_validos)
]


# Eliminar pagos duplicados
pagos = pagos.drop_duplicates(
    subset=["id_pago"],
    keep="first"
)


pagos.to_csv(
    f"{CARPETA_SALIDA}/canal_pago_limpio.csv",
    index=False,
    encoding="utf-8-sig"
)


print("Pagos limpios:", len(pagos))


# FINAL

print("       LIMPIEZA FINALIZADA")

print("\nArchivos generados:")

print("✓ clientes_limpios.csv")
print("✓ productos_limpios.csv")
print("✓ pedidos_limpios.csv")
print("✓ detalle_pedidos_limpios.csv")
print("✓ envios_limpios.csv")
print("✓ canal_pago_limpio.csv")

print("\nTodos los archivos están en la carpeta:")
print("Salida/")