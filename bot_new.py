import telebot
from telebot import types

import mine_token

bot = telebot.TeleBot(mine_token.get_token())


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start\n' + str(message.chat.id))


@bot.message_handler(commands=['game'])
def game_command(message):
    keyboard = types.InlineKeyboardMarkup()
    key_start = types.InlineKeyboardButton(text="Start", callback_data="start")
    keyboard.add(key_start)
    key_start = types.InlineKeyboardButton(text="Cancel", callback_data="cancel")
    keyboard.add(key_start)
    bot.reply_to(message, text='Should we begin?', reply_markup=keyboard)
    # bot.send_message(message.from_user.id, text='Should we begin?', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def should_we_start(call):
    if call.data == 'start':
        msg = '5432'
        bot.send_message(call.message.chat.id, msg)
    elif call.data == 'cancel':
        bot.send_message(call.message.chat.id, "OK")


# @bot.message_handler(commands=['help'])
# def start_message(message):
#     bot.reply_to(message, 'Привет, ты написал мне /help\n')
#     keyboard_start = telebot.types.ReplyKeyboardMarkup(True, True)
#     keyboard_start.row('Start', 'Cancel')
#     bot.send_message(message.chat.id, "Начнем?", reply_markup=keyboard_start)


@bot.message_handler(content_types=['text'])
def chat_id(message):
    print('got message ' + str(message))
    bot.send_message(message.chat.id, 'Chat ID: ' + str(message.chat.id))


@bot.channel_post_handler(content_types=['text'])
def chat_id(message):
    print('got channel post' + str(message))
    bot.send_message(message.chat.id, 'Chat ID: ' + str(message.chat.id))


bot.polling()
