# Proyecto de limpieza y organización de datos de E-Commerce

## ¿De qué trata el proyecto?

Este proyecto consiste en tomar unos datos de ventas de un sistema de e-commerce que inicialmente estaban desordenados, tenían errores y estaban mezclados, limpiarlos utilizando Python y Pandas, organizarlos en diferentes tablas y finalmente convertir toda la información limpia en una base de datos SQLite.

La idea principal fue hacer un proceso parecido al que se utilizaría en un proyecto real de datos: primero se reciben los datos originales, después se revisan y limpian, luego se organizan y finalmente se cargan en una base de datos para poder hacer consultas y obtener información.

El proyecto se trabajó utilizando GitHub Codespaces, Visual Studio Code, Python, Pandas y SQLite.

---

# 1. Datos originales

Primero se recibió un archivo CSV llamado:

`ecommerce_datos_crudos_sucios_400_filas-1.csv`

Este archivo contenía aproximadamente 400 registros relacionados con diferentes partes de una tienda virtual.

Los datos estaban intencionalmente "sucios" para poder practicar un proceso de limpieza de datos.

Dentro del archivo estaban mezcladas seis fuentes diferentes:

* Clientes
* Productos
* Pedidos
* Detalle de pedidos
* Envíos
* Canal de pago

Por eso fue necesario separar la información antes de comenzar con la limpieza.

---

# 2. Errores que tenían los datos

Los datos originales no estaban completamente listos para utilizarse en una base de datos. Tenían diferentes problemas que debían detectarse y corregirse.

## Clientes

Los clientes podían tener:

* Correos electrónicos mal escritos.
* Correos sin `@`.
* Nombres con espacios adicionales.
* Caracteres o formatos inconsistentes.
* Teléfonos con diferentes formatos.
* Teléfonos con prefijos mezclados.
* Fechas escritas de diferentes maneras.
* Personas repetidas utilizando el mismo documento de identidad.

Por ejemplo, podían existir fechas como:

`2026-05-20`

y otras como:

`20/05/2026`

También podían existir teléfonos con diferentes formatos o con el prefijo `57`.

---

## Productos

Los productos también tenían errores.

Los precios podían aparecer como:

`$150.00`

`USD 20`

o como valores numéricos normales.

Las categorías podían aparecer de diferentes formas, por ejemplo:

`electronica`

`Electrónica`

`ELECTRONICS`

También existían marcas vacías y algunos productos podían tener valores negativos en el stock.

---

## Pedidos

En los pedidos existían problemas como:

* Estados escritos de diferentes maneras.
* Estados en mayúsculas y minúsculas.
* Estados en inglés.
* Montos totales vacíos.
* Fechas futuras.
* Clientes que no existían en la tabla de clientes.

Por ejemplo, un mismo estado podía aparecer como:

`completado`

`COMPLETADO`

`Paid`

`Cancel`

Estos valores necesitaban ser normalizados.

---

## Detalle de pedidos

En el detalle de cada pedido podían aparecer:

* Cantidades iguales a cero.
* Cantidades negativas.
* Precios diferentes al precio del catálogo.
* Productos repetidos dentro de una misma orden.
* Descuentos inconsistentes.
* Valores que matemáticamente no coincidían con la cantidad y el precio.

Por ejemplo:

`cantidad × precio - descuento`

debía tener sentido matemáticamente.

---

## Envíos

Los datos de envío también tenían problemas.

Podían existir:

* Fechas de entrega anteriores a la fecha de despacho.
* Diferentes formas de escribir la misma empresa.
* Direcciones incompletas.
* Direcciones sin ciudad o departamento.

Por ejemplo:

`Servientrega`

y

`servi-entrega`

representaban la misma empresa y debían quedar con un único nombre.

---

## Canal de pago

Finalmente, la información de los pagos podía tener:

* Transacciones duplicadas.
* El mismo ID de pago repetido.
* Montos procesados diferentes al pedido.
* Tipos de tarjeta vacíos.
* Diferentes formas de escribir las pasarelas.

