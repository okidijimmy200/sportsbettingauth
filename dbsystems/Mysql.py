import os, jwt
from models.authmodels import UserModel, UserSchema
from authinterface import AuthInterface
from werkzeug.security import generate_password_hash, check_password_hash
from typing import Dict, Tuple

class AuthUser(AuthInterface):
    def __init__(self, db) -> None:
        self.db = db

    def signup(self, username: str, email: str, password: str) -> Tuple[bool, str, str]:
        try:

            '''check if user exists'''
            user = self.db.query(UserModel).filter(UserModel.email == email).first()

            if not user:
                user = UserModel(
                    username=username,
                    email=email,
                    password= generate_password_hash(password)
                )
                self.db.add(user)
                self.db.commit()

                return True, f'Successfully registered {username}', 201
            else:
                return False, 'User already exists. Please Log in.', 403
        except Exception as e:
            result = (
                f"-Failed to create user {username} in MYSQL DB, reason: "
                + f"{type(e).__name__} {str(e)}"
            )
            print(result)
            reason = f'-Failed to create user {username} in MYSQL DB'
            return False, reason, 500

    def login(self, email, password) -> Tuple[bool, str, str]:
        try:
            print(email, password)
            if email is None or password is None:
                return False, "Please provide user details", 400

            schema = UserSchema()
            q = self.db.query(UserModel).filter(UserModel.email == email).first()
            user = schema.dump([q], many=True)

            print(os.environ['SECRET_KEY'])

            if not user:
                return False, 'Could not verify', 401  

            if check_password_hash(user[0]['password'], password):
                token = jwt.encode({
                    'id': user[0]['id']
                }, os.environ['SECRET_KEY'], algorithm="HS256")
                return True, token, 201
            return False, 'Could not verify', 403
        except Exception as e:
            result = (
                f"-Failed to Login into MYSQL DB, reason: "
                + f"{type(e).__name__} {str(e)}"
            )
            print(result)
            reason = f'-Failed to Login into MYSQL DB'
            return False, reason, 500