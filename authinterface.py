from abc import ABC, abstractmethod
from typing import Dict, Tuple

class AuthInterface(ABC):
    @abstractmethod
    def signup(self, data:Dict[str, str, str]) -> Tuple[bool, str, str]:
        pass

    @abstractmethod
    def login(self, data: Dict[str, str]) -> Tuple[bool, str, str]:
        pass