import sqlalchemy
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    # room = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("rooms.id"))
    card1 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    card2 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    combo = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    chance = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    cash = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    pot = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    is_fold = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
