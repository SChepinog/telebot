import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import InlineQueryHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent
import logging

bot_token = ''

bot = telegram.Bot(token=bot_token)
print(bot.get_me())

updater = Updater(token=bot_token, use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


def chat_id(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.effective_chat.id)


chat_id_handler = CommandHandler('chat_id', chat_id)
dispatcher.add_handler(chat_id_handler)


def echo(update, context):
    logging.log(logging.INFO, context)
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)


# def caps(update, context):
#     text_caps = ' '.join(context.args).upper()
#     context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)
#
#
# caps_handler = CommandHandler('caps', caps)
# dispatcher.add_handler(caps_handler)


# def inline_caps(update, context):
#     query = update.inline_query.query
#     if not query:
#         return
#     results = list()
#     results.append(
#         InlineQueryResultArticle(
#             id=query.upper(),
#             title='Caps',
#             input_message_content=InputTextMessageContent(query.upper())
#         )
#     )
#     context.bot.answer_inline_query(update.inline_query.id, results)
#
#
# inline_caps_handler = InlineQueryHandler(inline_caps)
# dispatcher.add_handler(inline_caps_handler)


def inline_chat_id(update, context):
    query = update.inline_query.query
    if not query:
        return
    results = list()
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Chat ID',
            input_message_content=InputTextMessageContent(query)
        )
    )
    context.bot.answer_inline_query(update.inline_query.id, results)


inline_chat_id_handler = InlineQueryHandler(inline_chat_id)
dispatcher.add_handler(inline_chat_id_handler)


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Sorry, I didn't understand that command.\n" + str(context.args))


unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

updater.start_polling()
