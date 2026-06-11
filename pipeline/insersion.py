import pandas as pd
import numpy as np
import urllib
from sqlalchemy import create_engine, text

# =========================================================================
# 1. CONFIGURACIÓN DE CONEXIÓN A SQL SERVER (WINDOWS)
# =========================================================================
SERVER = "localhost\\SQLEXPRESS"  
DATABASE = "ventas_db"

connection_string = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    f"Trusted_Connection=yes;"
    f"Encrypt=no;"
    f"TrustServerCertificate=yes;"
)

params = urllib.parse.quote_plus(connection_string)
DATABASE_URL = f"mssql+pyodbc:///?odbc_connect={params}"
engine = create_engine(DATABASE_URL)

print("⏳ [ETL] Iniciando el proceso de extracción, transformación y carga...")

# =========================================================================
# 2. EXTRACCIÓN Y LIMPIEZA DE DATOS (PANDAS)
# =========================================================================
try:
    df = pd.read_csv("20260129 data v2 (MaryV).csv")
    print(f"🔹 [Extracción] Dataset cargado correctamente. Registros iniciales: {len(df)}")
except FileNotFoundError:
    print("❌ Error: No se encontró el archivo '20260129 data v2 (MaryV).csv' en la raíz.")
    exit()

# ---- CORRECCIÓN 1: Filtro estricto de nulos en Llave Primaria ----
df = df.dropna(subset=['invoice_id'])
df['invoice_id'] = df['invoice_id'].astype(str).str.strip()

# ---- CORRECCIÓN 2: Eliminar IDs de factura duplicados (Garantiza PK única) ----
df = df.drop_duplicates(subset=['invoice_id'], keep='first')

# ---- A. Estandarización de Fechas (Columna real: issue_date) ----
df['issue_date'] = pd.to_datetime(df['issue_date'], errors='coerce', format='mixed')
df = df.dropna(subset=['issue_date'])

# ---- B. Limpieza de Campos Numéricos ----
for col in ['unit_price', 'total']:
    if df[col].dtype == 'object':
        df[col] = df[col].astype(str).str.replace('$', '', regex=False).str.replace(' ', '', regex=False)
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)

df['qty'] = pd.to_numeric(df['qty'], errors='coerce').fillna(0).astype(int)

# ---- C. Normalización de Clientes ----
df['customer_name'] = df['customer_name'].str.strip().str.upper()
df['customer_id'] = df['customer_id'].str.strip().str.upper()

print(f"✅ [Transformación] Datos depurados. Registros limpios listos para cargar: {len(df)}")

# =========================================================================
# 3. CONSTRUCCIÓN DE LAS DIMENSIONES Y TABLA DE HECHOS (MODELO ESTRELLA)
# =========================================================================

# --- Dimensión Clientes ---
dim_clientes = df[['customer_id', 'customer_name']].drop_duplicates(subset=['customer_id'])
dim_clientes.columns = ['cliente_id', 'nombre_cliente']

# --- Dimensión Tiempo ---
fechas_unicas = pd.Series(df['issue_date'].unique())
dim_tiempo = pd.DataFrame({'fecha_id': fechas_unicas})
dim_tiempo['año'] = dim_tiempo['fecha_id'].dt.year
dim_tiempo['mes_numero'] = dim_tiempo['fecha_id'].dt.month
dim_tiempo['mes'] = dim_tiempo['fecha_id'].dt.strftime('%Y-%m')
dim_tiempo['trimestre'] = dim_tiempo['fecha_id'].dt.quarter

# --- Tabla de Hechos (Ventas) ---
fact_ventas = df[['invoice_id', 'issue_date', 'customer_id', 'item_description', 'qty', 'unit_price', 'total', 'status']].copy()
fact_ventas.columns = ['invoice_id', 'fecha_id', 'cliente_id', 'item_description', 'qty', 'unit_price', 'total', 'status']

# =========================================================================
# 4. CARGA DE DATOS EN ORDEN DE RESTRICCIÓN RELACIONAL
# =========================================================================
print("🔹 [Carga] Conectando a SQL Server e insertando registros...")

try:
    with engine.begin() as conn:
        # Limpieza previa de tablas en orden inverso
        conn.execute(text("DELETE FROM fact_ventas;"))
        conn.execute(text("DELETE FROM dim_clientes;"))
        conn.execute(text("DELETE FROM dim_tiempo;"))
        print(" ➡️ Tablas previas vaciadas (Idempotencia activa).")
        
        print(" ➡️ Insertando registros en dim_clientes...")
        dim_clientes.to_sql('dim_clientes', con=conn, if_exists='append', index=False)
        
        print(" ➡️ Insertando registros en dim_tiempo...")
        dim_tiempo.to_sql('dim_tiempo', con=conn, if_exists='append', index=False)
        
        print(" ➡️ Insertando registros en fact_ventas...")
        fact_ventas.to_sql('fact_ventas', con=conn, if_exists='append', index=False)

    print("🏁 [FIN] ¡El pipeline de ETL se ha ejecutado correctamente! Datos listos en SQL Server.")

except Exception as e:
    print("❌ Ocurrió un error durante la carga a la base de datos:")
    print(str(e))