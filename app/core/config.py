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

  SECRET_KEY = os.getenv("SECRET_KEY", "secret")
  ALGORITHM = os.getenv("ALGORITHM")

  APP_HOST = os.getenv("APP_HOST")
  MAIL_FROM_NAME = os.getenv("MAIL_FROM_NAME")

  FORGET_PASSWORD_LINK_EXPIRE_MINUTES = os.getenv("FORGET_PASSWORD_LINK_EXPIRE_MINUTES")
  MAIL_USERNAME = os.getenv("MAIL_USERNAME")
  MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
  MAIL_FROM = os.getenv("MAIL_FROM")
  MAIL_PORT = os.getenv("MAIL_PORT")
  MAIL_SERVER = os.getenv("MAIL_SERVER")
  MAIL_SSL_TLS = os.getenv('MAIL_SSL_TLS', 'False').lower() in ('true', '1', 't')
  MAIL_STARTTLS = os.getenv('MAIL_STARTTLS', 'False').lower() in ('true', '1', 't')
  USE_CREDENTIALS = os.getenv('USE_CREDENTIALS', 'False').lower() in ('true', '1', 't')
  VALIDATE_CERTS = os.getenv('VALIDATE_CERTS', 'False').lower() in ('true', '1', 't')
  MAIL_DEBUG = os.getenv('MAIL_DEBUG', 'True').lower() in ('true', '1', 't')
  MAIL_DEBUG = os.getenv('MAIL_DEBUG', 'True').lower() in ('true', '1', 't')





settings = Settings()
