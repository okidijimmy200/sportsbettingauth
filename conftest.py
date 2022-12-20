import pytest
from unittest import mock
from service.authentication import Authentication
from service.registration import Registration

class Helpers:
    @staticmethod
    def authentication(storage):
        client = Authentication(storage=storage)
        return client

    @staticmethod
    def registration(storage):
        client = Registration(storage=storage)
        return client
        

@pytest.fixture
def helpers():
    return Helpers

@pytest.fixture
def db_name(request):
    service = request.config.getoption('--service')
    return service

@pytest.fixture
@mock.patch('storage.mysql.mysql.MySQLStorage')
def storage(mock_mysql, db_name):
    print(db_name)
    if db_name == 'mysql':
        return mock_mysql

def pytest_addoption(parser):
    parser.addoption(
        "--service", action="store", default="mysql"
    )