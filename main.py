import os
import telebot
import time
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(regexp='^\d+[,|.]{0,1}\d+;\w+;\w+$')
def send_welcome(message):
    value, service, payment_method = message.text.split(';')
    
    bot.reply_to(message=message, text=f'Valor: R$ {value}\nServiço: {service}\nPagamento: {payment_method}')
    reply = bot.send_message(message.chat.id, "Registrando...")
    
    time.sleep(2)
    
    bot.edit_message_text('Registrado!', chat_id=reply.chat.id, message_id=reply.message_id)

    
bot.infinity_polling()