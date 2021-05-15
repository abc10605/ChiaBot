import abc
import datetime
import logging

from telegram import Bot
from telegram.ext import Filters, MessageHandler, Updater


class Telebot(abc.ABC):
    def __init__(self, chat_id: str, bot_token: str):
        self.chat_id = chat_id
        self.bot = Bot(bot_token)
        self.updater = Updater(token=bot_token)
        self.dispatcher =self.updater.dispatcher
        self.dispatcher.add_handler(
            MessageHandler(Filters.text, self.message_handler)
        )
        self.dispatcher.add_error_handler(self.error_handler)
        self.add_handler()
        self.add_reply_markup()
        self.starting_message()
        self.updater.start_polling()
        self.updater.idle()
        
    @abc.abstractmethod
    def starting_message(self):
        return NotImplemented
    
    @abc.abstractmethod
    def add_handler(self):
        return NotImplemented
    
    @abc.abstractmethod
    def add_reply_markup(self):
        return NotImplemented
    
    @abc.abstractmethod
    def send_text(self):
        return NotImplemented
    
    @abc.abstractmethod
    def message_handler(self):
        return NotImplemented
    
    @abc.abstractmethod
    def error_handler(self):
        return NotImplemented
    @abc.abstractmethod
    def reply_to_text(self):
        return NotImplemented
    