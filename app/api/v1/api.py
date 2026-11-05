from fastapi import APIRouter
from app.api.v1.endpoints import users

api_router = APIRouter()

# Incluimos el router de usuarios con su prefijo y etiqueta para Swagger
api_router.include_router(users.router, prefix="/users", tags=["users"])