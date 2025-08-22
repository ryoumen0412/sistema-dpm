from sqlalchemy import Column, Integer, String
from ..database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    usr = Column(String(255), nullable=False, unique=True)
    psswrd = Column(String(255), nullable=False)
    