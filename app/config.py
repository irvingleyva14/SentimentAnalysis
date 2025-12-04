# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Sentiment Analysis API"
    MODEL_PATH: str = "models/multilingual-sentiment"
    ENVIRONMENT: str = "development"  # dev | prod | test

settings = Settings()

