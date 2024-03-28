import sqlalchemy
import random
from .db_session import SqlAlchemyBase
from .users import User


help_list = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
help_l_combo = ['Hight Card', 'Pair', 'Two Pair', 'Three of a Kind', 'Straight', 'Flush', 'Full House',
                'Four of a Kind', 'Straight Flush', 'Royal Flush']


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
    first_step = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    bet = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    flag_bet = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    is_first_game = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    is_game_started = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    # настройки
    cash = sqlalchemy.Column(sqlalchemy.Integer, default=1000)
    min_pot = sqlalchemy.Column(sqlalchemy.Integer, default=50)
    max_players = sqlalchemy.Column(sqlalchemy.Integer, default=100)

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
        self.first_step = 0
        self.flag_bet = False
        self.is_game_started = True
        self.bet = 0
        self.pot = 0

    def get_cards(self):
        if self.card1:
            cards = [self.card1, self.card2, self.card3]
            if self.card4:
                cards.append(self.card4)
            if self.card5:
                cards.append(self.card5)
            return cards
        return []

    def give_card(self, per_cards):
        if not self.card4:
            self.card4 = random.choice(per_cards)
            del per_cards[per_cards.index(self.card4)]
        elif not self.card5:
            self.card5 = random.choice(per_cards)
            del per_cards[per_cards.index(self.card5)]

    def finish(self, players, bot, db_sess, room):
        for p in players:
            bot.send_message(p.id, 'Игра окончена, проводим подстчёт результатов...')
        combs = []
        for p in players:
            p.check_combo(room)
            db_sess.commit()
            combs.append(p.combo)
        for p in players:
            for p2 in players:
                bot.send_message(p2.id, f'Игрок {p.name}:\n'
                                        f'Коомбинация: {p.combo}.\n'
                                        f'Вероятность: {p.chance}.')
        best_combo = max(combs, key=lambda x: help_l_combo.index(x))
        winners = db_sess.query(User).filter(User.combo == best_combo, User.room == self.id,
                                             User.is_fold == False).all()
        n = len(winners)
        for p in winners:
            p.cash += self.pot // n
            for p2 in players:
                bot.send_message(p2.id, f'Игрок {p.name} победил! Он получает {self.pot // n} от общего выигрыша!')
        self.is_first_game = False
        self.is_game_started = False
        self.clear()
        db_sess.commit()
        for p in players:
            bot.send_message(p.id, 'Если хотите продолжить игру, введите /start_game.')
