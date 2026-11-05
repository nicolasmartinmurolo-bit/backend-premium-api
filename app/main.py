"""
Punto de Entrada Principal de la Aplicación (FastAPI Server Entrypoint).
--------------------------------------------------------------------------------
Este archivo es lo primero que lee el servidor (Uvicorn) al arrancar la aplicación.
Sus responsabilidades principales son:
1. Instanciar el objeto principal de FastAPI utilizando los metadatos globales.
2. Configurar la ruta base de la documentación interactiva (Swagger UI).
3. Montar y registrar el enrutador general de la API (api_router) que agrupa 
   todos los sub-módulos (usuarios, autenticación, etc.).
4. Exponer una ruta raíz (health check / root) para verificar que el servicio responde.
"""

from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.api import api_router

# -------------------------------------------------------------------------
# 1. Instanciación y Configuración del Servidor FastAPI
# -------------------------------------------------------------------------
# Creamos la aplicación principal. 
# - title: Extrae el nombre del proyecto desde las configuraciones globales.
# - openapi_url: Define la ruta donde se genera el esquema JSON de la API 
#   para alimentar de forma dinámica la interfaz interactiva de Swagger UI.
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# -------------------------------------------------------------------------
# 2. Montaje del Enrutador General de la API (Versionado)
# -------------------------------------------------------------------------
# Conectamos el enrutador central de la versión 1 (api_router) aplicando 
# el prefijo global (ej. /api/v1). 
# Gracias a esto, cualquier sub-ruta (como /users o /login) heredará automáticamente 
# dicho prefijo sin necesidad de modificar el main.
app.include_router(api_router, prefix=settings.API_V1_STR)


# -------------------------------------------------------------------------
# 3. Ruta Raíz / Verificación de Estado (Health Check)
# -------------------------------------------------------------------------
@app.get("/")
def root():
    """
    Endpoint raíz de bienvenida.
    Permite comprobar rápidamente que el servidor Uvicorn está activo y funcionando, 
    guiando al desarrollador hacia la documentación interactiva en /docs.
    """
    return {
        "message": "Welcome to the Premium Backend API. Go to /docs for Swagger documentation."
    }