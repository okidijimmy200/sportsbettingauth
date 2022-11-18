import grpc
import auth_pb2_grpc
import auth_pb2
from flask import jsonify
from concurrent import futures
from config import  SessionLocal
from dbsystems.Mysql import AuthUser
import sportsbettingapp
from app import app
from dbsystems.Mysql import MySQLTokenDecorator

db = SessionLocal()

database_service = AuthUser(db)

mysql_token = MySQLTokenDecorator(db)


class SignUpServiceServicer(auth_pb2_grpc.SignUpServiceServicer):
    def signUp(self, request, context):
        # operation to perform here before we send back to client
        # store information in db
        with app.app_context():
            result = sportsbettingapp.SportsBettingApp(database_service).signup(request.username, request.email, request.password)
            return auth_pb2.SignUpResponse(boolean=result[0], response=result[1], status=result[2])

class LoginServiceServicer(auth_pb2_grpc.LoginServiceServicer):
    def login(self, request, context):
        with app.app_context():
            result = sportsbettingapp.SportsBettingApp(database_service).login(request.email, request.password)
            return auth_pb2.LoginResponse(boolean=result[0], response=result[1], status=result[2])

class TokenServiceServicer(auth_pb2_grpc.TokenServiceServicer):
    def ValidateToken(self, request, context):
        with app.app_context():
            result = sportsbettingapp.TokenRequiredSys(mysql_token).get_current_user_token(token=request.token)
            print(result[0], type(result[0]))
            return auth_pb2.TokenResponse(id=result[0]['id'], email=result[0]['email'], username=result[0]['username'], password=result[0]['password'])

def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    auth_pb2_grpc.add_SignUpServiceServicer_to_server(SignUpServiceServicer(), server)
    auth_pb2_grpc.add_LoginServiceServicer_to_server(LoginServiceServicer(), server)
    auth_pb2_grpc.add_TokenServiceServicer_to_server(TokenServiceServicer(), server)
    print("Server started")
    server.add_insecure_port("[::]:50052")
    server.start()
    server.wait_for_termination()

main()