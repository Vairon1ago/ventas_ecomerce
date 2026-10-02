import subprocess
import sys

procesos = [
    "Scripts/limpiar_datos.py",
    "Scripts/separar_limpios.py",
    "Scripts/limpiar_datos_2.py",
    "Scripts/limpiar_tablas.py",
    "Scripts/crear_base_datos.py"
]

print()
print("       PROCESO COMPLETO E-COMMERCE")
print()

for proceso in procesos:

    print()
    print("Ejecutando:", proceso)
    print("----------------------------------------------")

    resultado = subprocess.run(
        [sys.executable, proceso]
    )

    if resultado.returncode != 0:

        print()
        print("          PROCESO DETENIDO")
        print()
        print("Error en:")
        print(proceso)

        sys.exit(resultado.returncode)

print()
print("       PROCESO FINALIZADO CORRECTAMENTE")
print()
print("Archivo original:")
print("Scr/Entrada_de_datos/")
print()
print("Archivos separados:")
print("Scr/Archivos_sucios/")
print()
print("Archivos limpios:")
print("Scr/Archivos_limpios/")
print()
print("Base de datos:")
print("Scr/Base_de_datos/ecommerce.db")