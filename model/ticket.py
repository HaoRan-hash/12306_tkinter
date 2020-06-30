from .base import Base
from sqlalchemy import Column, Integer, String, Date, Time


class Ticket(Base):
    __tablename__ = 'ticket_info'
    ticket_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    train_id = Column(String(10), nullable=False)
    from_station_name = Column(String(20), nullable=False)
    to_station_name = Column(String(20), nullable=False)
    seat_type = Column(String(10), nullable=False)
    price = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    is_get = Column(Integer, nullable=False)
    from_time = Column(Time, nullable=False)
    to_time = Column(Time, nullable=False)
