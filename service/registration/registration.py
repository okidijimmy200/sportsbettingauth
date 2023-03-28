from service.interfaces import StorageInterface
from werkzeug.security import generate_password_hash
from models.models import (
    User,
    SignUpResponse,
    SignUpRequest,
    validate_request,
)


class Registration:
    def __init__(self, storage: StorageInterface) -> None:
        self.storage = storage

    def signup(self, req: SignUpRequest) -> SignUpResponse:
        print('test')
        try:
            valid, reason = validate_request(req)
            if not valid:
                return SignUpResponse(400, reason)
            code, reason = self.storage.create_user(User(
                id=None,
                username=req.username, 
                email=req.email, 
                password=generate_password_hash(req.password)
                )
            )
            
            return SignUpResponse(code, reason)
        except Exception as e:
            return SignUpResponse(code=500, reason=f"failed to sign up: " + f"{type(e).__name__} {str(e)}")
            

