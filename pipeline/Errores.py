import pandas as pd
import sys

# Definimos el nombre del archivo
archivo_csv = "20260129 data v2 (MaryV).csv"

print("--- INICIANDO PROCESAMIENTO ---")

# Controlamos la excepción al momento de leer el archivo
try:
    # Agregamos encoding='latin1' para resolver el UnicodeDecodeError de los sistemas legados
    df = pd.read_csv(archivo_csv, encoding='latin1')
    print(f"✔️ Archivo '{archivo_csv}' cargado exitosamente.\n")

except FileNotFoundError:
    print(f"❌ Error: El archivo '{archivo_csv}' no existe en esta carpeta.")
    sys.exit(1)  # Termina el programa de forma limpia con código de error

except UnicodeDecodeError as e:
    print(f"❌ Error de codificación: El archivo no es UTF-8 ni Latin1. Detalles: {e}")
    sys.exit(1)

except Exception as e:
    print(f"❌ Ocurrió un error inesperado al leer el archivo: {e}")
    sys.exit(1)


# --- SI LA LECTURA FUE EXITOSA, CONTINÚA EL PROGRAMA ---

print("--- 1. ESTRUCTURA GENERAL ---")
print(df.info())

print("\n--- 2. CONTEO DE VALORES NULOS ---")
print(df.isnull().sum())

print("\n--- 3. PROCESAMIENTO Y DETECCIÓN DE ERRORES EN FECHAS ---")
# Ajustamos la columna según el CSV real: 'issue_date'
if 'issue_date' in df.columns:
    fechas_convertidas = pd.to_datetime(df['issue_date'], errors='coerce', format='mixed')
    valores_invalidos_fecha = df[fechas_convertidas.isna()]['issue_date'].unique()
    print(f"Muestra de valores de fecha inválidos: {valores_invalidos_fecha[:10]}")
    
    df['fecha_estandar'] = fechas_convertidas.dt.strftime('%Y-%m-%d')
    print(f"-> Fechas procesadas. Nulos en fechas: {df['fecha_estandar'].isna().sum()}")
else:
    print("⚠️ No se encontró la columna 'issue_date'.")

print("\n--- 4. DETECTANDO ERRORES EN CAMPOS NUMÉRICOS ---")
# Ajustamos a la columna real del CSV: 'total' o 'unit_price'
columna_numerica = 'total'
if columna_numerica in df.columns:
    valores_no_numericos = df[pd.to_numeric(df[columna_numerica], errors='coerce').isna()][columna_numerica].unique()
    print(f"Caracteres extraños encontrados en '{columna_numerica}': {valores_no_numericos[:10]}")

print("\n--- 5. REVISANDO DUPLICADOS ---")
print(f"Cantidad de filas totalmente duplicadas: {df.duplicated().sum()}")

print("\n--- FIN DEL PROGRAMA EN FORMA EXITOSA ---")