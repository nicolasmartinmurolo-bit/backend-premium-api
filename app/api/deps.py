"""
Módulo de Inyección de Dependencias y Seguridad (Autenticación y Roles).
--------------------------------------------------------------------------------
Este archivo agrupa las funciones de dependencia fundamentales utilizadas 
para proteger los endpoints de la API:
1. Configuración del esquema OAuth2 para la extracción de tokens Bearer.
2. Validador de identidad mediante tokens JWT (get_current_user).
3. Validador de privilegios de administrador / superusuario (get_current_active_superuser).
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db  # <--- Importamos la única fuente oficial de get_db
from app.models.user import User as UserModel
from app.schemas.token import TokenData

# -------------------------------------------------------------------------
# 1. Esquema de Seguridad OAuth2 (Token Bearer)
# -------------------------------------------------------------------------
# OAuth2PasswordBearer le indica a FastAPI dónde debe buscar el token en las 
# peticiones entrantes. Apunta directamente a la ruta de login (/api/v1/login/access-token)
# para que Swagger UI sepa cómo y dónde autenticarse automáticamente.
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


# -------------------------------------------------------------------------
# 2. Dependencia de Usuario Actual (Autenticación por JWT)
# -------------------------------------------------------------------------
def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> UserModel:
    """
    Intercepta la petición HTTP, extrae y valida el token JWT recibido en los headers.
    Retorna el objeto del usuario autenticado si el token es válido y el usuario existe.
    Lanza una excepción HTTP 401 (Unauthorized) si algo falla.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decodificamos el token usando la clave secreta y el algoritmo global
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")  # 'sub' (subject) almacena el email del usuario
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        # Si el token expiró, fue alterado o es inválido, explota aquí
        raise credentials_exception
        
    # Buscamos al usuario en la base de datos PostgreSQL mediante su email
    user = db.query(UserModel).filter(UserModel.email == token_data.email).first()
    if user is None:
        raise credentials_exception
        
    # Validamos adicionalmente que la cuenta del usuario se encuentre activa
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
        
    return user


# -------------------------------------------------------------------------
# 3. Dependencia de Control de Acceso por Roles (Superusuario)
# -------------------------------------------------------------------------
def get_current_active_superuser(
    current_user: UserModel = Depends(get_current_user),
) -> UserModel:
    """
    Capa de autorización superior. Toma al usuario ya autenticado (gracias a get_current_user) 
    y evalúa si cuenta con privilegios de administrador (is_superuser = True).
    Si no es administrador, bloquea el acceso lanzando un error HTTP 403 (Forbidden).
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="El usuario no cuenta con privilegios de administrador."
        )
    return current_user