---

# 3. Separación de los datos

Después de cargar el CSV con Python, se utilizó Pandas para identificar qué registros pertenecían a cada fuente.

La columna `tabla_origen` permitía identificar si un registro correspondía a:

`raw_clientes`

`raw_productos`

`raw_pedidos`

`raw_detalle_pedidos`

`raw_envios`

`raw_canal_pago`

De esta manera se separaron los datos en seis tablas independientes.

---

# 4. Limpieza de los datos

Después de separar las tablas se realizó la limpieza de cada una.

La limpieza se hizo utilizando Python y Pandas.

No se trató simplemente de borrar todos los datos que parecían raros. Se intentó corregir los problemas cuando era posible y eliminar o dejar vacío aquello que no podía corregirse de forma segura.

---

# 5. Limpieza de clientes

En clientes se conservaron únicamente las columnas correspondientes a esta tabla:

* `id_cliente`
* `nombre_completo`
* `documento_identidad`
* `correo_electronico`
* `telefono`
* `direccion`
* `fecha_registro`

Se eliminaron espacios innecesarios de los nombres y direcciones.

Los nombres y direcciones quedaron con un formato más uniforme.

Los teléfonos fueron limpiados para eliminar caracteres que no correspondían al número y se normalizaron los prefijos.

Los correos fueron convertidos a minúsculas y se verificó que tuvieran una estructura válida.

Cuando un correo no tenía un formato válido, no se inventó uno nuevo. Se dejó vacío.

Las fechas fueron convertidas a un único formato:

`YYYY-MM-DD`

También se detectaron registros duplicados utilizando el documento de identidad.

---

# 6. Limpieza de productos

En productos se conservaron:

* `id_producto`
* `sku_codigo`
* `nombre_producto`
* `categoria`
* `marca`
* `precio_unitario`
* `stock_disponible`

Los precios fueron convertidos a números.

Por ejemplo:

`$150.00`

y

`USD 150`

fueron tratados para obtener un valor numérico.

Las categorías fueron normalizadas para evitar tener diferentes nombres para la misma categoría.

Por ejemplo:

`electronica`

`Electrónica`

`ELECTRONICS`

se transformaron en una categoría uniforme.

Los valores negativos de stock fueron corregidos para evitar que existieran cantidades de inventario imposibles.

También se eliminaron productos duplicados por su identificador.

---

# 7. Limpieza de pedidos

En pedidos se conservaron:

* `id_pedido`
* `id_cliente`
* `fecha_pedido`
* `canal_venta`
* `metodo_pago`
* `estado_pedido`
* `monto_total`

Los canales de venta fueron normalizados.

Los métodos de pago también fueron normalizados.

Los diferentes estados fueron unificados.

Por ejemplo:

`completado`

`COMPLETADO`

`Paid`

fueron tratados como diferentes formas de representar un pedido completado.

También se revisaron las fechas y se detectaron fechas posteriores a la fecha actual.

Los montos fueron convertidos a valores numéricos.

Finalmente se verificó que los clientes asociados a los pedidos realmente existieran en la tabla de clientes.

---

# 8. Limpieza del detalle de pedidos

En esta tabla se conservaron:

* `id_detalle`
* `id_pedido`
* `id_producto`
* `cantidad`
* `precio_unitario`
* `descuento_aplicado`

Las cantidades iguales a cero o negativas fueron consideradas inválidas y eliminadas.

Los precios y descuentos fueron convertidos a valores numéricos.

También se realizó una comprobación matemática utilizando:

`cantidad × precio_unitario - descuento_aplicado`

De esta forma se pudieron detectar valores que no tenían sentido.

También se comprobó que los pedidos y productos utilizados en esta tabla existieran realmente en sus respectivas tablas.

---

# 9. Limpieza de envíos

En envíos se conservaron:

* `id_envio`
* `id_pedido`
* `empresa_transporte`
* `codigo_rastreo`
* `direccion_entrega`
* `fecha_despacho`
* `fecha_entrega`

