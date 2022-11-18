from abc import ABC, abstractmethod
from typing import Tuple
from models.models import (
    User,
    LoginRequest,
    ValidateTokenRequest,
    ValidateTokenResponse,
    SignUpResponse,
    LoginResponse,
    SignUpRequest,
)


class AuthenticationInterface(ABC):
    @abstractmethod
    def login(self, req: LoginRequest) -> LoginResponse:
        pass

    @abstractmethod
    def validate_token(self, req: ValidateTokenRequest) -> ValidateTokenResponse:
        pass


class RegistrationInterface(ABC):
    @abstractmethod
    def signup(self, req: SignUpRequest) -> SignUpResponse:
        pass


class StorageInterface(ABC):
    @abstractmethod
    def find_user(self, email: str) -> Tuple[int, str, User]:
        pass

    @abstractmethod
    def create_user(self, user: User) -> Tuple[int, str]:
        pass
