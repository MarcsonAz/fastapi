from typing import List
import datetime, uuid

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from . import models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

#App Config
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

# Routes
@app.get("/")
def doc():
    """
    Redireciona para a documentação da API (não retorna dados)
    """
    return RedirectResponse(url="/docs/")

@app.get("/all/", response_model=List[schemas.CovidModel])
def show_data(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retorna todo o banco de dados
    """
    data = db.query(models.CovidModel).offset(skip).limit(limit).all()
    return data

@app.get("/countries/{slug}", response_model=schemas.CovidModel)
def last_country_data(slug: str, db: Session = Depends(get_db)):
    """
        Retorna o ultimo dia deste pais no banco de dados
    """
    country = db.query(models.CovidModel).\
        filter(models.CovidModel.slug == slug).\
        order_by(models.CovidModel.date.desc()).first()
    if country is None:
        raise HTTPException(status_code=404, detail="Country not found")
    return country

@app.get("/countries/total/{slug}", response_model=List[schemas.CovidModel])
def all_country_data(slug:str, db:Session=Depends(get_db)):
        """
        Retorna todos dias deste pais no banco de dados
        """
        data = db.query(models.CovidModel).\
            filter(models.CovidModel.slug == slug).all()
        return data


## rotas auxiliares 
@app.get("/count/", response_model=schemas.CovidModel)
def count_data(db: Session = Depends(get_db)):
    """
        Retorna os dados do ultimo id no banco de dados
    """
    n_id = db.query(models.CovidModel).\
        filter(models.CovidModel.id >= 600).\
        order_by(models.CovidModel.id.desc()).first()
    if n_id is None:
        raise HTTPException(status_code=404, detail="id not found")
    print(n_id.id)
    return n_id


@app.get("/count/{slug}")
def count_id(slug: str, db: Session = Depends(get_db)):
    """
        Retorna a quantidade de dados daquele pais no banco de dados
    """
    n_id = db.query(models.CovidModel.id).\
        filter(models.CovidModel.slug == slug).count()

    if (n_id == 0 or n_id is None):
        raise HTTPException(status_code=404, detail="Country not found in database")
    return n_id