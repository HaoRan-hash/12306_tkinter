from .base import Base
from sqlalchemy import Column, Integer, String, Date


class TrainRemain(Base):
    __tablename__ = 'train_remain_info'
    train_id = Column(String(10), primary_key=True, nullable=False)
    station_id = Column(Integer, primary_key=True, nullable=False)
    seat_count = Column(Integer, nullable=False, default=708)
    bed_top_count = Column(Integer, nullable=False, default=110)
    bed_mid_count = Column(Integer, nullable=False, default=110)
    bed_bot_count = Column(Integer, nullable=False, default=110)
    date = Column(Date, nullable=False)
    order = Column(Integer, nullable=False)
