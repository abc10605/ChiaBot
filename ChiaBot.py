import datetime
import json
import logging
import os
import subprocess
from threading import Timer

from telegram import ReplyKeyboardMarkup, Update
from telegram.ext.callbackcontext import CallbackContext

import Telebot

logging.basicConfig(
            format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level = logging.INFO,
            filename = f'./log/{datetime.date.today()}.log',
            filemode = 'a',
            encoding = 'utf8'
        )
logger = logging.getLogger(name=__name__)
def log(level: int) -> None:
    def decorator(func):
        def wrapper(*args, **kwargs):
            msg = func(*args)
            logger.log(level=level, msg=msg)
        return wrapper
    return decorator


class ChiaBot(Telebot.Telebot):
    def add_handler(self):
        pass
    
    def add_reply_markup(self):
        self.starting_msg_markup = ReplyKeyboardMarkup([['錢包', '耕地'], ['耕種', '節點']], resize_keyboard=True)
        
    @log(logging.INFO)
    def starting_message(self):
        self.send_text( 
            text='Chia機器人已啟動', 
            reply_markup=self.starting_msg_markup
        )
        return "Starting message sended."
    
    def send_text(self, text: str='', reply_markup=None):
        self.updater.bot.send_message(chat_id=self.chat_id, text=text, reply_markup=reply_markup)
    
    @log(logging.INFO)
    def message_handler(self, update: Update, context: CallbackContext):
        msg = update.message
        text = msg.text
        user = msg.from_user['first_name'] + msg.from_user['last_name']
        if text == '錢包':
            reply = subprocess.check_output('chia wallet show', shell=True)
            reply = '\n'.join(list(map(lambda _: _.lstrip(), reply.decode('utf8').split('\r\n')[-4: -1])))
            self.reply_to_text(update, context, reply, user)
        elif text == '耕地':
            reply = subprocess.check_output('chia plots check', shell=True, stderr=subprocess.STDOUT)
            reply = '\n'.join(list(map(lambda _: _.split('\x1b[0m')[1].lstrip(), reply.decode('utf8').split('\r\n')[-3: -1])))
            self.reply_to_text(update, context, reply, user)
        elif text == '耕種':
            for _ in range(1):
                subprocess.check_output('chia plots create --override-k -k 25 -n 1 -b 1024 -t D:\chia_test\ -d D:\chia_test\ -r 2', shell=True)
                Timer(240, subprocess.check_output('chia plots create --override-k -k 25 -n 1 -b 1024 -t D:\chia_test\ -d D:\chia_test\ -r 2', shell=True))
        elif text == '節點':
            reply = subprocess.check_output('chia show -s', shell=True)
            reply = '\n'.join(reply.decode('utf8').split('\r\n')[2: 5])
            self.reply_to_text(update, context, reply, user)
        else:
            pass
        return f'Receive an message {text} from {user}'

    @log(logging.ERROR)
    def error_handler(self, update: Update, context: CallbackContext):
        print(context.error)
    
    @log(logging.INFO)
    def reply_to_text(self, update: Update, context: CallbackContext, text: str='', user: str= None):
        update.message.reply_text(text)
        return f'Bot have replied message to user {user}'
    

token = json.loads(open('./Token.json', 'r').read())
bot = ChiaBot(token['CHATS']['ChiaBot'], token['BOTS']['Hsuan_Test_Bot'])
