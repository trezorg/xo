import json


def test_signup_bad_request_no_password(client, signup_url):
    data = {
        'username': 'test'
    }
    response = client.post(
        signup_url,
        data=json.dumps(data),
        content_type='application/json'
    )
    assert response.status_code == 400, data
    payload = response.json
    assert 'error' in payload
    assert 'status_code' in payload
    assert 'description' in payload


def test_signup_existing_login(client, signup_url, db_user):
    data = {
        'username': db_user.login,
        'password': db_user.password,
    }
    response = client.post(
        signup_url,
        data=json.dumps(data),
        content_type='application/json'
    )
    payload = response.json
    assert response.status_code == 400, payload
    assert 'error' in payload, payload


def test_signup(client, signup_url, str_generator):
    data = {
        'username': next(str_generator),
        'password': next(str_generator),
    }
    response = client.post(
        signup_url,
        data=json.dumps(data),
        content_type='application/json'
    )
    payload = response.json
    assert response.status_code == 201, payload
    assert 'success' in payload, payload
