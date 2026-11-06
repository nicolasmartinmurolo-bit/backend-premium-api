"""
Módulo de Configuración y Entorno de Migraciones (Alembic Environment).
--------------------------------------------------------------------------------
Este archivo es ejecutado por Alembic cada vez que se corre un comando de migración 
(como 'alembic revision --autogenerate' o 'alembic upgrade head').
Sus funciones principales son:
1. Cargar la configuración general desde el archivo 'alembic.ini'.
2. Importar la Base declarativa y los modelos ORM de SQLAlchemy para que Alembic 
   pueda compararlos contra el estado actual de la base de datos real (PostgreSQL).
3. Configurar y ejecutar las migraciones tanto en modo offline (generación de scripts SQL) 
   como en modo online (conexión directa y ejecución sobre la base de datos).
"""

from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# -------------------------------------------------------------------------
# 1. Configuración Inicial de Alembic y Logs
# -------------------------------------------------------------------------
# Objeto de configuración de Alembic que provee acceso a las propiedades 
# definidas en el archivo 'alembic.ini' (incluyendo la URL de conexión a la BD).
config = context.config

# Interpretación y configuración del sistema de logs de Python para Alembic.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# -------------------------------------------------------------------------
# 2. Vinculación de Modelos ORM para Autogeneración (Target Metadata)
# -------------------------------------------------------------------------
# Importamos la 'Base' y los modelos de la aplicación (como User).
# Esto es vital: le permite a Alembic inspeccionar los modelos de Python y 
# detectar automáticamente si se agregaron, modificaron o eliminaron tablas o columnas.
from app.core.database import Base
from app.models.user import User  # Importación explícita para asegurar el registro en el ORM

# Asignamos los metadatos de SQLAlchemy a target_metadata.
# Gracias a esto, Alembic sabe qué estructura debe tener la base de datos real.
target_metadata = Base.metadata


# -------------------------------------------------------------------------
# 3. Ejecución de Migraciones en Modo Offline
# -------------------------------------------------------------------------
def run_migrations_offline() -> None:
    """
    Ejecuta las migraciones en modo 'offline'.
    En este escenario, Alembic genera las sentencias SQL puras en texto 
    sin necesidad de conectarse activamente a un motor de base de datos (DBAPI).
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# -------------------------------------------------------------------------
# 4. Ejecución de Migraciones en Modo Online (Conexión Activa a PostgreSQL)
# -------------------------------------------------------------------------
def run_migrations_online() -> None:
    """
    Ejecuta las migraciones en modo 'online' (el modo habitual).
    Crea una instancia activa del motor de base de datos utilizando la URL 
    del archivo .ini/.env y abre una conexión transaccional para aplicar 
    los cambios directamente sobre PostgreSQL.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


# -------------------------------------------------------------------------
# 5. Selector de Modo de Ejecución
# -------------------------------------------------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()