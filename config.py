# config.py
from pathlib import Path
from dotenv import load_dotenv
import os

# Завантаження змінних середовища з файлу .env
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Settings:
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_NAME: str = os.getenv("DB_NAME")
    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: str = os.getenv("DB_PORT")

    # Створення URL для підключення до БД
    DATABASE_URL: str = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

# Ініціалізація налаштувань
settings = Settings()
