from werkzeug.security import generate_password_hash
from models.models import LoginRequest, ValidateTokenRequest

class MockPerson(object):
    id = 1
    email = 'okidijimmie@gmail.com'
    password = generate_password_hash('test123')

def test_login(storage, helpers):
    test_cases = [
        {
            "name": "pass",
            "code": 200,
            "reason": ""
        },
        {
            "name": "invalid",
            "code": 401,
            "reason": "invalid password"
        },
        {
            "name": "fail",
            "code": 500,
            "reason": "failed to login"
        }
    ]
    for test_case in test_cases:
        client = helpers.authentication(storage=storage)
        client.storage.find_user.return_value = (test_case['code'], test_case['reason'], MockPerson())
        output = client.login(LoginRequest("okidijimmie@gmail.com", "test123" ))
        assert output.code == test_case['code']
        assert output.reason == test_case["reason"]

    
def test_validate_token(storage, helpers):
    test_cases = [
        {
            "name": "pass",
            "code": 200,
            "reason": ""
        },
        {
            "name": "invalid",
            "code": 401,
            "reason": "invalid password"
        },
        {
            "name": "fail",
            "code": 500,
            "reason": "failed to login"
        }
    ]
    for test_case in test_cases:
        client = helpers.authentication(storage=storage)
        client.storage.find_user.return_value = (test_case['code'], test_case['reason'], MockPerson())
        output = client.validate_token(ValidateTokenRequest("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwiZW1haWwiOiJva2lkaWppbW1pZTEyMzQ1NjdAZ21haWwuY29tIn0.Co2NFMS1-PdA_8d9ZHvGBWMltUQt3xKj8IganUlNXbE"))
        assert output.code == test_case["code"]
        assert output.reason == test_case['reason']