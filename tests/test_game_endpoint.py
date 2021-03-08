import random

from flask import url_for


def test_game_absent(client, auth_header):
    rand_game_id = random.randint(100000, 10000000)
    game_url = url_for('game', game_id=rand_game_id)
    response = client.get(game_url, headers=auth_header)
    payload = response.json
    assert response.status_code == 403
    assert 'error' in payload, payload


def test_game(client, game_url, db_game, auth_header):
    game, _ = db_game
    response = client.get(game_url, headers=auth_header)
    payload = response.json
    assert response.status_code == 200
    assert 'moves' in payload, payload
    assert payload['id']
