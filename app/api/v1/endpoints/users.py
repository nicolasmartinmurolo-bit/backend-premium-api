from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db  # Importamos la dependencia centralizada
from app.core.security import get_password_hash  # Módulo de hashing (Bcrypt)
from app.models.user import User as UserModel
from app.schemas.user import User, UserCreate

router = APIRouter()

@router.post("/", response_model=User)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    # 1. Verificar si el usuario ya existe por email
    existing_user = db.query(UserModel).filter(UserModel.email == user_in.email).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="El correo electrónico ya está registrado en la base de datos."
        )
    
    # 2. Instanciar el modelo aplicando hashing seguro a la contraseña
    db_user = UserModel(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),  # Hash seguro con Bcrypt
        full_name=user_in.full_name,
        is_active=user_in.is_active
    )
    
    # 3. Guardar en la base de datos con control transaccional seguro
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        print(f"ERROR REAL EN BD: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")

@router.get("/", response_model=List[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(UserModel).offset(skip).limit(limit).all()
    return users