"""
Esquemas de Validación y Serialización de Datos (Pydantic).
--------------------------------------------------------------------------------
Este archivo define los esquemas de Pydantic para la entidad 'User'. A diferencia 
de los modelos ORM (que estructuran cómo se guardan los datos en la base de datos), 
los esquemas de Pydantic se encargan de validar, serializar y documentar los 
datos que entran a través de las peticiones HTTP (inputs) y los que salen 
hacia el cliente (outputs).
"""

from pydantic import BaseModel, EmailStr
from typing import Optional

# -------------------------------------------------------------------------
# 1. Esquema Base (Propiedades Compartidas)
# -------------------------------------------------------------------------
class UserBase(BaseModel):
    """
    Clase base que agrupa los atributos comunes compartidos entre diferentes 
    operaciones (creación, actualización y lectura). Utiliza tipos opcionales 
    para flexibilidad en las estructuras de datos.
    """
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False  # Campo para identificar privilegios de administrador


# -------------------------------------------------------------------------
# 2. Esquema de Creación de Usuarios (Datos de Entrada / Request Payload)
# -------------------------------------------------------------------------
class UserCreate(UserBase):
    """
    Esquema utilizado estrictamente para validar la información enviada por 
    el cliente al registrar un nuevo usuario mediante una petición POST.
    Hereda de UserBase pero vuelve obligatorios el correo y la contraseña.
    """
    email: EmailStr
    password: str

    # Configuración moderna de Pydantic V2 para inyectar ejemplos visuales 
    # directamente en la documentación interactiva de Swagger UI (/docs).
    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "nico@example.com",
                "full_name": "nico",
                "is_active": True,
                "password": "1234"
            }
        }
    }


# -------------------------------------------------------------------------
# 3. Esquema de Actualización de Datos (Modificación Parcial)
# -------------------------------------------------------------------------
class UserUpdate(UserBase):
    """
    Esquema para modificar registros existentes. Permite actualizar opcionalmente 
    cualquier campo, incluyendo la posibilidad de cambiar el password de forma independiente.
    """
    password: Optional[str] = None


# -------------------------------------------------------------------------
# 4. Esquema Base de Datos / Conversión de ORM (from_attributes)
# -------------------------------------------------------------------------
class UserInDBBase(UserBase):
    """
    Esquema intermedio que incorpora el identificador único (ID) generado por PostgreSQL.
    'from_attributes = True' (conocido como orm_mode en versiones anteriores de Pydantic) 
    es la propiedad clave que le permite a Pydantic leer datos directamente desde 
    los objetos ORM de SQLAlchemy y serializarlos como diccionarios o JSON.
    """
    id: Optional[int] = None

    class Config:
        from_attributes = True


# -------------------------------------------------------------------------
# 5. Esquema Final de Respuesta (Data Output / Response Model)
# -------------------------------------------------------------------------
class User(UserInDBBase):
    """
    Esquema final devuelto al cliente en las respuestas HTTP (como al consultar 
    el perfil /me o listar usuarios). Hereda de UserInDBBase y asegura que nunca 
    se exponga el campo 'hashed_password' en las respuestas de la API.
    """
    pass