Las empresas de transporte fueron normalizadas.

Por ejemplo:

`Servientrega`

`servi-entrega`

quedaron representadas como:

`Servientrega`

También se revisaron las fechas.

Si una fecha de entrega aparecía antes de la fecha de despacho, esa fecha incorrecta no se mantuvo.

Finalmente se verificó que los pedidos asociados a los envíos existieran.

---

# 10. Limpieza del canal de pago

En esta tabla se conservaron:

* `id_pago`
* `id_pedido`
* `pasarela`
* `tipo_tarjeta`
* `monto_procesado`
* `codigo_respuesta`

Se normalizaron los nombres de las pasarelas de pago.

Los montos fueron convertidos a valores numéricos.

También se eliminaron pagos duplicados utilizando el identificador del pago.

Los tipos de tarjeta que estaban vacíos se conservaron como valores vacíos, ya que no era correcto inventar información que no estaba disponible.

---

# 11. Organización final de los archivos

Después de terminar la limpieza se organizó todo el proyecto de una forma más ordenada.

La estructura final quedó así:

```text
ventas_ecomerce/
│
├── Scr/
│   │
│   ├── Entrada_de_datos/
│   │   └── ecommerce_datos_crudos_sucios_400_filas-1.csv
│   │
│   ├── Archivos_sucios/
│   │   ├── clientes.csv
│   │   ├── productos.csv
│   │   ├── pedidos.csv
│   │   ├── detalle_pedidos.csv
│   │   ├── envios.csv
│   │   └── canal_pago.csv
│   │
│   ├── Archivos_limpios/
│   │   ├── clientes_limpios.csv
│   │   ├── productos_limpios.csv
│   │   ├── pedidos_limpios.csv
│   │   ├── detalle_pedidos_limpios.csv
│   │   ├── envios_limpios.csv
│   │   └── canal_pago_limpio.csv
│   │
│   └── Base_de_datos/
│       └── ecommerce.db
│
├── Scripts/
│   ├── limpiar_datos.py
│   ├── limpiar_clientes.py
│   ├── limpiar_productos.py
│   ├── limpiar_pedidos.py
│   ├── limpiar_detalle_pedidos.py
│   ├── limpiar_envios.py
│   ├── limpiar_canal_pago.py
│   └── crear_base_datos.py
│
└── README.md
```

La carpeta `Entrada_de_datos` contiene el archivo original.

La carpeta `Archivos_sucios` contiene las tablas después de haber sido separadas, pero antes de realizar la limpieza.

La carpeta `Archivos_limpios` contiene las tablas después de haber realizado el proceso de limpieza.

La carpeta `Base_de_datos` contiene la base de datos SQLite.

La carpeta `Scripts` contiene únicamente los programas utilizados para procesar la información.

---

# 12. Creación de la base de datos

Después de tener los archivos limpios se utilizó Python para convertirlos en una base de datos SQLite.

El resultado fue:

`ecommerce.db`

Dentro de este archivo se encuentran las seis tablas:

```text
clientes
productos
pedidos
detalle_pedidos
envios
canal_pago
```

Esto permite pasar de trabajar con varios archivos CSV a trabajar con una sola base de datos.

La información también queda relacionada lógicamente mediante los identificadores.

Por ejemplo:

`clientes`

se relaciona con:

`pedidos`

mediante `id_cliente`.

Los pedidos se relacionan con:

`detalle_pedidos`

mediante `id_pedido`.

Los productos se relacionan con:

`detalle_pedidos`

mediante `id_producto`.

Los envíos y pagos también se relacionan con los pedidos mediante `id_pedido`.

La estructura general puede entenderse así:

```text
CLIENTES
   │
   │ id_cliente
   ▼
PEDIDOS
   │
   │ id_pedido
   ├──────────────► ENVÍOS
   │
   ├──────────────► CANAL DE PAGO
   │
   ▼
DETALLE_PEDIDOS
   │
   │ id_producto
   ▼
PRODUCTOS
```

