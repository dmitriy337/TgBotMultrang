from aiogram import Bot, Dispatcher, executor, types
import asyncio
import requests
from time import sleep
import time
from bs4 import BeautifulSoup
import sqlite3
import datetime
import os
import re

conn = sqlite3.connect('Base.db')
c = conn.cursor()

StartTimeConsole = time.perf_counter()

API_TOKEN = '<YourToken>'
AdminIn = <YourUserId>

try:
    c.execute('''CREATE TABLE BotTrans
             (UserId int, Username text, FirstName text, MessageText text, ResponceMessage text,MessageTime real )''')
except Exception as e:
    pass

try:
    c.execute('''CREATE TABLE BotException
             (UserId int, Username text, FirstName text, MessageText text, ExceptionText text,MessageTime real )''')
except Exception as e:
    pass

headers = {
    "User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}

API_TOKEN = '1041401599:AAG_JPLd8SCgOd-Xp4ppYo7UejgHIfTBAd8'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

LanhEn = list('qwertyuiopasdfghjklzxcvbnm')
LangRu = list('йцукенгшщзхъфывапролджэячсмитьбю')


@dp.message_handler(commands=['stop'])
async def send_welcome(message: types.Message):
    StopBot()


def Stats():
    c.execute("SELECT * FROM BotTrans")
    Notes = []
    for Note in (c.fetchall())[-5:]:
        date_time_obj = datetime.datetime.strptime(
            Note[5], '%Y-%m-%d %H:%M:%S.%f')
        NoteText = f'Usrnm:@{Note[1]},Nknm:{Note[2]}, Zprs:{Note[3]}, Tm:{date_time_obj.strftime("%H:%M:%S")}'
        Notes.append(NoteText)
    return '\n'.join(Notes)

def ExceptionDB(message,Except):
    ExceptL = str(Except).replace('"',"'")
    c.execute(
            f'INSERT INTO BotException (UserId, Username , FirstName , MessageText , ExceptionText ,MessageTime) VALUES({message.chat.id},"{message.chat.username}","{message.chat.first_name}","{message.text}","{ExceptL}","{(datetime.datetime.now())}");')
    conn.commit()

def CountDB():
    c.execute("SELECT * FROM BotTrans")
    Notes = []
    All = len(c.fetchall())
    return All



@dp.message_handler(commands=['stat', 'stats'])
async def send_welcome(message: types.Message):
    try:
        # if str(message.chat.id) ==
        TimeWorking = (StartTimeConsole - time.perf_counter()) * -1
        await message.reply(f'TimeWorking: {time.strftime("%H:%M:%S",time.gmtime(TimeWorking))}\nCountDB: {CountDB()}\nLastDB:(\n{Stats()})')
    except Exception as e:
        await message.reply(f'Exception:\n{e}')


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await bot.send_message(message.chat.id, "SendWord!")


@dp.message_handler(content_types=['text'])
async def send_welcome(message: types.Message):
    try:
        if any(word in message.text for word in LanhEn):  # LangEn
            await EnToRu(message)
        else:  # LangRu
            await RuToEn(message)
    except Exception as e:
        ExceptionDB(message,e)
        await message.reply(f'Ooops!')


async def EnToRu(message):
    try:
        fulls_pager = requests.get(
            (f'https://www.multitran.com/m.exe?l1=2&l2=1&s={str(message.text).lower()}&langlist=1'), headers=headers)
        Page = BeautifulSoup(fulls_pager.content, 'html.parser')
        MainTable = (Page.find('table', width=True))
        ObjGlobal = MainTable.find('td', class_='subj', width=True)
        NameCattegory = (ObjGlobal.find('a')['title'])
        TransGlobal = MainTable.find('td', class_='trans', width=True)
        AllTrans = TransGlobal.find_all('a')
        TransList = []
        for trans in AllTrans:
            TransList.append(trans.text)
        TransListText = ', '.join(TransList)
        MessageText = (f'{NameCattegory}:\n{TransListText}')
        await message.reply(MessageText)
        MessageTextE = str(message.text).replace('"',"'")
        try:
            c.execute(
                f'INSERT INTO BotTrans (UserId, Username , FirstName , MessageText , ResponceMessage ,MessageTime) VALUES({message.chat.id},"{message.chat.username}","{message.chat.first_name}","{MessageTextE}","{TransList}","{(datetime.datetime.now())}");')
            conn.commit()
        except Exception as e:
            await bot.send_message(AdminIn, f'Exception:\n{e}')
            ExceptionDB(message,e)

    except Exception as e:
        ExceptionDB(message,e)
        await message.reply('Ooops!')



async def RuToEn(message):
    try:
        fulls_pager = requests.get(
            (f'https://www.multitran.com/m.exe?l1=2&l2=1&s={str(message.text).lower()}'), headers=headers)
        Page = BeautifulSoup(fulls_pager.content, 'html.parser')
        MainTable = (Page.find('table', width=True))
        ObjGlobal = MainTable.find('td', class_='subj', width=True)
        NameCattegory = (ObjGlobal.find('a')['title'])
        TransGlobal = MainTable.find('td', class_='trans', width=True)
        AllTrans = TransGlobal.find_all('a')
        TransList = []
        for trans in AllTrans:
            TransList.append(trans.text)
        TransListText = ', '.join(TransList)
        MessageText = (f'{NameCattegory}:\n{TransListText}')
        await message.reply(MessageText)
        MessageTextE = str(message.text).replace('"',"'")
        try:
            c.execute(
                f'INSERT INTO BotTrans (UserId, Username , FirstName , MessageText , ResponceMessage ,MessageTime) VALUES({message.chat.id},"{message.chat.username}","{message.chat.first_name}","{MessageTextE}","{TransList}","{(datetime.datetime.now())}");')
            conn.commit()
        except Exception as e:
            await bot.send_message(AdminIn, f'Exception:\n{e}')
            ExceptionDB(message,e)
    except Exception as e:
        ExceptionDB(message,e)
        await message.reply('Ooops!')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
