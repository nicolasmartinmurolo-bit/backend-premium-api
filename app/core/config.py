"""
Módulo de Configuración Global del Proyecto.
--------------------------------------------------------------------------------
Este archivo utiliza Pydantic Settings para centralizar, tipar y validar todas 
las variables de entorno de la aplicación. Actúa como la "única fuente de la 
verdad" para los parámetros globales (como nombres de la API, prefijos y 
credenciales de base de datos o seguridad).
"""

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Clase de configuración principal heredada de BaseSettings.
    Pydantic lee automáticamente los atributos definidos aquí y busca sus 
    valores correspondientes en el archivo .env o en las variables de entorno del sistema.
    """
    
    # -------------------------------------------------------------------------
    # 1. Metadatos Generales de la API
    # -------------------------------------------------------------------------
    PROJECT_NAME: str = "Premium Backend API"
    API_V1_STR: str = "/api/v1"
    
    # -------------------------------------------------------------------------
    # 2. Credenciales y Configuración de Base de Datos
    # -------------------------------------------------------------------------
    # Al no tener un valor por defecto asignado, Pydantic exigirá obligatoriamente 
    # que esta variable esté presente en el archivo .env, lanzando un error si falta.
    DATABASE_URL: str

    # -------------------------------------------------------------------------
    # 3. Configuración de Seguridad y Autenticación (JWT)
    # -------------------------------------------------------------------------
    SECRET_KEY: str                    # Llave criptográfica para firmar los tokens JWT.
    ALGORITHM: str                     # Algoritmo de encriptación simétrica (ej. HS256).
    ACCESS_TOKEN_EXPIRE_MINUTES: int   # Tiempo de vida útil del token antes de expirar.

    # -------------------------------------------------------------------------
    # 4. Configuración Interna de Pydantic (Clase Config)
    # -------------------------------------------------------------------------
    class Config:
        """
        Configuraciones de comportamiento para Pydantic.
        'env_file' le indica explícitamente que debe buscar y cargar las 
        variables desde el archivo local llamado '.env' ubicado en la raíz.
        """
        env_file = ".env"
        env_file_encoding = "utf-8"  # Asegura soporte correcto para acentos y caracteres especiales.


# Instancia global de configuración.
# Al importar 'settings' desde cualquier otro archivo de la aplicación, 
# ya tendremos disponibles todas las variables validadas y listas para usar.
settings = Settings()