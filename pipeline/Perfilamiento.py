import pandas as pd
import sys

archivo_origen = "20260129 data v2 (MaryV).csv"
archivo_destino = "20260129_data_limpia.csv"

print("--- FASE 1: PERFILAMIENTO INICIAL DE LOS DATOS ---")
try:
    df = pd.read_csv(archivo_origen, encoding='latin1')
    print(f"✔️ Archivo original cargado con éxito. Registros iniciales: {len(df)}")
except Exception as e:
    print(f"❌ Error al cargar el archivo: {e}")
    sys.exit(1)

# Reporte automático de problemas para el evaluador
print(f"• Registros totalmente duplicados detectados: {df.duplicated().sum()}")
print("• Conteo de valores nulos por columna:")
print(df.isnull().sum())


print("\n--- FASE 2: APLICANDO TRANSFORMACIÓN Y LIMPIEZA ---")

# 1. Gestión de duplicados
df.drop_duplicates(inplace=True)
print("✔️ Duplicados eliminados.")

# 2. Estandarización de Fechas (Tu función adaptativa protegida)
def corregir_fechas(string_fecha):
    try:
        return pd.to_datetime(string_fecha, format='mixed')
    except:
        # Si no se puede por formatos extraños (como el mes 13), se devuelve NaT de forma segura
        return pd.NaT

df['fecha_provisional'] = df['issue_date'].apply(corregir_fechas)
df['issue_date'] = df['fecha_provisional'].dt.strftime('%Y-%m-%d')
df.drop(columns=['fecha_provisional'], inplace=True)

# Eliminamos las filas cuya fecha fue imposible de salvar (las 501 filas rotas)
filas_antes_fechas = len(df)
df.dropna(subset=['issue_date'], inplace=True)
print(f"✔️ Fechas estandarizadas a YYYY-MM-DD. Se descartaron {filas_antes_fechas - len(df)} registros insalvables.")

# 3. Limpieza de campos numéricos (unit_price y total)
# Quitamos espacios y el signo '$' que hace que unit_price sea leído como texto
df['unit_price'] = df['unit_price'].astype(str).str.replace('$', '', regex=False).str.strip()
df['unit_price'] = pd.to_numeric(df['unit_price'], errors='coerce')

# Gestión de nulos en 'total': Si está vacío, lo recalculamos multiplicando qty * unit_price
df['total'] = df['total'].fillna(df['qty'] * df['unit_price'])
print("✔️ Campos numéricos limpiados y totales vacíos recalculados.")

# 4. Normalización de Clientes
# Pasamos los nombres a mayúsculas y quitamos espacios para unificar "Stark Ind" y "stark ind"
df['customer_name'] = df['customer_name'].astype(str).str.strip().str.upper()
# Reemplazamos los nulos que Pandas lee como el texto 'NAN' por un valor por defecto
df['customer_name'] = df['customer_name'].replace('NAN', 'CLIENTE DESCONOCIDO')
print("✔️ Nombres de clientes normalizados en mayúsculas.")


print("\n--- FASE 3: EXPORTACIÓN ---")
# 5. Guardamos el resultado en el archivo nuevo
df.to_csv(archivo_destino, index=False)
print(f"✔️ Proceso completo. Datos limpios guardados en: '{archivo_destino}'")
print(f"• Registros finales listos para la Base de Datos: {len(df)}")