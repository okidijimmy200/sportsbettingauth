from flask import jsonify
from authinterface import AuthInterface

class SportsBettingApp:
    def __init__(self,  db_service_provider: AuthInterface) -> None:
        self.db = db_service_provider

    def signup(self, username, email, password):
        try:
            created, reason, status = self.db.signup(username, email, password)
            if not created:
                print(reason)
                return False, reason, status
            return True, reason, status
        except Exception as e:
            result = (
                f"-Error "
                + f"{type(e).__name__} {str(e)}"
            )
            print(result)
            return result

    def login(self, email, password):
        try:
            created, reason, status = self.db.login(email, password)
            if not created:
                print(reason)
                return False, reason, status
            return True, reason, status
        except Exception as e:
            result = (
                f"-Error "
                + f"{type(e).__name__} {str(e)}"
            )
            print(result)
            return result