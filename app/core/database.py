"""
Módulo de Conexión y Gestión de Base de Datos (SQLAlchemy).
--------------------------------------------------------------------------------
Este archivo se encarga de establecer la comunicación con la base de datos 
relacional (PostgreSQL), configurar el motor de ejecución (Engine), crear la 
fábrica de sesiones (SessionLocal) y proveer la función de inyección de 
dependencias para manejar el ciclo de vida de las sesiones en cada petición HTTP.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings

# -------------------------------------------------------------------------
# 1. Normalización y Validación de la URL de Conexión
# -------------------------------------------------------------------------
# Obtenemos la URL de la base de datos desde las configuraciones globales.
db_url = settings.DATABASE_URL

# Validación de seguridad defensiva: si la URL utiliza el prefijo genérico 
# 'postgresql://' pero no especifica explícitamente el driver de psycopg2, 
# se realiza un reemplazo automático para evitar errores de compatibilidad con SQLAlchemy.
if "postgresql://" in db_url and "psycopg2" not in db_url:
    db_url = db_url.replace("postgresql://", "postgresql+psycopg2://")

# -------------------------------------------------------------------------
# 2. Creación del Motor de Base de Datos (Engine)
# -------------------------------------------------------------------------
try:
    # create_engine es el punto central de conexión de SQLAlchemy.
    # 'connect_args' se utiliza para pasar parámetros específicos del driver a nivel 
    # de conexión en bruto, como un tiempo límite (timeout) de 5 segundos para evitar 
    # que el servidor se quede bloqueado indefinidamente si la base de datos no responde.
    engine = create_engine(
        db_url,
        connect_args={"connect_timeout": 5}
    )
    print("LOG: Motor de Base de Datos configurado correctamente.")
except Exception as e:
    # Capturamos cualquier error crítico al intentar inicializar el motor y lo relanzamos 
    # para detener el inicio de la aplicación si no hay acceso a los datos.
    print(f"LOG ERROR: Falló la creación del motor de BD: {e}")
    raise e

# -------------------------------------------------------------------------
# 3. Configuración de Sesiones y Modelos ORM
# -------------------------------------------------------------------------

# Fábrica de sesiones (SessionLocal):
# Cada instancia de SessionLocal representará una "sesión de trabajo" temporal 
# con la base de datos. Desactivamos autocommit y autoflush para mantener un 
# control manual y transaccional estricto de los cambios (commits y rollbacks).
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa:
# Clase constructora de la cual heredarán todos nuestros modelos ORM (como User).
# Permite mapear clases de Python directamente a tablas relacionales en la base de datos.
Base = declarative_base()

# -------------------------------------------------------------------------
# 4. Inyección de Dependencias (Ciclo de Vida de la Sesión)
# -------------------------------------------------------------------------
def get_db():
    """
    Dependencia global generadora (Generator).
    Se encarga de abrir una nueva sesión de base de datos para cada petición HTTP 
    que la requiera, entregándola mediante 'yield', y garantizando su cierre 
    automático en el bloque 'finally' (incluso si ocurren errores durante la ejecución).
    Esto previene fugas de memoria y conexiones colgadas en el servidor.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()