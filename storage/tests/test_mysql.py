from unittest import mock
import pytest
from typing import Dict, Tuple
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String
from storage.mysql.mysql import MySQLStorage
from werkzeug.security import generate_password_hash
from models.models import User

@pytest.fixture(scope='function')
def db_session():
    """Session for SQLAlchemy."""
    Base = declarative_base()  
    meta = Base.metadata
    engine = create_engine('sqlite://')
    Table('users', meta, Column('id',Integer, primary_key=True, index=True), Column('username',String(20), index=True, nullable=False), Column('email',String(50), index=True,  unique=True), Column('password',String(3000), index=True, nullable=False))
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

class MockUser(object):
    id = 1
    username='jimmyjones'
    email = 'okidijimmie@gmail.com'
    password = generate_password_hash('test123')

def test_create_user(db_session):
    test_cases = [
        {
            "name": "pass",
            "input": MockUser,
            "output": (201, 'user created')
        },
        {
            "name": "fail",
            "input": MockUser,
            "output": (403, 'user already exists')
        },
    ]
    for test_case in test_cases:
        result = MySQLStorage(db_session).create_user(test_case['input'])
        assert result == test_case['output']

def test_find_user(db_session):
    test_cases = [
        {
            "name": "pass",
            "input": 'okidijimmie@gmail.com',
            "output": 200
        },
        {
            "name": "fail",
            "input": 'test@test.com',
            "output": 404
        },
    ]
    for test_case in test_cases:
        MySQLStorage(db_session).create_user(MockUser)
        result = MySQLStorage(db_session).find_user(test_case['input'])
        assert result[0] == test_case['output']