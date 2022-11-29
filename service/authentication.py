import os, jwt
from typing import Dict
from service.interfaces import AuthenticationInterface, StorageInterface
from werkzeug.security import generate_password_hash, check_password_hash
from models.models import (
    LoginRequest,
    ValidateTokenRequest,
    ValidateTokenResponse,
    LoginResponse,
    validate_request,
)


class Authentication(AuthenticationInterface):
    storage: StorageInterface

    def __init__(self, storage: StorageInterface) -> None:
        self.storage = storage

    def login(self, req: LoginRequest) -> LoginResponse:
        try:
            valid, reason = validate_request(req)
            if not valid:
                return LoginResponse(400, reason)

            code, reason, user = self.storage.find_user(req.email)
            if code != 200 and code != 201:
                return LoginResponse(code, reason, token=None)
            token = jwt.encode({"id": user.id, "email": user.email}, os.environ["SECRET_KEY"], algorithm="HS256")
            if check_password_hash(user.password, req.password):
                print('if statement test')
                return LoginResponse(
                    200,
                    "",
                    token)
            else:
                return LoginResponse(401, "invalid password")
        except Exception as e:
            # return LoginResponse(code=500, reason=f"failed to log in: " + f"{type(e).__name__} {str(e)}")
            result = (
                f"failed to log in, reason: "
                + f"{type(e).__name__} {str(e)}"
            )
            print(result)
            return result

    def validate_token(self, req: ValidateTokenRequest) -> ValidateTokenResponse:
        try:
            valid, reason = validate_request(req)
            if not valid:
                return LoginResponse(400, reason, token=None)

            data: Dict[str, int] = jwt.decode(req.token, os.environ['SECRET_KEY'], algorithms=["HS256"])
            # TODO: check if token is expired etc.

            code, reason, user = self.storage.find_user(data['email'])
   
            if code != 200:
                return ValidateTokenResponse(code, reason, user_id=None)
            
            return ValidateTokenResponse(200, "", user.id)
        except Exception as e:
            return ValidateTokenResponse(code=500, reason=f"failed to validate token: " + f"{type(e).__name__} {str(e)}")


# SOLID
# Single Responsibility Principle
# Open Closed Principle
# Liskov Substitution Principle
# Interface Segregation Principle
# Dependency Inversion Principle
