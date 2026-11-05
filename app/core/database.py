from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings

# Verificamos que la URL use explícitamente psycopg2
db_url = settings.DATABASE_URL
if "postgresql://" in db_url and "psycopg2" not in db_url:
    db_url = db_url.replace("postgresql://", "postgresql+psycopg2://")

try:
    # El connect_timeout se pasa correctamente dentro de connect_args
    engine = create_engine(
        db_url,
        connect_args={"connect_timeout": 5}
    )
    print("LOG: Motor de Base de Datos configurado correctamente.")
except Exception as e:
    print(f"LOG ERROR: Falló la creación del motor de BD: {e}")
    raise e

# Fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa para los modelos ORM
Base = declarative_base()

# Dependencia global para inyectar la sesión en los endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()