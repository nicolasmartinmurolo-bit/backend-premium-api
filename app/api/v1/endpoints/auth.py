"""
Endpoints de Autenticación y Login (OAuth2).
--------------------------------------------------------------------------------
Este módulo expone las rutas públicas relacionadas con la acreditación de identidad. 
Su función principal es recibir las credenciales del usuario (correo y contraseña), 
verificar su autenticidad contra la base de datos y emitir un token JWT cifrado 
que servirá como pase de acceso para las rutas protegidas de la API.
"""

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.config import settings
from app.core.security import verify_password, create_access_token
from app.models.user import User as UserModel
from app.schemas.token import Token

# -------------------------------------------------------------------------
# 1. Definición del Enrutador (Router)
# -------------------------------------------------------------------------
# Instanciamos APIRouter para agrupar todas las rutas de autenticación 
# y permitir que el enrutador principal (api_router) las registre de forma modular.
router = APIRouter()

def get_db():
    """
    Dependencia local para abrir y cerrar sesiones de base de datos 
    durante el proceso de autenticación.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------------------------------------------------------
# 2. Endpoint de Autenticación y Emisión de Tokens (Login)
# -------------------------------------------------------------------------
@router.post("/login/access-token", response_model=Token)
def login_access_token(
    db: Session = Depends(get_db), 
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    Endpoint compatible con OAuth2 para el inicio de sesión.
    - Recibe un formulario estándar (OAuth2PasswordRequestForm) donde el campo 
      'username' corresponde al correo electrónico del usuario y 'password' a su clave.
    - Retorna un token de acceso cifrado (JWT) junto con su tipo (bearer).
    """
    
    # Paso 1: Buscar al usuario en PostgreSQL utilizando su correo electrónico.
    # Nota: OAuth2PasswordRequestForm almacena el identificador en la propiedad 'username'.
    user = db.query(UserModel).filter(UserModel.email == form_data.username).first()
    
    # Paso 2: Verificar la existencia del usuario y la validez de la contraseña.
    # Comparamos la contraseña en texto plano con el hash seguro guardado usando bcrypt.
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )
    
    # Paso 3: Validar que el estado de la cuenta del usuario se encuentre activo.
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )
    
    # Paso 4: Configurar el tiempo de vida útil del token de acceso 
    # utilizando los parámetros globales definidos en el archivo .env y config.py.
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Paso 5: Generar y retornar el token JWT incluyendo el email como identificador (subject 'sub').
    return {
        "access_token": create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }