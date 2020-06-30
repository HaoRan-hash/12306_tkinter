from .base import Base
from sqlalchemy import Column, Integer, String, Time


class TrainPass(Base):
    __tablename__ = 'train_pass_info'
    train_id = Column(String(10), primary_key=True, nullable=False)
    station_id = Column(Integer, primary_key=True, nullable=False)
    is_stay = Column(Integer, nullable=False)
    order = Column(Integer, nullable=False)
    arrive_time = Column(Time)
    leave_time = Column(Time)
    mileage = Column(Integer, nullable=False)
