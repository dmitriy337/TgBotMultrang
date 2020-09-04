from aiogram import Bot, Dispatcher, executor, types
import asyncio
import requests
from time import sleep
from bs4 import BeautifulSoup

headers = {"User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}

API_TOKEN = 'YourToken'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# https://www.multitran.com/m.exe?s=if&l1=1&l2=2
# https://www.multitran.com/m.exe?l1=1&l2=2&s=%D0%BA%D0%B0%D0%BA

LanhEn = list('qwertyuiopasdfghjklzxcvbnm')
LangRu = list('йцукенгшщзхъфывапролджэячсмитьбю')



@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await bot.send_message(message.chat.id, "SendWord!")


@dp.message_handler(content_types=['text'])
async def send_welcome(message: types.Message):
    try:
        if any(word in message.text for word in LanhEn): #LangEn
            await EnToRu(message)
        else: #LangRu
            await RuToEn(message)
    except Exception as e:
        await message.reply(f'Ooops! Exception: {e}')



async def EnToRu(message):
    fulls_pager = requests.get((f'https://www.multitran.com/m.exe?l1=2&l2=1&s={str(message.text).lower()}&langlist=1'), headers=headers)
    Page = BeautifulSoup(fulls_pager.content,'html.parser')
    MainTable = (Page.find('table',width=True))
    ObjGlobal = MainTable.find('td',class_='subj',width=True)
    NameCattegory = (ObjGlobal.find('a')['title'])
    TransGlobal = MainTable.find('td',class_='trans',width=True)
    AllTrans = TransGlobal.find_all('a')
    TransList = []
    for trans in AllTrans:
        TransList.append(trans.text)
    TransListText = ', '.join(TransList)
    MessageText = (f'{NameCattegory}:\n{TransListText}')
    await message.reply(MessageText)


async def RuToEn(message):
    fulls_pager = requests.get((f'https://www.multitran.com/m.exe?l1=2&l2=1&s={str(message.text).lower()}'), headers=headers)
    Page = BeautifulSoup(fulls_pager.content,'html.parser')
    MainTable = (Page.find('table',width=True))
    ObjGlobal = MainTable.find('td',class_='subj',width=True)
    NameCattegory = (ObjGlobal.find('a')['title'])
    TransGlobal = MainTable.find('td',class_='trans',width=True)
    AllTrans = TransGlobal.find_all('a')
    TransList = []
    for trans in AllTrans:
        TransList.append(trans.text)
    TransListText = ', '.join(TransList)
    MessageText = (f'{NameCattegory}:\n{TransListText}')
    await message.reply(MessageText)




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)



 
