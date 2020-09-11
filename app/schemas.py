from datetime import date, datetime
from pydantic import BaseModel, Field


class CovidModel(BaseModel):
    id        : str
    create_at : date
    country   : str
    slug      : str
    cases     : int
    deaths    : int
    recoveries: int
    date      : datetime

    class Config:
        orm_mode = True
