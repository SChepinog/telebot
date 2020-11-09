import telebot

bot = telebot.TeleBot('')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start\n' + str(message.chat.id))


@bot.message_handler(content_types=['text'])
def chat_id(message):
    print(str(message))
    bot.send_message(message.chat.id, 'Chat ID: ' + str(message.chat.id))


@bot.channel_post_handler(content_types=['text'])
def chat_id(message):
    print(str(message))
    bot.send_message(message.chat.id, 'Chat ID: ' + str(message.chat.id))


bot.polling()
