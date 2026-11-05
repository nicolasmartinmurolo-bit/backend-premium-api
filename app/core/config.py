from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Premium Backend API"
    API_V1_STR: str = "/api/v1"
    
    # Base de datos
    DATABASE_URL: str

    # Configuración de JWT
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"

settings = Settings()