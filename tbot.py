#!/usr/bin/env python3

import os
import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from document_searcher import DocumentSearcher

logging.basicConfig(filename='tbot.log',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update, context):
    id = update.message.chat_id
    user = update.message.from_user
    user = update.effective_user.id
    logger.info(f"/start: {user}")
    print(f"/start: {user}")
    context.bot.send_message(chat_id=update.message.chat_id, 
                             text='Введите одно или несколько '
                              'слов для поиска (через пробел).')

def echo(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, 
                             text=update.message.text)

def search(update, context):
    bot = context.bot
    id = update.message.chat_id
    print('search')
    bot.send_message(chat_id=id, 
                         text='Стартую поиск...')
    ds = DocumentSearcher()
    print(f'ds: {ds}')
    for progress in ds.search():
        bot.send_message(chat_id=id, text=f"Выполнено: {progress}%")
    bot.send_message(chat_id=id, text='Поиск закончен !')
    bot.send_document(chat_id=id, document=open('venv/pyvenv.cfg', 'rb'))

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    """Start the bot."""
    token = os.environ['TOKEN']

    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    
    dispatcher.add_handler(CommandHandler('search', search))
    
    echo_handler = MessageHandler(Filters.text, echo)
    dispatcher.add_handler(echo_handler)
    
    dispatcher.add_handler(MessageHandler(Filters.text, echo))
    dispatcher.add_error_handler(error)

    print('Starting')
    updater.start_polling()
    updater.idle()
        
if __name__ == '__main__':
    main()



