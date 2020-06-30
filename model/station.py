from .base import Base
from sqlalchemy import Column, Integer, String


class Station(Base):
    __tablename__ = 'station_info'
    station_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    station_name = Column(String(20), nullable=False)
    image = Column(String(100))
