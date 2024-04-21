from app.core.Base import Base
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship


class Role(Base):
  __tablename__ = "roles"

  id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
  name = Column(String(450), primary_key=True)
  created_at = Column(DateTime, default=datetime.now)
  updated_at = Column(DateTime, default=datetime.now)


class User(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True, index=True, unique=True)
  role_id = Column(Integer, ForeignKey("roles.id", ondelete="SET NULL"), nullable=True)
  full_name = Column(String)
  email = Column(String)
  password = Column(String)
  avatar = Column(String, nullable=True)
  role = relationship("Role")
  is_active = Column(Boolean, default=False)
  is_email_verified = Column(Boolean, default=False)
  email_verified_at = Column(DateTime)
  created_at = Column(DateTime, default=datetime.now)
  updated_at = Column(DateTime, default=datetime.now)


class Token(Base):
  __tablename__ = "tokens"

  id = Column(Integer, primary_key=True, index=True, unique=True)
  user_id = Column(Integer)
  token = Column(String)
  status = Column(Boolean, default=True)
  created_at = Column(DateTime, default=datetime.now)
  updated_at = Column(DateTime, default=datetime.now)
