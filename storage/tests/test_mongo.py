import pytest
import pymongo
from werkzeug.security import generate_password_hash
from storage.mongodb.Mongodb import MongoStorage

@pytest.fixture(scope="session")
def mongo_conn():
    myclient = pymongo.MongoClient("mongodb://0.0.0.0:27017/")

    yield myclient
    myclient.drop_database('testdb')

class MockUser(object):
    id = 1
    username='jimmyjones'
    email = 'okidijimmie@gmail.com'
    password = generate_password_hash('test123')

def test_create_user(mongo_conn):
    test_cases = [
        {
            "name": "pass",
            "input": MockUser,
            "output": (201, 'Successfully registered jimmyjones')
        },
        {
            "name": "fail",
            "input": MockUser,
            "output": (403, 'User already exists. Please Log in.')
        }
    ]
    for test_case in test_cases:
        result = MongoStorage(mongo_conn, 'testdb', 'testcollection').create_user(test_case['input'])
        assert result == test_case['output']

def test_find_user(mongo_conn):
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
        }
    ]
    for test_case in test_cases:
        MongoStorage(mongo_conn, 'testdb', 'testcollection').create_user(MockUser)
        result = MongoStorage(mongo_conn, 'testdb', 'testcollection').find_user(test_case['input'])
        assert result[0] == test_case['output']
