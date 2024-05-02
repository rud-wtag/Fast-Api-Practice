import os
from pathlib import Path

from dotenv import load_dotenv

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
  APP_ENV: str = os.getenv("APP_ENV", "local")

  PROJECT_NAME: str = "Demo project"
  PROJECT_VERSION: str = "1.0.0"

  POSTGRES_USER: str = os.getenv("POSTGRES_USER")
  POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
  POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
  POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", 5432)
  POSTGRES_DB: str = os.getenv("POSTGRES_DB", "tdd")
  DATABASE_URL = os.getenv("DB_URL", "tdd")

  SECRET_KEY = os.getenv("SECRET_KEY", "secret")
  ALGORITHM = os.getenv("ALGORITHM")

  LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
  LOG_FILE = os.getenv("LOG_FILE", "app.log")
  LOG_FORMAT = os.getenv("LOG_FORMAT", "{time} - {level} - {message}")
  LOG_ROTATION = os.getenv("LOG_ROTATION", "100 MB")
  LOG_RENTATION = os.getenv("LOG_RENTATION", "30 days")
  LOG_SERIALIZATION = os.getenv("LOG_SERIALIZATION", "false").lower() in (
    "true",
    "1",
    "t",
  )


settings = Settings()
