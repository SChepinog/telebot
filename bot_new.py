import telebot
from telebot import types

import mine_token
from game_container import Game

bot = telebot.TeleBot(mine_token.get_token())
game = Game()


def get_current_game():
    return game


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start\n' + str(message.chat.id))


@bot.message_handler(commands=['stop'])
def stop_command(message):
    if get_current_game().is_started:
        get_current_game().stop()
        bot.send_message(message.chat.id, 'Game has stopped. Secret was ' + get_current_game().secret)
    else:
        bot.send_message(message.chat.id, 'There is no game to stop')


@bot.message_handler(commands=['game'])
def game_command(message):
    keyboard = types.InlineKeyboardMarkup()
    key_start = types.InlineKeyboardButton(text="Start", callback_data="start")
    keyboard.add(key_start)
    key_start = types.InlineKeyboardButton(text="Cancel", callback_data="cancel")
    keyboard.add(key_start)
    bot.reply_to(message, text='Should we begin?', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def should_we_start(call):
    if call.data == 'start':
        if get_current_game().is_started:
            bot.send_message(call.message.chat.id, 'Game is started already')
        else:
            get_current_game().start()
            print("Game is started with user " + call.from_user.first_name + " " + call.from_user.last_name
                  + " (" + call.from_user.username + "). Secret is " + get_current_game().secret)
            bot.send_message(call.message.chat.id, 'Game has begun!')
    elif call.data == 'cancel':
        bot.send_message(call.message.chat.id, "OK")


@bot.message_handler(content_types=['text'])
def chat_id(message):
    if get_current_game().is_started:
        result = get_current_game().try_string(message.text)
        bot.send_message(message.chat.id, str(result))
    else:
        print('got message ' + str(message))
        bot.send_message(message.chat.id, 'No game is active. This chat ID: ' + str(message.chat.id))


# @bot.message_handler(commands=['help'])
# def start_message(message):
#     bot.reply_to(message, 'Привет, ты написал мне /help\n')
#     keyboard_start = telebot.types.ReplyKeyboardMarkup(True, True)
#     keyboard_start.row('Start', 'Cancel')
#     bot.send_message(message.chat.id, "Начнем?", reply_markup=keyboard_start)


# @bot.message_handler(content_types=['text'])
# def chat_id(message):
#     print('got message ' + str(message))
#     bot.send_message(message.chat.id, 'Chat ID: ' + str(message.chat.id))


# @bot.channel_post_handler(content_types=['text'])
# def chat_id(message):
#     print('got channel post' + str(message))
#     bot.send_message(message.chat.id, 'Chat ID: ' + str(message.chat.id))


bot.polling()
