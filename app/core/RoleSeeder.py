from app.auth.models import Role
from app.auth.constants import USER, GUEST, ADMIN
from fastapi import Depends
from app.core.database import get_db
from sqlalchemy.orm import Session

class RoleSeeder:
  def __init__(self, db: Session = Depends(get_db)):
    self.db = db

  def seed_roles(self):
    roles = [
      {"name": GUEST},
      {"name": USER},
      {"name": ADMIN},
    ]
    for role_data in roles:
      role = Role(**role_data)
      self.db.add(role)
      self.db.commit()