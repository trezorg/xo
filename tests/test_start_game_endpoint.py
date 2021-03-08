import json


def test_start_game_no_auth_headers(client, start_game_url):
    data = {
        'size': 3
    }
    response = client.post(
        start_game_url,
        data=json.dumps(data),
        content_type='application/json'
    )
    assert response.status_code == 401, data
    payload = response.json
    assert 'error' in payload
    assert 'status_code' in payload
    assert 'description' in payload


def test_start_game_wrong_auth_headers(client, start_game_url, auth_header):
    data = {
        'size': 3
    }
    auth_header['Authorization'] += 'xxx'
    response = client.post(
        start_game_url,
        headers=auth_header,
        data=json.dumps(data),
        content_type='application/json'
    )
    assert response.status_code == 401, data
    payload = response.json
    assert 'error' in payload
    assert 'status_code' in payload
    assert 'description' in payload


def test_start_wrong_board_size(client, start_game_url, auth_header):
    data = {
        'size': 30
    }
    response = client.post(
        start_game_url,
        headers=auth_header,
        data=json.dumps(data),
        content_type='application/json'
    )
    payload = response.json
    assert response.status_code == 400, data
    assert 'error' in payload
    assert 'status_code' in payload
    assert 'description' in payload


def test_start_game(client, start_game_url, auth_header):
    data = {
        'size': 5
    }
    response = client.post(
        start_game_url,
        headers=auth_header,
        data=json.dumps(data),
        content_type='application/json'
    )
    payload = response.json
    assert response.status_code == 201, data
    assert 'id' in payload
    assert 'user_id' in payload
    assert 'moves' in payload
    assert payload['winner'] is None
