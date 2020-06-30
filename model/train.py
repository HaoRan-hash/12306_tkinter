from .base import Base
from sqlalchemy import Column, Integer, String


class Train(Base):
    __tablename__ = 'train_info'
    train_id = Column(String(10), primary_key=True, nullable=False)
    type = Column(Integer, nullable=False)
