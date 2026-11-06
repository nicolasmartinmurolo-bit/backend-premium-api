"""
Esquemas de Validación y Serialización para Autenticación (Tokens JWT).
--------------------------------------------------------------------------------
Este módulo define los esquemas de Pydantic específicos para el manejo de 
la sesión y los tokens de acceso:
1. 'Token': Estructura del JSON de respuesta que recibe el cliente tras un login exitoso.
2. 'TokenData': Estructura de la carga útil interna (payload) utilizada para extraer 
   el identificador del usuario (email) durante la validación del token.
"""

from pydantic import BaseModel
from typing import Optional

# -------------------------------------------------------------------------
# 1. Esquema de Respuesta del Token de Acceso (Token Output)
# -------------------------------------------------------------------------
class Token(BaseModel):
    """
    Define el esquema exacto que la API devuelve al cliente cuando las credenciales 
    de inicio de sesión son correctas (en el endpoint /login/access-token).
    - access_token: El JWT firmado digitalmente que el cliente usará como pase.
    - token_type: El tipo de token (estándar OAuth2, generalmente 'bearer').
    """
    access_token: str
    token_type: str


# -------------------------------------------------------------------------
# 2. Esquema de Datos del Token (Payload / TokenData)
# -------------------------------------------------------------------------
class TokenData(BaseModel):
    """
    Define la estructura interna de los datos extraídos y validados desde el payload 
    del token JWT (típicamente el campo 'sub' que almacena el correo electrónico).
    Se utiliza en las dependencias de seguridad para buscar al usuario en la base de datos.
    """
    email: Optional[str] = None