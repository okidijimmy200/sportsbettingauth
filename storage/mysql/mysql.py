from typing import Tuple
from sqlalchemy.orm import sessionmaker
from service.interfaces import StorageInterface
from storage.mysql.models import UserModel, UserSchema
from models.models import User


class MySQLStorage(StorageInterface):
    db: sessionmaker

    def __init__(self, db: sessionmaker):
        self.db = db

    def find_user(self, email: str) -> Tuple[int, str, User]:
        try:
            user: UserModel = self.db.query(UserModel).filter(UserModel.email == email).first()
            
            if user is None:
                return 404, "user not found", None
            return 200, "", User(user.id, user.username, user.email, user.password)
        except Exception as e:
            reason = (
                f"failed to read data from storage: "
                + f"{type(e).__name__} {str(e)}"
            )
            print(reason) # TODO: make log
            return 500, reason, None

    def create_user(self, user: User) -> Tuple[int, str]:
        try:
            _user = self.db.query(UserModel).filter(UserModel.email == user.email).first()
            if not _user:
                _user = UserModel(
                    username=user.username,
                    email=user.email,
                    password=user.password # this is hashed in the service layer a.k.a business logc
                )
                self.db.add(_user)
                self.db.commit()
            else:
                return 403, "user already exists"

            return 201, "user created"
        except Exception as e:
            reason = (
                f"failed to read data from storage: "
                + f"{type(e).__name__} {str(e)}"
            )
            print(reason) # TODO: make log
            return 500, reason, None
