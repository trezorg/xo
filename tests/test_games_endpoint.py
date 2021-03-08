
def test_game_list_endpoint_default_pagination(client, games_url, db_game, auth_header):
    game, _ = db_game
    response = client.get(games_url, headers=auth_header)
    payload = response.json
    assert response.status_code == 200
    assert 'games' in payload, payload
    games = payload['games']
    assert len(games) == 1, payload
    assert 'page' in payload, payload
    assert payload['page']['page'] == 1, payload


def test_game_list_endpoint_exceeded_pagination(client, games_url, db_game, auth_header):
    game, _ = db_game
    page = 3
    response = client.get(f'{games_url}?page={page}', headers=auth_header)
    payload = response.json
    assert response.status_code == 200
    assert 'games' in payload, payload
    games = payload['games']
    assert not games, payload
