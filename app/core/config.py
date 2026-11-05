from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Premium Backend API"
    API_V1_STR: str = "/api/v1"
    
    # Esta línea leerá automáticamente el DATABASE_URL del archivo .env
    DATABASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()