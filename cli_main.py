from models.models import SignUpRequest
from storage.mysql.mysql import MySQLStorage
from service.registration import Registration
from storage.mysql.functions import auto_create, get_instance

def getUserFromCLI() -> SignUpRequest:
    # read signup params from the command line
    return SignUpRequest()

if __name__ == '__main__':
    auto_create()

    db = get_instance()

    user_storage = MySQLStorage(db)
    
    registration_service = Registration(user_storage)

    user = getUserFromCLI()
    response = registration_service.signup(user)

    # print response to the command line
    print(response)
