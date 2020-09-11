from sqlalchemy import Column, Integer, String
from sqlalchemy.types import Date, DateTime
from .database import Base


class CovidModel(Base):
    __tablename__ = "covid19online"

    id = Column(Integer, primary_key=True, index=True)
    create_at = Column(Date)
    country = Column(String(255), index=True)
    slug = Column(String(255), index=True)
    cases = Column(Integer)
    deaths = Column(Integer)
    recoveries = Column(Integer)
    date = Column(DateTime)