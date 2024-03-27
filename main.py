import telebot
import random

from data import db_session
from data.users import User
from data.rooms import Room

bot = telebot.TeleBot('6262493627:AAGhW1QAWBkE1niyqgvtP-exbu_xBTscqVM')

cards = ['2♠', '3♠', '4♠', '5♠', '6♠', '7♠', '8♠', '9♠', '10♠', 'J♠', 'Q♠', 'K♠', 'A♠',
         '2♥', '3♥', '4♥', '5♥', '6♥', '7♥', '8♥', '9♥', '10♥', 'J♥', 'Q♥', 'K♥', 'A♥',
         '2♣', '3♣', '4♣', '5♣', '6♣', '7♣', '8♣', '9♣', '10♣', 'J♣', 'Q♣', 'K♣', 'A♣',
         '2♦', '3♦', '4♦', '5♦', '6♦', '7♦', '8♦', '9♦', '10♦', 'J♦', 'Q♦', 'K♦', 'A♦']
help_list = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
help_l_combo = ['Hight Card', 'Pair', 'Two Pair', 'Three of a Kind', 'Straight', 'Flush', 'Full House',
                'Four of a Kind', 'Straight Flush', 'Royal Flush']

settings = {
    'cash': 1000,
    'min_pot': 50
}


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


@bot.message_handler(commands=['new_game'])
def new_game(mess):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == mess.chat.id).first()
    if not user.room:
        room = Room(
            players_count=1
        )
        db_sess.add(room)
        db_sess.commit()
        user.room = room.id
        db_sess.commit()
        bot.send_message(mess.chat.id, f'Комната успешно создана! Id: {room.id}. Чтобы выйти введите "/exit".')
    else:
        bot.send_message(mess.chat.id, 'Вы уже находитесь в команте. Чтобы выйти введите "/exit".')


@bot.message_handler(commands=['join'])
def join(mess):
    try:
        room_id = int(mess.text.split()[1])
    except Exception:
        bot.send_message(mess.chat.id, 'Введена неправильная команда. ID не является числом.')
        return
    db_sess = db_session.create_session()
    room = db_sess.query(Room).filter(Room.id == room_id).first()
    if not room:
        bot.send_message(mess.chat.id, f'Комната с id {room_id} не найдена.')
        return
    user = db_sess.query(User).filter(User.id == mess.chat.id).first()
    if not user.room:
        room.players_count += 1
        for player in db_sess.query(User).filter(User.room == room_id).all():
            bot.send_message(player.id, f'К комнате присоединился {user.name}! Чтобы начать игру введите "/start_game"')
        user.room = room_id
        db_sess.commit()
        bot.send_message(mess.chat.id, 'Вы успешно присоединились к комнате! Чтобы выйти введите "/exit".')
    else:
        bot.send_message(mess.chat.id, 'Вы уже находитесь в команте. Чтобы выйти введите "/exit".')


@bot.message_handler(commands=['exit'])
def exit(mess):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == mess.chat.id).first()
    if not user.room:
        bot.send_message(mess.chat.id, f'Вы не находитесь в комнате.')
    else:
        room = db_sess.query(Room).filter(Room.id == user.room).first()
        user.room = 0
        room.players_count -= 1
        db_sess.commit()
        if room.players_count == 0:
            db_sess.delete(room)
        db_sess.commit()
        user.clear()
        room.clear()
        db_sess.commit()
        bot.send_message(mess.chat.id, 'Вы вышли из комнаты.')


@bot.message_handler(commands=['start_game'])
def start_game(mess):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == mess.chat.id).first()
    if user.room:
        room = db_sess.query(Room).filter(user.room == Room.id).first()
        if room.players_count >= 1:
            bot.send_message(mess.chat.id, 'Игра запускается...')
            players = db_sess.query(User).filter(User.room == user.room).all()
            per_cards = cards.copy()

            for p in players:
                p.init(settings, per_cards)
                bot.send_message(p.id, f'Ваша колода: {p.card1} | {p.card2}')
                db_sess.commit()

            room.init(per_cards)
            db_sess.commit()
            for p in players:
                bot.send_message(p.id, f'Колода на столе: {room.card1} | {room.card2} | {room.card3}')
        else:
            bot.send_message(mess.chat.id, 'В комнате недостаточно человек!')
    else:
        bot.send_message(mess.chat.id, 'Вы не находитесь в комнате')


@bot.message_handler(commands=['info'])
def info(mess):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == mess.chat.id).first()
    if user.card1:
        room = db_sess.query(Room).filter(user.room == Room.id).first()
        user.check_combo(room)
        db_sess.commit()
        bot.send_message(mess.chat.id, f'Ваша колода: {user.card1} | {user.card2}\n'
                                       f'Колода на столе: {" | ".join(room.get_cards())}\n'
                                       f'Ваша коомбинация: {user.combo}! Шанс выпадения: {user.chance}')
        bot.send_message(mess.chat.id, f'Ваша ставка: {user.pot}\n'
                                       f'Ваш счёт: {user.cash}\n'
                                       f'Общий банк на столе: {room.pot}')
    else:
        bot.send_message(mess.chat.id, 'Вы не находитесь в комнате или игра ещё не началась.')



def main():
    db_session.global_init('db/pocker.db')
    print('Бот запущен')


if __name__ == '__main__':
    main()
    bot.polling(none_stop=True)
