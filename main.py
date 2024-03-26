import telebot
import random

from data import db_session
from data.users import User

bot = telebot.TeleBot('6262493627:AAGhW1QAWBkE1niyqgvtP-exbu_xBTscqVM')

cards = ['2♠', '3♠', '4♠', '5♠', '6♠', '7♠', '8♠', '9♠', '10♠', 'J♠', 'Q♠', 'K♠', 'A♠',
         '2♥', '3♥', '4♥', '5♥', '6♥', '7♥', '8♥', '9♥', '10♥', 'J♥', 'Q♥', 'K♥', 'A♥',
         '2♣', '3♣', '4♣', '5♣', '6♣', '7♣', '8♣', '9♣', '10♣', 'J♣', 'Q♣', 'K♣', 'A♣',
         '2♦', '3♦', '4♦', '5♦', '6♦', '7♦', '8♦', '9♦', '10♦', 'J♦', 'Q♦', 'K♦', 'A♦']
per_cards = cards.copy()
help_list = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
help_l_combo = ['Hight Card', 'Pair', 'Two Pair', 'Three of a Kind', 'Straight', 'Flush', 'Full House',
                'Four of a Kind', 'Straight Flush', 'Royal Flush']


@bot.message_handler(commands=['start'])
def start(mess):
    bot.send_message(mess.chat.id, 'Добро пожаловать в TgPocker! Версия игры: 0.0')
    db_sess = db_session.create_session()
    if not db_sess.query(User).filter(User.id == mess.chat.id).first():
        user = User(
            id=mess.chat.id,
            name=mess.from_user.first_name
        )
        db_sess.add(user)
        db_sess.commit()
        bot.send_message(mess.chat.id, f'Регистрация пользователя прошла успешно. Ваше игровое имя: {user.name}. '
                                       f'Если хотите поменять игровое имя, введите команду "/set_name <новое_имя>"')
    bot.send_message(mess.chat.id, 'Чтобы создать комнату, введите команду "/new_game". Чтобы войти в существующую '
                                   'комнату, введите команду "/join <id_комнаты>".')


@bot.message_handler(commands=['set_name'])
def set_name(mess):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == mess.chat.id).first()
    user.name = mess.text.split()[1]
    db_sess.commit()
    bot.send_message(mess.chat.id, f'Имя успешно изменено на {user.name}.')


def main():
    db_session.global_init('db/pocker.db')


if __name__ == '__main__':
    main()
    bot.polling(none_stop=True)
