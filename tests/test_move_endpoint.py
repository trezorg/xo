import json

from app.services.game.game import store_move
from app.xo.board import Board
from app.xo.enum import Player
from app.xo.types import GameMove

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
    assert response.status_code == 201, payload
    assert 'row' in payload
    assert 'column' in payload


def test_moves_till_game_finished(client, move_url, db_game, auth_header):
    game, moves = db_game
    size = game.size
    moves_set = {(move.row, move.column) for move in moves}
    request_row, request_column = -1, -1
    # find free cell
    for row in range(size):
        for column in range(size):
            if (row, column) not in moves_set:
                request_row, request_column = row, column
                break

    required_turns = size ** 2 - len(moves_set)
    number_of_requests = sum(divmod(required_turns, 2))

    for turn in range(number_of_requests):

        moves_set.add((request_row, request_column))

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

        if 'moves' in payload:
            # game finished
            assert payload['finished_at']
            json_moves = payload['moves']
            moves = [GameMove(**move) for move in json_moves]
            board = Board.from_storage(size, moves)
            assert board.is_over
            break
        else:
            # move response
            assert response.status_code == 201, payload
            assert 'row' in payload, payload
            assert 'column' in payload, payload
            moves_set.add((payload['row'], payload['column']))

        for row in range(size):
            for column in range(size):
                if (row, column) not in moves_set:
                    request_row, request_column = row, column
                    break
