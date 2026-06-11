import urllib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Configuración del servidor y base de datos según tus capturas
SERVER_NAME = "localhost\\SQLEXPRESS"  
DATABASE_NAME = "ventas_db"

# Cadena de conexión para Autenticación de Windows
connection_string = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={SERVER_NAME};"
    f"DATABASE={DATABASE_NAME};"
    f"Trusted_Connection=yes;"
    f"Encrypt=no;"
)

# Codificación segura para SQLAlchemy
params = urllib.parse.quote_plus(connection_string)
DATABASE_URL = f"mssql+pyodbc:///?odbc_connect={params}"

# Inicialización del motor
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependencia para abrir/cerrar conexiones
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()