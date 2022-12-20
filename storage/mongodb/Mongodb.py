import json
from typing import Tuple
from bson import json_util
from service.interfaces import StorageInterface
from pymongo import MongoClient
from models.models import User


class MongoStorage(StorageInterface):
    def __init__(self, mongo_conn, database, collection) -> None:
        self.client = mongo_conn

        cursor = self.client[database]
        self.collection = cursor[collection]

    def find_user(self, email: str) -> Tuple[int, str, User]:
        try:
            user = self.collection.find_one( { "email": f"{email}" } )
            new_user = json.loads(json_util.dumps(user))
            
            if user is None:
                return 404, "user not found", None
            return 200, "", User(new_user['_id']['$oid'], new_user['username'], new_user['email'], new_user['password'])
        except Exception as e:
            reason = (
                f"failed to read data from storage: "
                + f"{type(e).__name__} {str(e)}"
            )
            print(reason) # TODO: make log
            return 500, reason, None

    def create_user(self, user: User) -> Tuple[int, str]:
        try:
            # get email
            email = user.email
            name = user.username
            password = user.password

            '''check if user exists'''
            user = self.collection.find_one( { "email": f"{email}" } )
            if not user:
                new_data = {
                    "username": f"{name}", 
                    "email": f"{email}",
                    "password":  f"{password}"
                }
                self.collection.insert_one(new_data)

                return 201, f'Successfully registered {name}'
            
            return 403, 'User already exists. Please Log in.'
        except Exception as e:
            result = (
                f"-Failed to create user {name} in MongoDB, reason: "
                + f"{type(e).__name__} {str(e)}"
            )
            print(result)
            reason = f'-Failed to create user {name} in MYSQL DB'
            return 500, reason