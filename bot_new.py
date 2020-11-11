import telebot
import mine_token

bot = telebot.TeleBot(mine_token.get_token())


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start\n' + str(message.chat.id))


@bot.message_handler(commands=['game'])
def game_command(message):
    keyboard_start = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard_start.row('Start', 'Cancel')
    bot.send_message(message.chat.id, "Начнем?", reply_markup=keyboard_start)


@bot.message_handler(content_types=['text'])
def chat_id(message):
    print('got message ' + str(message))
    bot.send_message(message.chat.id, 'Chat ID: ' + str(message.chat.id))


@bot.channel_post_handler(content_types=['text'])
def chat_id(message):
    print('got channel post' + str(message))
    bot.send_message(message.chat.id, 'Chat ID: ' + str(message.chat.id))


bot.polling()
