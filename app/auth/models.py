from app.core.Base import Base
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship

class Role(Base):
  __tablename__ = "roles"

  id = Column(Integer, primary_key=True, index=True, unique=True)
  user_id = Column(Integer)
  name = Column(String(450), primary_key=True)
  status = Column(Boolean)
  created_at = Column(DateTime, default=datetime.now)
  updated_at = Column(DateTime, default=datetime.now)

class User(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True, index=True, unique=True)
  role_id = Column(Integer, ForeignKey("roles.id", ondelete="SET NULL"))
  full_name = Column(String)
  email = Column(String)
  password = Column(String)
  avatar = Column(String, nullable=True)
  role = relationship("Role", back_populates="users")
  is_active = Column(Boolean, default=False)
  is_email_verified = Column(Boolean, default=False)
  email_verified_at = Column(DateTime)
  created_at = Column(DateTime, default=datetime.now)
  updated_at = Column(DateTime, default=datetime.now)


class Token(Base):
  __tablename__ = "tokens"

  id = Column(Integer, primary_key=True, index=True)
  user_id = Column(Integer)
  access_token = Column(String(450), primary_key=True)
  refresh_token = Column(String(450), nullable=False)
  status = Column(Boolean)
  created_at = Column(DateTime, default=datetime.now)
  updated_at = Column(DateTime, default=datetime.now)