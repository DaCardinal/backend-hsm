from pydantic_settings import BaseSettings

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

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()