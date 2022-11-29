import grpc
from concurrent import futures
import generated.auth_pb2 as auth_pb2
import generated.auth_pb2_grpc as auth_pb2_grpc
from service.interfaces import AuthenticationInterface, RegistrationInterface
from models.models import (
    LoginRequest,
    ValidateTokenRequest,
    SignUpRequest,
)


class UserManagementService(auth_pb2_grpc.UserManagenmentServiceServicer):
    authentication_service: AuthenticationInterface
    registration_service: RegistrationInterface

    def __init__(
        self,
        authentication_service: AuthenticationInterface,
        registration_service: RegistrationInterface,
    ):
        self.authentication_service = authentication_service
        self.registration_service = registration_service

    def SignUp(self, request, context):
        # operation to perform here before we send back to client
        # store information in db
        response = self.registration_service.signup(
            SignUpRequest(request.username, request.email, request.password)
        )
        return auth_pb2.SignUpResponse(code=response.code, reason=response.reason)

    def Login(self, request, context):
        response = self.authentication_service.login(
            LoginRequest(request.email, request.password)
        )
        return auth_pb2.LoginResponse(code=response.code, reason=response.reason, token=response.token)

    def ValidateToken(self, request, context):
        response = self.authentication_service.validate_token(
            ValidateTokenRequest(request.token)
        )
        return auth_pb2.ValidateTokenResponse(
            code=response.code, reason=response.reason, user_id=response.user_id
        )


def run(
    authentication_service: AuthenticationInterface,
    registration_service: RegistrationInterface,
):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    auth_pb2_grpc.add_UserManagenmentServiceServicer_to_server(
        UserManagementService(authentication_service, registration_service), server
    )
    print("server started")
    server.add_insecure_port("[::]:50052")
    server.start()
    server.wait_for_termination()
