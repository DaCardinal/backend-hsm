from pydantic_settings import BaseSettings
import cloudinary.api

class Settings(BaseSettings):
    APP_NAME: str
    APP_URL: str
    LOG_LEVEL: str
    
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_DATABASE: str
    DB_ENGINE: str
    DB_DATABASE_DEFAULT: str

    GOOGLE_SIGNIN_CLIENT_ID: str
    GOOGLE_SIGNIN_CLIENT_SECRET: str
    GOOGLE_CALLBACK: str

    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str

    JWT_ALGORITHM: str
    JWT_SECRET: str

    PYTHON_VERSION: str

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET
)