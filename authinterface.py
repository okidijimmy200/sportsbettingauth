from abc import ABC, abstractmethod
from typing import Dict, Tuple

class AuthInterface(ABC):
    @abstractmethod
    def signup(self, username: str, email: str, password: str) -> Tuple[bool, str, str]:
        pass

    @abstractmethod
    def login(self,  email: str, password: str) -> Tuple[bool, str, str]:
        pass