from models.models import SignUpRequest

def test_signup(storage, helpers):
    test_cases = [
        {
            "name": "pass",
            "code": 201,
            "reason": ""
        },
        {
            "name": "fail",
            "code": 500,
            "reason": "failed to login"
        }
    ]
    for test_case in test_cases:
        client = helpers.registration(storage=storage)
        client.storage.create_user.return_value = (test_case['code'], test_case['reason'])
        output = client.signup(SignUpRequest('jimmy', 'okidijimmie@gmail.com', 'test123'))
        assert output.code == test_case["code"]
        assert output.reason == test_case["reason"]