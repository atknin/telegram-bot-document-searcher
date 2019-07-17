#!/usr/bin/env python3
import os
import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from nltk.stem.snowball import SnowballStemmer

from document_searcher import DocumentsSearcher

logging.basicConfig(filename='tbot.log',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update, context):
    id = update.message.chat_id
    user = update.message.from_user
    user = update.effective_user.id
    # logger.info(f"/start: {user}")
    context.bot.send_message(chat_id=update.message.chat_id, 
                             text='Введите одно или несколько '
                              'слов для поиска (через пробел).')
'''
def echo(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, 
                             text=update.message.text)
'''
def search(update, context):
    bot = context.bot
    id = update.message.chat_id
                         
    stemmer = SnowballStemmer("russian")
    keyword_list = [stemmer.stem(w).lower() for w in update.message.text.split()]
    
    bot.send_message(chat_id=id, 
                     text="Начинаю поиск по словам: {}".format(keyword_list))
    
    ds = DocumentsSearcher(keyword_list=keyword_list)
    for progress in ds.search():
        bot.send_message(chat_id=id, text="Выполнено: {}%".format(progress))
    if ds.result_list:
        bot.send_message(chat_id=id, text='Поиск закончен, ваши файлы:')
        for d in ds.result_list:
            bot.send_document(chat_id=id, document=open(d, 'rb'))
    else:
        bot.send_message(chat_id=id, text='Поиск закончен, ничего не найдено :-(')

def error(update, context):
    ''' Log Errors caused by Updates '''
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    logger.info('Start')
    token = '974931890:AAHh3S9scYVl7AxvahSIFBJCv2umeJNYT3k'

    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    dispatcher.add_handler(MessageHandler(Filters.text, search))
    dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()
        
if __name__ == '__main__':
    main()




