from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Sequence,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM

from .base import Base
from ..constant import DEFAULT_GAME_SIZE
from ..xo.enum import Player


class User(Base):

    __tablename__ = 'user'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    login = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    games = relationship("Game", back_populates="user")

    def __repr__(self):
        return f"<User(login='{self.login}')>"


class Game(Base):

    __tablename__ = 'game'

    id = Column(Integer, Sequence('game_id_seq'), primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False, index=True)
    finished_at = Column(DateTime(timezone=True), nullable=True, default=None)
    winner = Column('winner', ENUM(Player, name='player_enum'), nullable=True)
    size = Column(Integer, nullable=False, default=DEFAULT_GAME_SIZE)
    user = relationship("User", back_populates="games")
    moves = relationship("Move", back_populates="game")

    @property
    def is_over(self):
        return self.finished_at is not None


class Move(Base):

    __tablename__ = 'move'

    id = Column(Integer, Sequence('move_id_seq'), primary_key=True)
    game_id = Column(Integer, ForeignKey('game.id', ondelete="CASCADE"), nullable=False)
    position = Column(Integer, nullable=False)
    player = Column('player', ENUM(Player, name='player_enum'), nullable=False)
    order = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    game = relationship("Game", back_populates="moves")
    UniqueConstraint('game_id', 'order', name='game_order_uniq')
