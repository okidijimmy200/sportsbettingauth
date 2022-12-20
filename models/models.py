# service models
from typing import Tuple


class User:
    id: int
    username: str
    email: str
    password: str

    def __init__(self, id: int, username: str, email: str, password: str):
        self.id = id
        self.username = username
        self.email = email
        self.password = password


class SignUpRequest:
    username: str
    email: str
    password: str

    def __init__(self, username: str, email: str, password: str):
        self.username = username
        self.email = email
        self.password = password


class SignUpResponse:
    code: int
    reason: str

    def __init__(self, code: int, reason: str):
        self.code = code
        self.reason = reason


class LoginRequest:
    email: str
    password: str
    reason: str

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def validate(self):
        if self.email == "":
            self.reason = "email is required"
            return False
        if self.password == "":
            self.reason = "password is required"
            return False

        return True


class LoginResponse:
    code: int
    reason: str
    token: str

    def __init__(self, code: int, reason: str, token: str):
        self.code = code
        self.reason = reason
        self.token = token


class ValidateTokenRequest:
    token: str

    def __init__(self, token: str):
        self.token = token


class ValidateTokenResponse:
    code: int
    reason: str
    user_id: str

    def __init__(self, code: int, reason: str, user_id: str):
        self.code = code
        self.reason = reason
        self.user_id = user_id


def validate_request(instance) -> Tuple[bool, str]:
    for key, value in instance.__dict__.items():
        if isinstance(value, str) and value == "":
            return False, f"{key} is required"
        if isinstance(value, int) and value == 0:
            return False, f"{key} is required"
    return True, ""
