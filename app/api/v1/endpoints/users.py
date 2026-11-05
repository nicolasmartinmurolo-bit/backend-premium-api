from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import SessionLocal
from app.models.user import User as UserModel
from app.schemas.user import User, UserCreate

router = APIRouter()

# Dependencia para obtener la sesión de base de datos por cada request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=User)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = UserModel(
            email=user_in.email,
            hashed_password=user_in.password,
            full_name=user_in.full_name,
            is_active=user_in.is_active
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        print(f"ERROR REAL EN BD: {str(e)}") # <--- Esto aparecerá en rojo en tu terminal de uvicorn
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")

@router.get("/", response_model=List[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(UserModel).offset(skip).limit(limit).all()
    return users