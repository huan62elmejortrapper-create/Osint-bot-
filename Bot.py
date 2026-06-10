import telebot
import requests
import os

BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👁 OSINT Bot\n\nComandos:\n/email <email> - Buscar email en brechas\n/ip <ip> - Info de una IP\n/user <usuario> - Buscar usuario en redes")

@bot.message_handler(commands=['email'])
def check_email(message):
    try:
        query = message.text.split(' ', 1)[1]
        r = requests.get(f"https://haveibeenpwned.com/api/v3/breachedaccount/{query}", 
                        headers={"hibp-api-key": "free", "User-Agent": "osint-bot"})
        if r.status_code == 200:
            breaches = [b['Name'] for b in r.json()]
            bot.reply_to(message, f"⚠️ Encontrado en {len(breaches)} brechas:\n" + "\n".join(breaches))
        else:
            bot.reply_to(message, "✅ No encontrado en brechas conocidas")
    except:
        bot.reply_to(message, "Uso: /email correo@ejemplo.com")

@bot.message_handler(commands=['ip'])
def check_ip(message):
    try:
        query = message.text.split(' ', 1)[1]
        r = requests.get(f"https://ipapi.co/{query}/json/")
        data = r.json()
        bot.reply_to(message, f"🌍 IP: {query}\nPaís: {data.get('country_name')}\nCiudad: {data.get('city')}\nISP: {data.get('org')}")
    except:
        bot.reply_to(message, "Uso: /ip 1.1.1.1")

@bot.message_handler(commands=['user'])
def check_user(message):
    try:
        query = message.text.split(' ', 1)[1]
        redes = ['twitter.com', 'instagram.com', 'github.com', 'reddit.com', 'tiktok.com']
        resultado = f"🔍 Usuario: {query}\n\n"
        for red in redes:
            resultado += f"https://{red}/{query}\n"
        bot.reply_to(message, resultado)
    except:
        bot.reply_to(message, "Uso: /user nombre_usuario")

bot.infinity_polling()
