import os
import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import document_searcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

token = os.environ['TOKEN']
updater = Updater(token=token, use_context=True)

dispatcher = updater.dispatcher

def start(update, context):
    print(update.message.chat_id)
    context.bot.send_message(chat_id=update.message.chat_id, 
                             text="I'm a bot, please talk to me!")
                             
def echo(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, 
                             text=update.message.text)
                             
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)

def search(update, context):
    print('search')
    context.bot.send_message(chat_id=update.message.chat_id, 
                         text='Стартую поиск...')
    ds = DocumentSearcher()
    for progress in ds.search():
        context.bot.send_message(chat_id=update.message.chat_id, 
                         text=f"Выполнено: {progress}%")
    context.bot.send_message(chat_id=update.message.chat_id, 
                         text='Поиск закончен !')
        

def caps(update, context):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.message.chat_id, text=text_caps)

caps_handler = CommandHandler('caps', caps)
dispatcher.add_handler(caps_handler)

updater.start_polling()
updater.idle()




