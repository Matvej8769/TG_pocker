import sqlalchemy
import random
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    room = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("rooms.id"), primary_key=True, default=0)
    card1 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    card2 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    combo = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    chance = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    cash = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    pot = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    is_fold = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)

    def clear(self):
        self.card1, self.card2, self.combo, self.chance = None, None, None, None
        self.cash, self.pot = None, None
        self.is_fold = None

    def init(self, settings, per_cards):
        self.clear()
        self.cash = settings['cash']
        self.give_hand(per_cards)

    def give_hand(self, per_cards):
        self.pot, self.is_fold = 0, False
        self.card1 = random.choice(per_cards)
        del per_cards[per_cards.index(self.card1)]
        self.card2 = random.choice(per_cards)
        del per_cards[per_cards.index(self.card2)]
