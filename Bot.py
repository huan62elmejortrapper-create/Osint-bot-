import telebot
import requests
import os

BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, """👁 OSINT Bot

Comandos:
/email <email> - Buscar email en brechas
/ip <ip> - Info de una IP
/user <usuario> - Buscar usuario en redes
/link <url> - Analizar un link
/phone <numero> - Info de un teléfono
/dominio <dominio> - Info de un dominio""")

@bot.message_handler(commands=['email'])
def check_email(message):
    try:
        query = message.text.split(' ', 1)[1]
        resultado = f"🔍 Buscando: {query}\n\n"
        
        # LeakCheck (gratis limitado)
        r = requests.get(f"https://leakcheck.io/api/public?check={query}")
        if r.status_code == 200:
            data = r.json()
            if data.get('found'):
                resultado += f"⚠️ LeakCheck: Encontrado en {data.get('sources', [])}\n"
            else:
                resultado += "✅ LeakCheck: No encontrado\n"
        
        # IntelX (free tier)
        intelx_key = os.environ.get('INTELX_KEY', '')
        if intelx_key:
            headers = {"x-key": intelx_key}
            r2 = requests.post("https://2.intelx.io/intelligent/search",
                json={"term": query, "maxresults": 5, "media": 0},
                headers=headers)
            if r2.status_code == 200:
                resultado += f"🔎 IntelX: {r2.json()}\n"
        
        # Links para búsqueda manual
        resultado += f"\n🔗 Buscar manualmente:\n"
        resultado += f"• https://haveibeenpwned.com/account/{query}\n"
        resultado += f"• https://leakcheck.io/?query={query}\n"
        resultado += f"• https://intelx.io/?s={query}\n"
        resultado += f"• https://dehashed.com/search?query={query}\n"
        
        bot.reply_to(message, resultado)
    except:
        bot.reply_to(message, "Uso: /email correo@ejemplo.com")

@bot.message_handler(commands=['link'])
def check_link(message):
    try:
        query = message.text.split(' ', 1)[1]
        resultado = f"🔗 Analizando: {query}\n\n"
        
        # VirusTotal
        resultado += f"🦠 VirusTotal: https://www.virustotal.com/gui/url/{requests.utils.quote(query)}\n"
        # URLScan
        r = requests.post("https://urlscan.io/api/v1/scan/",
            json={"url": query, "visibility": "public"},
            headers={"Content-Type": "application/json"})
        if r.status_code == 200:
            uuid = r.json().get('uuid')
            resultado += f"🔍 URLScan: https://urlscan.io/result/{uuid}/\n"
        
        resultado += f"📦 Archive: https://web.archive.org/web/*/{query}\n"
        resultado += f"🔎 IntelX: https://intelx.io/?s={query}\n"
        
        bot.reply_to(message, resultado)
    except:
        bot.reply_to(message, "Uso: /link https://ejemplo.com")

@bot.message_handler(commands=['ip'])
def check_ip(message):
    try:
        query = message.text.split(' ', 1)[1]
        r = requests.get(f"https://ipapi.co/{query}/json/")
        data = r.json()
        r2 = requests.get(f"https://ipwho.is/{query}")
        data2 = r2.json()
        resultado = f"""🌍 IP: {query}
País: {data.get('country_name')}
Ciudad: {data.get('city')}
ISP: {data.get('org')}
ASN: {data2.get('connection', {}).get('asn')}
Proxy/VPN: {data2.get('security', {}).get('proxy')}
Tor: {data2.get('security', {}).get('tor')}"""
        bot.reply_to(message, resultado)
    except:
        bot.reply_to(message, "Uso: /ip 1.1.1.1")

@bot.message_handler(commands=['user'])
def check_user(message):
    try:
        query = message.text.split(' ', 1)[1]
        redes = ['twitter.com', 'instagram.com', 'github.com', 'reddit.com',
                 'tiktok.com', 'facebook.com', 'linkedin.com', 'youtube.com',
                 'twitch.tv', 'pinterest.com', 'snapchat.com', 'telegram.me']
        resultado = f"🔍 Usuario: {query}\n\n"
        for red in redes:
            resultado += f"https://{red}/{query}\n"
        resultado += f"\n🔎 Sherlock: https://sherlock-project.github.io/?q={query}"
        bot.reply_to(message, resultado)
    except:
        bot.reply_to(message, "Uso: /user nombre_usuario")

@bot.message_handler(commands=['dominio'])
def check_dominio(message):
    try:
        query = message.text.split(' ', 1)[1]
        resultado = f"🌐 Dominio: {query}\n\n"
        resultado += f"• WHOIS: https://whois.domaintools.com/{query}\n"
        resultado += f"• DNS: https://dnschecker.org/#A/{query}\n"
        resultado += f"• Subdomains: https://crt.sh/?q=%.{query}\n"
        resultado += f"• IntelX: https://intelx.io/?s={query}\n"
        resultado += f"• Shodan: https://www.shodan.io/search?query={query}\n"
        bot.reply_to(message, resultado)
    except:
        bot.reply_to(message, "Uso: /dominio ejemplo.com")

bot.infinity_polling()

