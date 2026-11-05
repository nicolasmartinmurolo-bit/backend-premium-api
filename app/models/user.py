"""
Modelo ORM de la Tabla de Usuarios (SQLAlchemy).
--------------------------------------------------------------------------------
Este archivo define la estructura relacional de la entidad 'User' utilizando 
SQLAlchemy ORM (Object-Relational Mapping). Cada clase aquí mapea directamente 
una tabla en la base de datos PostgreSQL, permitiendo manipular registros 
mediante objetos de Python en lugar de escribir consultas SQL manuales.
"""

from sqlalchemy import Column, Integer, String, Boolean
from app.core.database import Base

class User(Base):
    """
    Clase modelo que representa la tabla física 'users' en la base de datos.
    Hereda de 'Base' (creada en database.py), lo que le indica a SQLAlchemy 
    que esta clase es una entidad mapeada y debe ser rastreada por el sistema.
    """
    
    # Nombre exacto de la tabla en la base de datos PostgreSQL
    __tablename__ = "users"

    # -------------------------------------------------------------------------
    # Definición de Columnas y Restricciones (Constraints)
    # -------------------------------------------------------------------------
    
    # Identificador único (Primary Key). 'index=True' crea un índice en la BD 
    # para acelerar las búsquedas basadas en el ID.
    id = Column(Integer, primary_key=True, index=True)
    
    # Correo electrónico del usuario. 
    # - unique=True: Garantiza que no existan dos usuarios con el mismo email.
    # - index=True: Mejora drásticamente la velocidad al buscar usuarios por email en los logins.
    # - nullable=False: Restricción estricta de que el campo es obligatorio.
    email = Column(String, unique=True, index=True, nullable=False)
    
    # Contraseña cifrada (Hash generado por bcrypt). 
    # Nunca se guarda la contraseña en texto plano por seguridad.
    hashed_password = Column(String, nullable=False)
    
    # Nombre completo del usuario. Es opcional (nullable=True).
    full_name = Column(String, nullable=True)
    
    # Estado de la cuenta. Por defecto inicia en True (activo). 
    # Permite desactivar usuarios sin necesidad de borrarlos físicamente.
    is_active = Column(Boolean, default=True)
    
    # Indicador de privilegios de administrador (Superusuario).
    # Por defecto es False, permitiendo restringir rutas críticas solo a admins.
    is_superuser = Column(Boolean, default=False)