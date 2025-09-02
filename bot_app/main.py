import requests
import json
import telebot
import re
import logging
import modul1 as m

# pytelegrambotapi
 

 
bot = telebot.TeleBot(TOKEN)
bank= m.Bank(name = 'cbr')
#msg = m.Message()
val_list= bank.val


  
# Обрабатываются все сообщения, содержащие команды '/start' or '/help'.
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    
    msg = f"""Чтобы начать работу, введите команду в следующем формате:\n 
<код или название валюты - продажа>\n
<код или название валюты - покупка>\n
<количество валюты на продажу>\n
{'-'*60}\n
Для вызова справочника валют, используйте /values"""
    
    bot.send_message(message.chat.id, f"{msg}")

@bot.message_handler(commands=['values'])
def handle_start_help(message):
        
    bot.send_message(message.chat.id, f"{val_list}")

@bot.message_handler(content_types=['text'])
def handle_start_help(message):
    logging.info(f"{message.text}, {type(message.text)}")
    
    p = m.Message(message.text, val_list)
    a , b, c = p.check_input()
    

    if a:
        logging.info(f" out = {a}, in = {b}, sum_out = {c}")
        res_sum = bank.get_price(a, b, c)
        logging_info(f"{c} {a} = {res+sum} {b} по курсу ЦБР на {bank.current_date}")
    else:
        logging.error(f" ошибка входных данных")

        
    
  
   


bot.infinity_polling()


