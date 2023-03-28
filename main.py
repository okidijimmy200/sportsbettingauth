import os
from server.grpc.grpc import run
from service.auth.authentication import Authentication
from service.registration.registration import Registration
from pymongo import MongoClient
from storage.mongodb.Mongodb import MongoStorage
from storage.mysql.functions import auto_create, get_instance


if __name__ == '__main__':
    auto_create()

    db = get_instance()
    mongo_db = MongoClient(os.environ['DATABASE_LOCAL'])
    database = os.environ['Database']
    collection = os.environ['Collection']

    # user_storage = MySQLStorage(db)
    user_storage = MongoStorage(mongo_db, database, collection)

    authentication_service = Authentication(user_storage)
    registration_service = Registration(user_storage)

    run(authentication_service, registration_service)
