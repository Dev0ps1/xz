import requests
import os
from bs4 import BeautifulSoup as bs
import threading
from datetime import datetime, timedelta
import telebot
import time
import random
import flask
from telebot import types

bot = telebot.TeleBot('1237531967:AAH68xo2IzAVnt1s2SZZ6Y542L8Hcb-WHcM')

TOKEN = '1237531967:AAH68xo2IzAVnt1s2SZZ6Y542L8Hcb-WHcM'

chat_ids_file = 'chat_ids.txt'

ADMIN_CHAT_ID = 1019817991

users_amount = [0]
threads = list()
THREADS_AMOUNT = [0]
types = telebot.types
bot = TeleBot(TOKEN)
running_spams_per_chat_id = []

def ProxyParsing():
    proxyList = open("proxy.txt", "a")  # Создаем файл для прокси с атрибутом "a"
    request = requests.get("http://foxtools.ru/Proxy")  # Открываем ссылку
    pages = bs(request.content, 'lxml').find('div', attrs={'class': 'pager'})
    pages = pages.find_all('a')[-1].text  # получаем номер последней страницы
    for page in range(1, int(pages) + 1):  # Проходим по каждой странице
        url = "http://foxtools.ru/Proxy?page=" + str(page)
        print(url)
        request = requests.get(url)  # Открываем ссылку

        if request.status_code == 200:  # Проверка на подключение
            s = bs(request.content, 'lxml')  # Получаем весь html код страницы
            table = s.find('table', attrs={"id": "theProxyList"}).tbody  # выделяем тело таблицы с прокси
            trs = table.find_all('tr')  # Ищем теги tr
            for tr in trs:
                # Перебираем tr и ищем в нем input атрибутам "class": "ch", и получаем значение, то есть прокси
                inp = tr.find('input', attrs={'class': 'ch'})['value']
                proxyList.write(inp + "\n")  # Добавляем прокси в файл
            print('GOOD')
        else:
            print('ERROR')
    proxyList.close()  # закрываем файл с прокси
    global proxyread  # делаем переменную глобальной, чтобы можно было закрыть после функции
    proxyread = open("proxy.txt")  # читаем файл с прокси
    return proxyread  # Возвращает файл прокси

def save_chat_id(chat_id):
    "Функция добавляет чат айди в файл если его там нету"
    chat_id = str(chat_id)
    with open(chat_ids_file,"a+") as ids_file:
        ids_file.seek(0)

        ids_list = [line.split('\n')[0] for line in ids_file]

        if chat_id not in ids_list:
            ids_file.write(f'{chat_id}\n')
            ids_list.append(chat_id)
            print(f'New chat_id saved: {chat_id}')
        else:
            print(f'chat_id {chat_id} is already saved')
        users_amount[0] = len(ids_list)
    return

def send_message_users(message):

    def send_message(chat_id):
        data = {
            'chat_id': chat_id,
            'text': message
        }
        response = requests.post(f'https://api.telegram.org/bot{TOKEN}/sendMessage', data=data)




























    with open(chat_ids_file, "r") as ids_file:
        ids_list = [line.split('\n')[0] for line in ids_file]

    [send_message(chat_id) for chat_id in ids_list]
    bot.send_message(ADMIN_CHAT_ID, f"сообщение успешно отправлено всем ({users_amount[0]}) пользователям бота!")

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    boom = types.KeyboardButton(text='Получить прокси!')
    info = types.KeyboardButton(text='🤖Информация')
    stats = types.KeyboardButton(text='📈Статистика')

    buttons_to_add = [boom, info, stats]

    if int(message.chat.id) == ADMIN_CHAT_ID:
        buttons_to_add.append(types.KeyboardButton(text='🔥Рассылка'))
        buttons_to_add.append(types.KeyboardButton(text='addbl'))
        buttons_to_add.append(types.KeyboardButton(text='delbl'))


    keyboard.add(*buttons_to_add)
    bot.send_message(message.chat.id, 'Добро пожаловать!\nЯ на yougame.biz - yougame.biz/members/165883\nВыбери действие:',  reply_markup=keyboard)
    save_chat_id(message.chat.id)

@bot.message_handler(commands=['GET', 'Get', 'get'])  # Создаем команду
def sendMessage(message):  # Создаем функцию команды
        bot.send_document(message.chat.id, ProxyParsing())  # отправляем файл
        proxyread.close()  # убираем файл прокси из памяти
        os.remove("proxy.txt")  # удаляем файл прокси

@bot.message_handler(content_types=['text'])
def handle_message_received(message):
    chat_id = int(message.chat.id)
    text = message.text

    if text == '🤖Информация':
        bot.send_message(chat_id, 'Создатель бота: @AlphaES1\n<b>httpProxys_bot\n\nПо вопросам сотрудничества обращаться в ЛС к создателю бота\n\n Профиль создателя на yougame.biz : yougame.biz/members/165883 </b>', parse_mode='HTML')

    if text == 'Получить прокси!':
        bot.send_message(chat_id, '<b>Привет,чтобы получить бесплатные http прокси напиши боту команду /get</b>', parse_mode='HTML')

    elif text == '📈Статистика':
        bot.send_message(chat_id, f'📊Статистика отображается в реальном времени📡!\nПользователей🙎‍♂: {users_amount[0]}<b>\nБот запущен: 24.04.2020</b>', parse_mode='HTML')

    elif text == '🔥Рассылка' and chat_id==ADMIN_CHAT_ID:
        bot.send_message(chat_id, 'Введите сообщение в формате: "РАЗОСЛАТЬ: ваш_текст" без кавычек')

    elif text == 'addbl':
        addbl(message)

    elif text == 'delbl':
        delbl(message)

    elif 'РАЗОСЛАТЬ: ' in text and chat_id==ADMIN_CHAT_ID:
        msg = text.replace("РАЗОСЛАТЬ: ","")
        send_message_users(msg)


bot.polling()  # Прослушивание бота
 
bot() # Вызываем функцию
