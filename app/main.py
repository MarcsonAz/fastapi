from typing import List
import datetime, uuid

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from . import models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/")
def main():
    return RedirectResponse(url="/docs/")

@app.get("/all/", response_model=List[schemas.CovidModel])
def show_data(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    data = db.query(models.CovidModel).offset(skip).limit(limit).all()
    return data

@app.get("/countries/{slug}", response_model=schemas.CovidModel)
def country_data(slug: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    country = db.query(models.CovidModel).filter(models.CovidModel.slug == slug).offset(skip).limit(limit).first()
    if country is None:
        raise HTTPException(status_code=404, detail="Country not found")
    return country


@app.get("/countries/total/{slug}", response_model=List[schemas.CovidModel])
def all_country_data(slug:str, skip:int=0, limit:int=100, db:Session=Depends(get_db)):
    data = db.query(models.CovidModel).filter(models.CovidModel.slug == slug).offset(skip).limit(limit).all()
    return data
