from sqlalchemy.orm import sessionmaker
from storage.mysql.config import Base, engine, SessionLocal

db = SessionLocal()


def auto_create():
    Base.metadata.create_all(engine)


def get_instance() -> sessionmaker:
    return db
