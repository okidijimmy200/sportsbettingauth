import grpc
import auth_pb2_grpc
import auth_pb2
from concurrent import futures
from flask import Flask, request, jsonify
from authinterface import AuthInterface
from config import Base, engine, SessionLocal


def create_app():
    app = Flask(__name__) 
    with app.app_context():
        Base.metadata.create_all(engine)
    return app


        

# class SignUpServiceServicer(auth_pb2_grpc.SignUpServiceServicer):
#     def signUp(self, request, context):
#         # operation to perform here before we send back to client
#         # store information in db
#         result = SportsBettingApp(database_service).signup(username=request.username, email=request.email, password=request.password)
#         return auth_pb2.SignUpResponse(boolean=result['boolean'], response=result['response'], status=result['status'])

# def main():
#     server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
#     auth_pb2_grpc.add_SignUpServiceServicer_to_server(SignUpServiceServicer(), server)
#     print("Server started")
#     server.add_insecure_port("[::]:50052")
#     server.start()
#     server.wait_for_termination()
app = create_app()


if __name__ == '__main__':
        app.run(debug=True)
    # main()