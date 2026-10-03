import os
import requests
from telebot import TeleBot
from flask import Flask
from threading import Thread
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot faol ishlamoqda!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

def keep_alive():
    t = Thread(target=run)
    t.start()

TOKEN = "8877074707:AAH_Jlknum7R9aTQo6WWO91nCAozW2jBR7I"
bot = TeleBot(TOKEN)

JOYLAR = {
    "Pastdarg'om": {"lat": 39.560, "lon": 66.692},
    "Ishtixon": {"lat": 39.966, "lon": 66.486},
    "Kattaqo'rg'on": {"lat": 39.897, "lon": 66.255}
}

@bot.message_handler(commands=['start'])
def start(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for joy in JOYLAR.keys():
        markup.add(KeyboardButton(joy))
    
    # Web App ochadigan inline tugma
    web_app_url = "https://sunnatovasaida8-blip.github.io/namoz-vaqtlari-toza/"
    inline_markup = InlineKeyboardMarkup()
    inline_markup.add(InlineKeyboardButton("📱 Namoz Vaqtlari (Web App)", web_app=WebAppInfo(url=web_app_url)))
    
    bot.send_message(
        message.chat.id, 
        "Assalomu alaykum! Tumaningizni tanlang yoki chiroyli mini-ilovamizni oching:", 
        reply_markup=markup
    )
    bot.send_message(
        message.chat.id, 
        "👇 Mini-ilovada ko'rish uchun bosing:", 
        reply_markup=inline_markup
    )

@bot.message_handler(func=lambda message: message.text in JOYLAR)
def send_namoz_vaqtlari(message):
    joy = JOYLAR[message.text]
    url = f"https://api.aladhan.com/v1/timings?latitude={joy['lat']}&longitude={joy['lon']}&method=3"
    
    try:
        res = requests.get(url).json()
        timings = res['data']['timings']
        
        text = f"📍 <b>{message.text} tumani</b> bo'yicha bugungi namoz vaqtlari:\n\n"
        text += f"🏙 Bomdod: {timings['Fajr']}\n"
        text += f"🌅 Quyosh: {timings['Sunrise']}\n"
        text += f"☀️ Peshin: {timings['Dhuhr']}\n"
        text += f"🌤 Asr: {timings['Asr']}\n"
        text += f"🌆 Shom: {timings['Maghrib']}\n"
        text += f"🌃 Hufton: {timings['Isha']}\n"
        
        bot.send_message(message.chat.id, text, parse_mode="HTML")
    except Exception as e:
        bot.send_message(message.chat.id, "Ma'lumot olishda xatolik yuz berdi. Qayta urinib ko'ring.")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()

