"""
Módulo de Seguridad, Cifrado y Autenticación por Tokens (Bcrypt y JWT).
--------------------------------------------------------------------------------
Este archivo concentra toda la lógica criptográfica de la aplicación:
1. El hashing unidireccional de contraseñas utilizando la librería 'bcrypt' 
   de forma directa (evitando conflictos de compatibilidad).
2. La generación, firma y validación de tokens digitales (JSON Web Tokens - JWT) 
   utilizados para implementar una autenticación sin estado (stateless).
"""

import bcrypt
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from app.core.config import settings

# -------------------------------------------------------------------------
# 1. Funciones de Hashing y Verificación de Contraseñas (Bcrypt)
# -------------------------------------------------------------------------

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si una contraseña en texto plano ingresada por el usuario 
    coincide con el hash seguro almacenado en la base de datos.
    Retorna True si son idénticas o False en caso contrario.
    """
    return bcrypt.checkpw(
        plain_password.encode('utf-8'), 
        hashed_password.encode('utf-8')
    )

def get_password_hash(password: str) -> str:
    """
    Genera un hash criptográfico irreversible de la contraseña utilizando bcrypt.
    
    Nota de seguridad: Bcrypt tiene una limitación nativa de 72 bytes máximos.
    Por ello, convertimos el texto a bytes y aplicamos un corte preventivo a los 
    primeros 72 bytes si la contraseña es excesivamente larga, evitando errores de sistema.
    """
    pwd_bytes = password.encode('utf-8')
    if len(pwd_bytes) > 72:
        pwd_bytes = pwd_bytes[:72]
        
    # Generamos la semilla aleatoria (salt) y aplicamos el hash con bcrypt
    hashed = bcrypt.hashpw(pwd_bytes, bcrypt.gensalt())
    return hashed.decode('utf-8')


# -------------------------------------------------------------------------
# 2. Generación de Tokens de Acceso (JSON Web Tokens - JWT)
# -------------------------------------------------------------------------

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Genera un token JWT firmado digitalmente para autenticar al usuario en peticiones futuras.
    
    Parámetros:
    - data: Diccionario con la carga útil o 'payload' (ej: {"sub": user.email}).
    - expires_delta: Tiempo de vida opcional para el token. Si no se provee, 
      utiliza por defecto el valor configurado en ACCESS_TOKEN_EXPIRE_MINUTES.
    """
    to_encode = data.copy()
    
    # Determinamos el tiempo exacto de expiración (ahora + delta de tiempo)
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Inyectamos la fecha de expiración estándar ('exp') dentro del payload del token
    to_encode.update({"exp": expire})
    
    # Codificamos el token usando la clave secreta global y el algoritmo de firma (ej. HS256)
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    return encoded_jwt