De esta forma se puede trabajar con la información como una verdadera base de datos relacional.

---

# 13. ¿Cómo entrar a SQLite desde la terminal?

Primero hay que ubicarse en la carpeta principal del proyecto.

Después se ejecuta:

```bash
sqlite3 Scr/Base_de_datos/ecommerce.db
```

Si SQLite está instalado correctamente aparecerá algo parecido a:

```text
SQLite version ...
Enter ".help" for usage hints.
sqlite>
```

A partir de ese momento estamos dentro de la base de datos.

---

# 14. Ver todas las tablas

Una vez dentro de SQLite:

```sql
.tables
```

Esto debe mostrar:

```text
clientes
productos
pedidos
detalle_pedidos
envios
canal_pago
```

---

# 15. Ver la estructura de una tabla

Para ver las columnas de clientes:

```sql
.schema clientes
```

También se puede utilizar:

```sql
PRAGMA table_info(clientes);
```

Para productos:

```sql
PRAGMA table_info(productos);
```

Para pedidos:

```sql
PRAGMA table_info(pedidos);
```

Y lo mismo se puede hacer con las demás tablas.

---

# 16. Ver todos los clientes

```sql
SELECT * FROM clientes;
```

Si hay muchos registros, es más cómodo utilizar:

```sql
SELECT * FROM clientes LIMIT 10;
```

Esto muestra solamente los primeros 10.

---

# 17. Ver todos los productos

```sql
SELECT * FROM productos;
```

O:

```sql
SELECT * FROM productos LIMIT 10;
```

---

# 18. Ver todos los pedidos

```sql
SELECT * FROM pedidos;
```

---

# 19. Ver los detalles de los pedidos

```sql
SELECT * FROM detalle_pedidos;
```

---

# 20. Ver los envíos

```sql
SELECT * FROM envios;
```

---

# 21. Ver los pagos

```sql
SELECT * FROM canal_pago;
```

---

# 22. Contar registros de cada tabla

Para saber cuántos clientes existen:

```sql
SELECT COUNT(*) FROM clientes;
```

Productos:

```sql
SELECT COUNT(*) FROM productos;
```

Pedidos:

```sql
SELECT COUNT(*) FROM pedidos;
```

Detalles:

```sql
SELECT COUNT(*) FROM detalle_pedidos;
```

Envíos:

```sql
SELECT COUNT(*) FROM envios;
```

Pagos:

```sql
SELECT COUNT(*) FROM canal_pago;
```

---

# 23. Consultas sobre clientes

Para buscar clientes por nombre:

```sql
SELECT *
FROM clientes
WHERE nombre_completo LIKE '%Juan%';
```

Para ver los correos:

```sql
SELECT nombre_completo, correo_electronico
FROM clientes;
```

Para ordenar los clientes:

```sql
SELECT *
FROM clientes
ORDER BY nombre_completo;
```

---

# 24. Consultas sobre productos

Para ver los productos más caros:

```sql
SELECT nombre_producto, precio_unitario
FROM productos
ORDER BY precio_unitario DESC;
```

Para ver los productos más baratos:

```sql
SELECT nombre_producto, precio_unitario
FROM productos
ORDER BY precio_unitario ASC;
```

Para consultar una categoría:

```sql
SELECT *
FROM productos
WHERE categoria = 'Electrónica';
```

Para consultar productos con poco inventario:

```sql
SELECT nombre_producto, stock_disponible
FROM productos
WHERE stock_disponible < 10;
```

Para saber cuánto inventario existe:

```sql
SELECT SUM(stock_disponible)
FROM productos;
```

---

# 25. Consultas sobre pedidos

Para ver los pedidos completados:

```sql
SELECT *
FROM pedidos
WHERE estado_pedido = 'Completado';
```

Para ver pedidos cancelados:

```sql
SELECT *
FROM pedidos
WHERE estado_pedido = 'Cancelado';
```

