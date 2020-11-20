import telebot
from telebot import types

import mine_token
import game_container

bot = telebot.TeleBot(mine_token.get_token())


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start\n' + str(message.chat.id))


@bot.message_handler(commands=['stop'])
def stop_command(message):
    user_id = str(message.from_user.id)
    if game_container.user_has_game(user_id):
        game_container.get_game_for_user(user_id).stop()
        bot.send_message(message.chat.id, 'Game has stopped. Secret was '
                         + game_container.get_game_for_user(user_id).secret)
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
    user_id = str(call.from_user.id)
    if call.data == 'start':
        if game_container.user_has_game(user_id):
            if game_container.get_game_for_user(user_id).is_started:
                bot.send_message(call.message.chat.id, 'Game is started already')
            else:
                game_container.get_game_for_user(user_id).start()
                print(
                    "Game is started with user " + str(call.from_user.first_name) + " " + str(call.from_user.last_name)
                    + " (" + str(call.from_user.username)
                    + "). Secret is " + game_container.get_game_for_user(user_id).secret)
                bot.send_message(call.message.chat.id, 'Game has begun!')
        else:
            game_container.add_game(user_id)
            game_container.get_game_for_user(user_id).start()
            print(
                "Game is started with user " + str(call.from_user.first_name) + " " + str(call.from_user.last_name)
                + " (" + str(call.from_user.username) + "). Secret is "
                + game_container.get_game_for_user(user_id).secret)
            bot.send_message(call.message.chat.id, 'Game has begun!')
    elif call.data == 'cancel':
        bot.send_message(call.message.chat.id, "OK")


@bot.message_handler(content_types=['text'])
def chat_id(message):
    user_id = str(message.from_user.id)
    if game_container.user_has_game(user_id):
        if game_container.get_game_for_user(user_id).is_started:
            result = game_container.get_game_for_user(user_id).try_string(message.text)
            bot.send_message(message.chat.id, str(result))
        else:
            game_container.add_game(user_id)
            bot.send_message(message.chat.id, 'Error occured. Please try again')
    else:
        print('got message ' + str(message))
        bot.send_message(message.chat.id, 'No game is active. This chat ID: ' + str(message.chat.id))


# @bot.message_handler(commands=['help'])
# def start_message(message):
#     bot.reply_to(message, 'Привет, ты написал мне /help\n')
#     keyboard_start = telebot.types.ReplyKeyboardMarkup(True, True)
#     keyboard_start.row('Start', 'Cancel')
#     bot.send_message(message.chat.id, "Начнем?", reply_markup=keyboard_start)


bot.polling()
