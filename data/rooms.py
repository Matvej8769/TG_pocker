import sqlalchemy
import random
from .db_session import SqlAlchemyBase


class Room(SqlAlchemyBase):
    __tablename__ = 'rooms'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    players_count = sqlalchemy.Column(sqlalchemy.Integer)
    card1 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    card2 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    card3 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    card4 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    card5 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    pot = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    step = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    bet = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    flag_bet = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)

    def clear(self):
        self.card1, self.card2, self.card3, self.card4, self.card5 = None, None, None, None, None
        self.pot, self.bet, self.flag_bet, self.step = None, None, None, None

    def init(self, per_cards):
        self.clear()
        self.card1 = random.choice(per_cards)
        del per_cards[per_cards.index(self.card1)]
        self.card2 = random.choice(per_cards)
        del per_cards[per_cards.index(self.card2)]
        self.card3 = random.choice(per_cards)
        del per_cards[per_cards.index(self.card3)]
        self.step = 0
        self.flag_bet = False
