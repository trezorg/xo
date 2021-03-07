import json

from app.services.game.game import store_move
from app.xo.enum import Player

default_data = {
    'row': 2,
    'column': 2,
    'game_id': 1,
}


def test_move_no_auth_headers(client, move_url):
    response = client.post(
        move_url,
        data=json.dumps(default_data),
        content_type='application/json'
    )
    assert response.status_code == 401, default_data
    payload = response.json
    assert 'error' in payload
    assert 'status_code' in payload
    assert 'description' in payload


def test_move_wrong_auth_headers(client, move_url, auth_header):
    auth_header['Authorization'] += 'xxx'
    response = client.post(
        move_url,
        headers=auth_header,
        data=json.dumps(default_data),
        content_type='application/json'
    )
    assert response.status_code == 401, default_data
    payload = response.json
    assert 'error' in payload
    assert 'status_code' in payload
    assert 'description' in payload


def test_move_over_board_boundary(client, move_url, db_game, auth_header):
    game, _ = db_game
    data = {
        'row': game.size + 1,
        'column': 2,
        'game_id': game.id,
    }
    response = client.post(
        move_url,
        headers=auth_header,
        data=json.dumps(data),
        content_type='application/json'
    )
    payload = response.json
    assert response.status_code == 400, data
    assert 'error' in payload
    assert 'status_code' in payload
    assert 'description' in payload


def test_move_occupied_cell(app, client, move_url, db_game, auth_header):
    game, _ = db_game
    session = app.config['session']()
    store_move(session, game.id, 0, Player.player, commit=True)
    data = {
        'row': 0,
        'column': 0,
        'game_id': game.id,
    }
    response = client.post(
        move_url,
        headers=auth_header,
        data=json.dumps(data),
        content_type='application/json'
    )
    payload = response.json
    assert response.status_code == 400, data
    assert 'error' in payload
    assert 'status_code' in payload
    assert 'description' in payload


def test_move(client, move_url, db_game, auth_header):
    game, moves = db_game
    size = game.size
    moves_set = {(move.row, move.column) for move in moves}
    request_row, request_column = -1, -1
    for row in range(size):
        for column in range(size):
            if (row, column) not in moves_set:
                request_row, request_column = row, column
                break
    data = {
        'row': request_row,
        'column': request_column,
        'game_id': game.id,
    }
    response = client.post(
        move_url,
        headers=auth_header,
        data=json.dumps(data),
        content_type='application/json'
    )
    payload = response.json
    assert response.status_code == 201, data
    assert 'row' in payload
    assert 'column' in payload
