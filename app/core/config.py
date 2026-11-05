from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Premium Backend API"
    API_V1_STR: str = "/api/v1"
    
    # URL de conexión por defecto a PostgreSQL (ajustala con tus credenciales locales o vía .env)
    DATABASE_URL: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/backend_db"
    class Config:
        env_file = ".env"

settings = Settings()