from server.grpc.grpc import run
from service.authentication import Authentication
from service.registration import Registration
from storage.mysql.mysql import MySQLStorage
from storage.mysql.functions import auto_create, get_instance


if __name__ == '__main__':
    auto_create()

    db = get_instance()

    user_storage = MySQLStorage(db)

    authentication_service = Authentication(user_storage)
    registration_service = Registration(user_storage)

    run(authentication_service, registration_service)
