import pandas as pd
import os
import sys

archivo_csv = "datos.csv"
ruta_script = os.path.dirname(os.path.abspath(__file__))
ruta_archivo = os.path.join(ruta_script, archivo_csv)

print("Explorador de CSV - Carga automática desde la carpeta del script\n")

if not os.path.isfile(ruta_archivo):
    print(f"ERROR: No se encontró el archivo '{archivo_csv}'")
    print(f"Ruta esperada: {ruta_archivo}")
    sys.exit(1)

try:
    try:
        df = pd.read_csv(ruta_archivo, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(ruta_archivo, encoding='latin-1')

    print(f"\nArchivo '{archivo_csv}' cargado correctamente.\n")
    print("Vista previa del contenido:")
    print(df.head(), "\n")

    print("Información general:")
    df.info()
    print("\n")

    print("Estadísticas descriptivas:")
    print(df.describe(include='all'))

except Exception as e:
    print("\nOcurrió un error al leer el archivo:")
    print(str(e))

