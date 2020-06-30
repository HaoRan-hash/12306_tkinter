from .base import Base
from sqlalchemy import Column, Integer, String


class User(Base):
    __tablename__ = 'user_info'
    user_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_name = Column(String(20), nullable=False)
    password = Column(String(32), nullable=False)
    role = Column(Integer, nullable=False)
