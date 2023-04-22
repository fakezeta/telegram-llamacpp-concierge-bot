from dotenv import load_dotenv
import telebot
from models.chatWithTools import ChatWithTools
from pathlib import Path
from io import BytesIO
import os

load_dotenv()
work_dir = "./tmp"

if "TELEGRAM_TOKEN" not in os.environ or "TELEGRAM_TOKEN" not in os.environ:
    raise AssertionError("Please configure TELEGRAN_TOKEN as environment variables or in .env file")

telegram_token = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(telegram_token, parse_mode=None)

#model = ChatWithTools()

if not os.path.exists(work_dir):
    os.makedirs(work_dir)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,"Hello! I'm a bot that can talk to the AI. Send me a message!")

@bot.message_handler(commands=['stop'])
def stop(message):
    bot.send_message(message.chat.id,"Stopping...")
    bot.stop()

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id,"Send me a message and I'll give it to the AI!")

@bot.message_handler(commands=["status"])
def status(message):
    bot.send_message(message.chat.id,"I'm running!")

@bot.message_handler(commands=["ping"])
def ping(message):
    bot.send_message(message.chat.id,"Pong!")

@bot.message_handler(func=lambda message: True)
def chat(message):
    if not message.text:
        bot.reply_to(message, "Please send a text message.")
        return

    print("Input: ", message.text)

    last_message = bot.send_message(message.chat.id,"typing",disable_notification= True)
    try:
        response = model.call(message.text)
        response=message.text
        bot.delete_message(message.chat.id,last_message.id)
        bot.send_message(message.chat.id,response)
    except Exception as error:
        print(error)

        bot.send_message(message.chat.id,"Whoops! There was an error while talking to OpenAI. Error: " + str(error))

bot.infinity_polling()