Para contar pedidos por estado:

```sql
SELECT estado_pedido, COUNT(*)
FROM pedidos
GROUP BY estado_pedido;
```

Para contar pedidos por canal:

```sql
SELECT canal_venta, COUNT(*)
FROM pedidos
GROUP BY canal_venta;
```

Para calcular el total vendido:

```sql
SELECT SUM(monto_total)
FROM pedidos;
```

Para calcular el promedio de venta:

```sql
SELECT AVG(monto_total)
FROM pedidos;
```

Para obtener el pedido más caro:

```sql
SELECT *
FROM pedidos
ORDER BY monto_total DESC
LIMIT 1;
```

---

# 26. Consultas sobre detalle de pedidos

Para ver qué productos aparecen en los pedidos:

```sql
SELECT *
FROM detalle_pedidos;
```

Para conocer la cantidad total de productos vendidos:

```sql
SELECT SUM(cantidad)
FROM detalle_pedidos;
```

Para saber qué productos tienen mayor cantidad vendida:

```sql
SELECT id_producto, SUM(cantidad) AS cantidad_vendida
FROM detalle_pedidos
GROUP BY id_producto
ORDER BY cantidad_vendida DESC;
```

---

# 27. Consultas sobre envíos

Para ver las empresas de transporte utilizadas:

```sql
SELECT DISTINCT empresa_transporte
FROM envios;
```

Para contar cuántos envíos realizó cada empresa:

```sql
SELECT empresa_transporte, COUNT(*)
FROM envios
GROUP BY empresa_transporte;
```

Para ver los envíos de un pedido:

```sql
SELECT *
FROM envios
WHERE id_pedido = 'P001';
```

---

# 28. Consultas sobre pagos

Para ver las diferentes pasarelas:

```sql
SELECT DISTINCT pasarela
FROM canal_pago;
```

Para saber cuánto dinero fue procesado:

```sql
SELECT SUM(monto_procesado)
FROM canal_pago;
```

Para contar pagos por pasarela:

```sql
SELECT pasarela, COUNT(*)
FROM canal_pago
GROUP BY pasarela;
```

Para ver los diferentes tipos de tarjeta:

```sql
SELECT tipo_tarjeta, COUNT(*)
FROM canal_pago
GROUP BY tipo_tarjeta;
```

---

# 29. Consultas utilizando varias tablas

Aquí es donde realmente se aprovecha la base de datos.

Por ejemplo, podemos mostrar los clientes junto con sus pedidos:

```sql
SELECT
    clientes.nombre_completo,
    pedidos.id_pedido,
    pedidos.fecha_pedido,
    pedidos.monto_total
FROM clientes
JOIN pedidos
ON clientes.id_cliente = pedidos.id_cliente;
```

También podemos mostrar los pedidos junto con los productos:

```sql
SELECT
    pedidos.id_pedido,
    productos.nombre_producto,
    detalle_pedidos.cantidad,
    detalle_pedidos.precio_unitario
FROM pedidos
JOIN detalle_pedidos
ON pedidos.id_pedido = detalle_pedidos.id_pedido
JOIN productos
ON detalle_pedidos.id_producto = productos.id_producto;
```

---

# 30. Ver qué compró cada cliente

Esta consulta combina clientes, pedidos, detalles y productos:

```sql
SELECT
    clientes.nombre_completo,
    pedidos.id_pedido,
    productos.nombre_producto,
    detalle_pedidos.cantidad
FROM clientes
JOIN pedidos
ON clientes.id_cliente = pedidos.id_cliente
JOIN detalle_pedidos
ON pedidos.id_pedido = detalle_pedidos.id_pedido
JOIN productos
ON detalle_pedidos.id_producto = productos.id_producto;
```

Esta es una de las consultas más importantes porque permite conocer la relación completa:

```text
Cliente
   ↓
Pedido
   ↓
Producto
```

---

# 31. Ver información completa de una venta

También se puede combinar información de productos, clientes, pedidos, pagos y envíos:

