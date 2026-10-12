import telebot
import subprocess
import os
import glob

# Badl TOKEN_DIALK_HNA b lcode li 3tak BotFather 
TOKEN = '8757938811:AAHDYgpfrKtTw_MSIswXPvB3NCDRAVKpwEM'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Mrehba! Sift lia lien dial Spotify w ghadi nsift lik l'mp3.")

@bot.message_handler(func=lambda message: 'spotify.com' in message.text)
def download_spotify(message):
    url = message.text
    msg = bot.reply_to(message, "Tsenna chwiya... rani kantelechargi l'aghniya ⏳")
    
    try:
        # Hna khedemna python -m spotdl nishan bach maytl3ch l'mochkil l9dim
        subprocess.run(['python', '-m', 'spotdl', url], check=True)
        
        list_of_files = glob.glob('*.mp3')
        if list_of_files:
            latest_file = max(list_of_files, key=os.path.getctime)
            
            with open(latest_file, 'rb') as audio:
                bot.send_audio(message.chat.id, audio)
            
            os.remove(latest_file)
            bot.delete_message(message.chat.id, msg.message_id)
        else:
            bot.reply_to(message, "Mal9itch l'aghniya, jereb lien akhor.")
            
    except Exception as e:
        bot.reply_to(message, "W9e3 mochkil w ana kantelechargi l'aghniya. T2ked mn lien!")

print("Lbot khdam daba! Sir l Telegram w jereb sift lih lien...")
bot.polling()