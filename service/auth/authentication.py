import os, jwt, logger
from typing import Dict
from service.interfaces import AuthenticationInterface, StorageInterface
from werkzeug.security import check_password_hash
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
        self.logging = logger.setup_logger("my_logger", log_file="app.log")

    def login(self, req: LoginRequest) -> LoginResponse:
        try:
            valid, reason = validate_request(req)
            if not valid:
                return LoginResponse(400, reason, token=None)

            code, reason, user = self.storage.find_user(req.email)
            if code != 200 and code != 201:
                return LoginResponse(code, reason, token=None)
            token = jwt.encode({"id": user.id, "email": user.email}, os.environ["SECRET_KEY"], algorithm="HS256")
            if check_password_hash(user.password, req.password):
                return LoginResponse(
                    code=200,
                    reason="",
                    token=token)
            else:
                return LoginResponse(401, "invalid password", token=None)
        except Exception as e:
            self.logging.exception(f"Failed to login user: " + f"{type(e).__name__} {str(e)}")
            return LoginResponse(code=500, reason=f"Internal Server Error", token=None)
        

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
                
            if type(user.id) is int:
                userID = str(user.id)
                return ValidateTokenResponse(200, "", userID)
            
            return ValidateTokenResponse(200, "", user.id)
        except Exception as e:
            self.logging.exception(f"failed to validate token: " + f"{type(e).__name__} {str(e)}")
            return ValidateTokenResponse(code=500, reason="Internal Server Error")


# SOLID
# Single Responsibility Principle
# Open Closed Principle
# Liskov Substitution Principle
# Interface Segregation Principle
# Dependency Inversion Principle
