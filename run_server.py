import flask
from telebot import types
import os

server = flask.Flask(__name__) #мой код начало

APP_NAME = 'botproxys'
TOKEN = '1237531967:AAH68xo2IzAVnt1s2SZZ6Y542L8Hcb-WHcM'
bot = telebot.TeleBot("1237531967:AAH68xo2IzAVnt1s2SZZ6Y542L8Hcb-WHcM")
 
@server.route('/' + TOKEN, methods=['POST'])
def get_message():
    bot.process_new_updates([types.Update.de_json(
         flask.request.stream.read().decode("utf-8"))])
    return "!", 200
 
 
@server.route('/', methods=["GET"])
def index():
    bot.remove_webhook()
    bot.set_webhook(url="https://{}.herokuapp.com/{}".format(APP_NAME, TOKEN))
    return "Hello from Heroku!", 200
 
 
if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000))) #мой код конец