```sql
SELECT
    clientes.nombre_completo,
    pedidos.id_pedido,
    productos.nombre_producto,
    detalle_pedidos.cantidad,
    pedidos.monto_total,
    canal_pago.pasarela,
    envios.empresa_transporte
FROM clientes
JOIN pedidos
ON clientes.id_cliente = pedidos.id_cliente
JOIN detalle_pedidos
ON pedidos.id_pedido = detalle_pedidos.id_pedido
JOIN productos
ON detalle_pedidos.id_producto = productos.id_producto
LEFT JOIN canal_pago
ON pedidos.id_pedido = canal_pago.id_pedido
LEFT JOIN envios
ON pedidos.id_pedido = envios.id_pedido;
```

Con esta consulta se puede obtener una visión mucho más completa de las ventas.

---

# 32. Consultas útiles para analizar el e-commerce

Total de ventas:

```sql
SELECT SUM(monto_total) AS ventas_totales
FROM pedidos;
```

Cantidad de pedidos:

```sql
SELECT COUNT(*) AS total_pedidos
FROM pedidos;
```

Venta promedio:

```sql
SELECT AVG(monto_total) AS venta_promedio
FROM pedidos;
```

Ventas por canal:

```sql
SELECT
    canal_venta,
    SUM(monto_total) AS ventas
FROM pedidos
GROUP BY canal_venta
ORDER BY ventas DESC;
```

Ventas por estado:

```sql
SELECT
    estado_pedido,
    SUM(monto_total) AS total
FROM pedidos
GROUP BY estado_pedido;
```

Productos más vendidos:

```sql
SELECT
    productos.nombre_producto,
    SUM(detalle_pedidos.cantidad) AS unidades_vendidas
FROM detalle_pedidos
JOIN productos
ON detalle_pedidos.id_producto = productos.id_producto
GROUP BY productos.id_producto
ORDER BY unidades_vendidas DESC;
```

Clientes con más compras:

```sql
SELECT
    clientes.nombre_completo,
    COUNT(pedidos.id_pedido) AS cantidad_pedidos
FROM clientes
JOIN pedidos
ON clientes.id_cliente = pedidos.id_cliente
GROUP BY clientes.id_cliente
ORDER BY cantidad_pedidos DESC;
```

Clientes que más dinero han gastado:

```sql
SELECT
    clientes.nombre_completo,
    SUM(pedidos.monto_total) AS dinero_gastado
FROM clientes
JOIN pedidos
ON clientes.id_cliente = pedidos.id_cliente
GROUP BY clientes.id_cliente
ORDER BY dinero_gastado DESC;
```

---

# 33. Salir de SQLite

Cuando terminemos de trabajar:

```sql
.quit
```

También se puede utilizar:

```sql
.exit
```

Después volverás a la terminal normal de Codespaces.

---

# 34. Resumen del proceso

En general, el proyecto siguió este proceso:

```text
DATOS ORIGINALES
       ↓
CSV CON DATOS CRUDOS
       ↓
SEPARACIÓN DE LAS 6 TABLAS
       ↓
DATOS SUCIOS
       ↓
LIMPIEZA CON PYTHON + PANDAS
       ↓
DATOS LIMPIOS
       ↓
ARCHIVOS CSV LIMPIOS
       ↓
CARGA CON PYTHON
       ↓
BASE DE DATOS SQLITE
       ↓
ecommerce.db
       ↓
CONSULTAS SQL
       ↓
ANÁLISIS DE LAS VENTAS
```

El resultado final es un proyecto donde los datos pasan desde un archivo original con errores hasta una base de datos organizada y lista para realizar consultas.

Esto permite trabajar no solamente con los datos individuales, sino también analizar la información de clientes, productos, pedidos, detalles, envíos y pagos de manera relacionada.

En otras palabras, el proyecto pasó de tener un conjunto de datos desordenados a tener una estructura organizada, limpia y preparada para ser utilizada en un sistema de información de e-commerce.
