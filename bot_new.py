import logging
import sys

import telebot
from telebot import types

import game_container
import mine_token
from game_container import Game

bot = telebot.TeleBot(mine_token.get_token())
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start\n' + str(message.chat.id))


@bot.message_handler(commands=['stop'])
def stop_command(message):
    user_id = str(message.from_user.id)
    game: Game = game_container.get_game_for_user(user_id)
    if game.is_started:
        game.stop()
        bot.send_message(message.chat.id, 'Game has stopped. Secret was '
                         + game.secret)
        logging.info('User ' + str(message.from_user.username) + ' has stopped game')
        keyboard = get_start_game_keyboard()
        bot.send_message(message.chat.id, text='Again?', reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, 'You have no active game')
        game_command(message)


@bot.message_handler(commands=['game'])
def game_command(message):
    keyboard = get_start_game_keyboard()
    bot.reply_to(message, text='Should we begin?', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'start')
def start_callback_handler(call):
    user_id = str(call.from_user.id)
    game: Game = game_container.get_game_for_user(user_id)
    if game.is_started:
        bot.send_message(call.message.chat.id, 'Game is started already')
    else:
        game.start()
        logging.info(
            "Game is started with user " + str(call.from_user.first_name) + " " + str(call.from_user.last_name)
            + " (" + str(call.from_user.username) + "). Secret is "
            + game.secret)
        bot.send_message(call.message.chat.id, 'Game has begun!')


@bot.callback_query_handler(func=lambda call: call.data == 'cancel')
def cancel_handler(call):
    bot.send_message(call.message.chat.id, "OK")


@bot.message_handler(content_types=['text'])
def handle_text_message(message):
    user_id = str(message.from_user.id)
    game: Game = game_container.get_game_for_user(user_id)
    if game.is_started:
        result = game.try_string(message.text)
        bot.send_message(message.chat.id, str(result))
        if not game.is_started:
            keyboard = get_start_game_keyboard()
            logging.info('User ' + str(message.from_user.username) + ' has finished game in '
                         + str(game_container.get_game_for_user(user_id).try_count) + ' tries')
            bot.send_message(message.chat.id, text='Again?', reply_markup=keyboard)
    else:
        logging.info('got message ' + str(message))
        bot.send_message(message.chat.id, text='No game is active')
        game_command(message)


def get_start_game_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    key_start = types.InlineKeyboardButton(text="Start", callback_data="start")
    keyboard.add(key_start)
    key_start = types.InlineKeyboardButton(text="Cancel", callback_data="cancel")
    keyboard.add(key_start)
    return keyboard


def polling():
    try:
        bot.polling()
    except:
        logging.exception("Error while polling:", sys.exc_info()[0])
        polling()


polling()
