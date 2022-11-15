import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pymongo import MongoClient

SQLALCHAMY_DATABASE_URL = os.environ['SQLALCHAMY_DATABASE_URL']

engine = create_engine(SQLALCHAMY_DATABASE_URL)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

Base = declarative_base()