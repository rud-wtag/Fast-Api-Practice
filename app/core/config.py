import os
from dotenv import load_dotenv

from pathlib import Path

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
  PROJECT_NAME: str = "Demo project"
  PROJECT_VERSION: str = "1.0.0"

  POSTGRES_USER: str = os.getenv("POSTGRES_USER")
  POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
  POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
  POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", 5432)
  POSTGRES_DB: str = os.getenv("POSTGRES_DB", "tdd")
  DATABASE_URL = os.getenv("DB_URL", "tdd")


settings = Settings()
