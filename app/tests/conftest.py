"""
Configuración Global de Pruebas Automatizadas (Pytest Fixtures).
--------------------------------------------------------------------------------
Este módulo configura el entorno de pruebas para la API utilizando una base de datos 
en memoria (SQLite) con un aislamiento total por cada función de test. 
Sus componentes principales son:
1. Creación de un motor de SQLite en memoria optimizado para pruebas concurrentes.
2. Una fixture ('db_session') que levanta un esquema limpio antes de cada test y lo destruye al finalizar.
3. Una fixture ('client') que sobrescribe la dependencia de la base de datos de producción 
   (get_db) para inyectar la sesión de pruebas mediante el TestClient de FastAPI.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import Base, get_db
from app.models.user import User  # <--- Importante: Necesario para que Base reconozca la tabla users y sus metadatos.

# -------------------------------------------------------------------------
# 1. Configuración de la Base de Datos de Pruebas (SQLite en memoria)
# -------------------------------------------------------------------------
# Usamos una base de datos SQLite efímera en la memoria RAM ("sqlite:///:memory:")
# junto con 'StaticPool' para garantizar que todas las conexiones compartan la misma 
# instancia aislada durante la ejecución de los tests.
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# -------------------------------------------------------------------------
# 2. Fixture de Sesión de Base de Datos por Test
# -------------------------------------------------------------------------
@pytest.fixture(scope="function")
def db_session():
    """
    Crea un ciclo de vida de base de datos limpio para cada prueba individual:
    - Antes de ejecutar el test, genera todas las tablas en la memoria RAM.
    - Entrega la sesión activa mediante 'yield'.
    - Al terminar, destruye todas las tablas para evitar contaminación entre pruebas.
    """
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


# -------------------------------------------------------------------------
# 3. Fixture del Cliente de Pruebas HTTP (TestClient Override)
# -------------------------------------------------------------------------
@pytest.fixture(scope="function")
def client(db_session):
    """
    Configura el cliente HTTP de pruebas para FastAPI:
    - Sobrescribe la dependencia oficial 'get_db' para que redirija las consultas 
      hacia nuestra base de datos temporal en memoria ('db_session').
    - Instancia un TestClient conectado a la aplicación principal.
    - Limpia las sobreescrituras (dependency_overrides) al finalizar.
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as c:
        yield c
        
    app.dependency_overrides.clear()