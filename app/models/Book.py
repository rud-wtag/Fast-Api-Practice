from sqlalchemy import Column, Integer, String
from app.core.Base import Base


class Books(Base):
  __tablename__ = "books"

  id = Column(Integer, primary_key=True, index=True)
  title = Column(String, index=True)
  author = Column(String, index=True)
  category = Column(String, index=True)
