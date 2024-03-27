from sqlalchemy import Column, Integer, String
from app.models.Base import Base


class User(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True, index=True)
  full_name = Column(String)
  email = Column(String)
  password = Column(String)
  avatar = Column(String, nullable=True)
