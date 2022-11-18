from flask import jsonify
from authinterface import AuthInterface, TokenInterface

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

class TokenRequiredSys:
    def __init__(self,  db_token_gen: TokenInterface) -> None:
        self.token = db_token_gen

    def get_current_user_token(self, token):
        try:
            result = self.token.get_current_user(token=token)
            return result
        except Exception as e:
            result = (
                f"-Error "
                + f"{type(e).__name__} {str(e)}"
            )
            print(result)
            return result