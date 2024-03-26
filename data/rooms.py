import sqlalchemy
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
