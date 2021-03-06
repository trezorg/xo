from app.xo.enum import Winner


def test_winner_enum():
    assert Winner.computer
    assert Winner.player
    assert not Winner.none
