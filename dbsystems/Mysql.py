from models.authmodels import UserModel, UserSchema
from authinterface import AuthInterface
from werkzeug.security import generate_password_hash, check_password_hash
from typing import Dict, Tuple

class AuthUser(AuthInterface):
    def __init__(self, db) -> None:
        self.db = db

    def signup(self, data: Dict[str, str, str]) -> Tuple[bool, str, str]:
        return super().signup(data)

    def login(self, data: Dict[str, str]) -> Tuple[bool, str, str]:
        return super().login(data)