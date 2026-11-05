"""
Endpoints de Gestión de Usuarios (CRUD y Perfil).
--------------------------------------------------------------------------------
Este módulo concentra las rutas HTTP destinadas a la administración de usuarios:
1. Registro de nuevos usuarios (POST /) con cifrado automático de contraseñas.
2. Listado general de usuarios (GET /) protegido exclusivamente para administradores.
3. Consulta de perfil propio (GET /me) validando la identidad mediante el token JWT.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db  # Dependencia centralizada de sesión de base de datos
from app.core.security import get_password_hash
from app.models.user import User as UserModel
from app.schemas.user import User, UserCreate
from app.api.deps import get_current_user, get_current_active_superuser

# -------------------------------------------------------------------------
# 1. Definición del Enrutador de Usuarios
# -------------------------------------------------------------------------
router = APIRouter()


# -------------------------------------------------------------------------
# 2. Endpoint de Registro de Usuarios (Create / POST)
# -------------------------------------------------------------------------
@router.post("/", response_model=User)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    Registra un nuevo usuario en la base de datos:
    - Valida que el correo electrónico no esté previamente registrado.
    - Toma la contraseña en texto plano y genera su hash seguro con bcrypt.
    - Almacena el registro en PostgreSQL de forma transaccional (commit/rollback).
    """
    
    # Paso 1: Verificamos si ya existe un usuario con el mismo email en la base de datos.
    existing_user = db.query(UserModel).filter(UserModel.email == user_in.email).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="El correo electrónico ya está registrado en la base de datos."
        )
    
    # Paso 2: Creamos una instancia del modelo ORM User con los datos validados por Pydantic.
    # Nota clave: La contraseña NUNCA se guarda en texto plano; se usa get_password_hash().
    db_user = UserModel(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        full_name=user_in.full_name,
        is_active=user_in.is_active,
        is_superuser=user_in.is_superuser
    )
    
    # Paso 3: Intentamos guardar los cambios en la base de datos de forma segura (Transacción).
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)  # Actualiza la instancia con el ID generado automáticamente por la BD.
        return db_user
    except Exception as e:
        # Si ocurre cualquier fallo inesperado, revertimos la transacción para no corromper la BD.
        db.rollback()
        print(f"ERROR REAL EN BD: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")


# -------------------------------------------------------------------------
# 3. Endpoint de Listado de Usuarios (Read / GET Protegido para Admins)
# -------------------------------------------------------------------------
@router.get("/", response_model=List[User])
def read_users(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_active_superuser) # Capa de seguridad: Solo Admins
):
    """
    Retorna una lista paginada de todos los usuarios registrados.
    - Utiliza 'skip' y 'limit' para implementar paginación eficiente.
    - Requiere obligatoriamente que el usuario que hace la petición tenga el rol 
      de superusuario (is_superuser = True), validado mediante la dependencia de seguridad.
    """
    users = db.query(UserModel).offset(skip).limit(limit).all()
    return users


# -------------------------------------------------------------------------
# 4. Endpoint de Consulta de Perfil Propio (Read / GET /me)
# -------------------------------------------------------------------------
@router.get("/me", response_model=User)
def read_users_me(current_user: UserModel = Depends(get_current_user)):
    """
    Obtiene los datos del usuario actual autenticado mediante el token JWT.
    - La dependencia 'get_current_user' intercepta el token Bearer, verifica su validez 
      y extrae automáticamente el objeto usuario correspondiente de la base de datos.
    """
    return current_user