from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# database
DATABASE_URL = "postgres://hlmnkwzs:3fpr0W89DAFULiuX9BeGfS-aUWA0vuM8@motty.db.elephantsql.com:5432/hlmnkwzs"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()