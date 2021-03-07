import json


def test_signin_bad_request_no_password(client, signin_url):
    data = {
        'username': 'test'
    }
    response = client.post(
        signin_url,
        data=json.dumps(data),
        content_type='application/json'
    )
    assert response.status_code == 400, data
    payload = response.json
    assert 'error' in payload
    assert 'status_code' in payload
    assert 'description' in payload


def test_signin_wrong_password(client, signin_url, db_user):
    data = {
        'username': db_user.login,
        'password': db_user.password + 'x',
    }
    response = client.post(
        signin_url,
        data=json.dumps(data),
        content_type='application/json'
    )
    payload = response.json
    assert response.status_code == 400, payload
    assert 'error' in payload, payload


def test_signin(client, signin_url, db_user):
    data = {
        'username': db_user.login,
        'password': db_user.password,
    }
    response = client.post(
        signin_url,
        data=json.dumps(data),
        content_type='application/json'
    )
    payload = response.json
    assert response.status_code == 200, payload
    assert 'access_token' in payload, payload
