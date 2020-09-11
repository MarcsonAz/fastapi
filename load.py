import json
import datetime

from app import models
from app.database import SessionLocal, engine

db = SessionLocal()

models.Base.metadata.create_all(bind=engine)

file = open('./summary.json')
data = json.load(file)

for row in data['Countries']:
    db_countries = models.CovidModel(
        create_at=datetime.datetime.now(),
        country=row["Country"],
        slug=row["Slug"],
        cases=row["TotalConfirmed"],
        deaths=row["TotalDeaths"],
        recoveries=row["TotalRecovered"],
        date=row["Date"]
    )
    db.add(db_countries)


db.commit()

db.close()