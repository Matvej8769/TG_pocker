import sqlalchemy
import random
from .db_session import SqlAlchemyBase


help_list = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
help_l_combo = ['Hight Card', 'Pair', 'Two Pair', 'Three of a Kind', 'Straight', 'Flush', 'Full House',
                'Four of a Kind', 'Straight Flush', 'Royal Flush']


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
    is_bet = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)

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

    def get_hand(self):
        if self.card1:
            return [self.card1, self.card2]
        return []

    def check_combo(self, room):
        per_hand = room.get_cards() + [self.card1, self.card2]
        per_numbs, per_nominal = [], []
        self.combo, self.chance = None, 0
        for c in per_hand:
            per_numbs.append(c[0:-1])
            per_nominal.append(c[-1])
        for i in range(len(per_hand)):
            for j in range(len(per_hand) - i - 1):
                if help_list.index(per_numbs[j]) > help_list.index(per_numbs[j + 1]):
                    per_numbs[j], per_numbs[j + 1] = per_numbs[j + 1], per_numbs[j]
                    per_nominal[j], per_nominal[j + 1] = per_nominal[j + 1], per_nominal[j]

        if '10' in per_numbs and 'J' in per_numbs and 'Q' in per_numbs and 'K' in per_numbs and 'A' in per_numbs \
                and per_nominal[per_numbs.index('10')] == per_nominal[per_numbs.index('J')] == \
                per_nominal[per_numbs.index('Q')] == per_nominal[per_numbs.index('K')] == \
                per_nominal[per_numbs.index('A')] and not bool(self.combo):
            self.combo = 'Royal Flush'
            self.chance = '~0.00015%'

        counts_street = [0]
        counts_flush = [0]
        for i in range(len(per_numbs) - 1):
            if help_list.index(per_numbs[i]) + 1 == help_list.index(per_numbs[i + 1]):
                counts_street[-1] += 1
                if per_nominal[i] == per_nominal[i + 1]:
                    counts_flush[-1] += 1
            elif per_numbs[i] == per_numbs[i + 1]:
                pass
            else:
                counts_street.append(0)
                counts_flush.append(0)
        for i in range(len(counts_street)):
            if counts_street[i] >= 4 and counts_flush[i] >= 4 and not bool(self.combo):
                self.combo = 'Straight Flush'
                self.chance = '~0.001%'
                break

        flag_three = False
        flag_two = False
        flag_two_pair = False
        for i in range(len(per_hand) - 1):
            if per_numbs.count(per_numbs[i]) == 4 and not bool(self.combo):
                self.combo = 'Four of a Kind'
                self.chance = '~0.02%'
                break
            elif per_numbs.count(per_numbs[i]) == 3:
                flag_three = True
            elif per_numbs.count(per_numbs[i]) == 2:
                if flag_two and per_numbs[i] == per_numbs[i + 1]:
                    flag_two_pair = True
                flag_two = True

        if flag_three and flag_two and not bool(self.combo):
            self.combo = 'Full House'
            self.chance = '~0.14%'

        for nom in per_nominal:
            if per_nominal.count(nom) >= 5 and not bool(self.combo):
                self.combo = 'Flush'
                self.chance = '~0.19%'
                break

        for i in range(len(counts_street)):
            if counts_street[i] >= 4 and not bool(self.combo):
                self.combo = 'Straight'
                self.chance = '~0.39%'
                break

        if flag_three and not bool(self.combo):
            self.combo = 'Three of a Kind'
            self.chance = '~2.13%'

        if flag_two_pair and not bool(self.combo):
            self.combo = 'Two Pair'
            self.chance = '~4.79%'

        if flag_two and not bool(self.combo):
            self.combo = 'Pair'
            self.chance = '~42.58%'

        if not bool(self.combo):
            self.combo = 'Hight Card'
            self.chance = '100%'
