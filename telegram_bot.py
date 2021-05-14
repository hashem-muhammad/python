import telebot
import re
import os
import pafy
from __future__ import unicode_literals


token = "token"
bot = telebot.TeleBot(token)
owner = 'HashemMuhammad'


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id, "welcom to song bot by Hashem\n just send song link on youtube")


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(
        message.chat.id, "for any help plasae tell my owner " + "@" + owner)


@bot.message_handler(content_types=["text"])
def link(message):
    link = message.text
    if link.find('youtu') != -1:
        video = pafy.new(link)
        best = video.getbestaudio(preftype="m4a")
        best.download(quiet=False)
        name = video.title
        file_download = open(name + '.' + best.extension, 'r+b')
        bot.send_audio(message.chat.id, file_download)
    else:
        print('link not correct !')


bot.polling(none_stop=False, interval=0, timeout=20)
