"""
Enrutador Central de la Versión 1 de la API (API Router).
--------------------------------------------------------------------------------
Este archivo implementa el patrón de diseño de enrutamiento modular. 
Su propósito es centralizar y agrupar todos los sub-routers específicos del 
sistema (como gestión de usuarios, autenticación, etc.) bajo un único enrutador 
general (`api_router`). Esto evita saturar el archivo principal (`main.py`) 
con múltiples importaciones y facilita la escalabilidad limpia del proyecto.
"""

from fastapi import APIRouter
from app.api.v1.endpoints import users, auth

# -------------------------------------------------------------------------
# 1. Instanciación del Enrutador Central de Versión
# -------------------------------------------------------------------------
# Creamos el objeto APIRouter general para esta versión de la API (v1).
api_router = APIRouter()


# -------------------------------------------------------------------------
# 2. Registro e Inclusión de Sub-Routers Modulares
# -------------------------------------------------------------------------

# Incluimos el router del módulo de usuarios:
# - prefix="/users": Todas las rutas definidas en 'users.py' colgarán de este prefijo (ej: /users/).
# - tags=["users"]: Agrupa visualmente estos endpoints bajo la sección "users" en Swagger UI.
api_router.include_router(users.router, prefix="/users", tags=["users"])

# Incluimos el router del módulo de autenticación (login):
# - No requiere un prefijo adicional ya que sus rutas (como /login/access-token) se definen de forma explícita.
# - tags=["login"]: Organiza el bloque de inicio de sesión bajo la etiqueta correspondiente en la documentación.
api_router.include_router(auth.router, tags=["login"])