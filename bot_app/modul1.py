import logging
import urllib.request
import os
import re
import requests
import pandas as pd
import redis
 
import datetime
import xml.etree.ElementTree as ET
from lxml import etree

def logging_app(path_log):
    
    
    logging.basicConfig(handlers=[logging.FileHandler(filename= path_log,
                                                 encoding='utf-8', mode='w')],
                    format="%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

    logging.info(f"{path_log} starting")

logging_app(f"{os.getcwd()}/skill.log")



class Server: # запуск базы Redis

    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

    


class Bank:
    def __init__(self, name = None, current_date = None):
        self.name = name
        self.current_date = datetime.date.today()
        #self.r = Server()
        #self.val = self.get_val_list() # общий список валют
        
        self.rates = self.get_rates()
        #self.rate_list = self.get_trading_()
        self.val = self.get_currency_codes() # список валют по странам с ISO
        
    
       

    def get_val_list(self):  # создает справочник валют

        url = "https://www.cbr.ru/scripts/XML_valFull.asp"
        
        try:
            
            req = requests.post(url)
            req = req.text
            

            # Парсим XML из объекта файла
            root = ET.fromstring(req)
           
            
            val={}
            val_list = ''
            for child in root:
                cur_name_rus = child[0].text
                cur_name_eng = child[1].text
                iso_chr = child[5].text
                iso_num = child[4].text
                cur_nominal = child[2].text
                logging.info(f"{child[0].text} {child[1].text} {child[2].text} {child[3].text} {child[4].text}{child[5].text} ")
                '''
                val[iso] = Value(iso)
                val[iso].name_rus = cur_name_rus
                val[iso].name_eng = cur_name_eng
                val[iso].nominal = cur_nominal
                '''
                if iso_chr:
                    val[iso_chr] = f"{iso_num:0>3}  {iso_chr:3}  {cur_name_rus: <30}"

            return val

        except urllib.error.URLError as e:
            print(f"Ошибка при загрузке URL: {e.reason}")
        except ET.ParseError as e:
            print(f"Ошибка при парсинге XML: {e}")


    def get_rates(self ): # котировки валют ЦБР
        date = self.current_date.strftime(r'%d/%m/%Y')
        
        url = f"http://www.cbr.ru/scripts/XML_daily.asp" 
        params = {'date_req': date}
        logging.info(f"url = {url}")
        try:
            
            req = requests.post(url, params= params)
            req = req.text
            

            # Парсим XML из объекта файла
            root = ET.fromstring(req)
            
            rate = {}
            for child in root:
                iso = child[1].text
                val  = child[5].text
                rate[iso] = val
            rate['RUB'] = 1
            return rate    
             

                

        except urllib.error.URLError as e:
            print(f"Ошибка при загрузке URL: {e.reason}")
        except ET.ParseError as e:
            print(f"Ошибка при парсинге XML: {e}")

                

    def get_trading_(self): # создаем список валют, по которым есть ненулевые котировки ЦБР
       res =f"   №    Код  {'Наименование':<30}\n {'-'* 60}\n"
       for k, v in self.rates.items():
           if v:
               res += f"{self.val[k][3]}  {self.val[k][2]}  {self.val[k][1]}\n"
       return res
    
    def get_price(self, base, quote, amount):
        

        base_rub = float(self.rates[base])
        quote_rub = float(self.rates[quote])
        quote_sum = quote_rub / base_rub * float(amount)

        return amount

    def get_currency_codes(self):

        url = "https://www.iban.ru/currency-codes"

        result = requests.get(url)

        req = result.text

        #logging.info(f"req = {req}")

        #root = ET.fromstring(req)
        root = etree.HTML(req)
        
        t  = root.xpath('//tr')

        val_list = {}
        val_list_country = {}
        val_list2 = []
        for p in t:

            q = p.xpath('//td')

            s = []
            for i in p:
                # Страна, валюта, код, номер"    
                logging.info(f"{i.text}")
                s.append(i.text)
            if s[2] == "BYR":
                s[2] = "BYN"
                s[3] = '933'

            if self.rates.get(s[2], False):

                val_list_country[s[0]] = ' , '.join(s)
                val_list[s[1]] = ' , '.join(s[1:])
               
                logging.info(f"{s[2]}:{val_list[s[1]]}")
            
        items = val_list_country.items()
        sorted_items = sorted(items)
        val_list_country = dict(sorted_items)

        

        items = val_list.items()
        sorted_items = sorted(items)
        val_list = dict(sorted_items)

        
        s = ''
        for k, v in val_list.items():
            s += f"{v}\n"

        
        

        return s
        
            
    
            

        


class Message:

    def __init__(self, message = None, val_list = None):
            self.message = message
            self.val_list = val_list
            



   
    def check_input(self):


        res = re.search(r'<(\w+)><(\w+)><(\d+)>', self.message)
        if res:
            logging.info(f"<{res.group(1)}>.*<{res.group(2)}>.*<{res.group(3)}>")
            val_out = self.find_in(res.group(1), self.val_list)
            val_in = self.find_in(res.group(2), self.val_list)
            if all([val_in, val_out]):
                return val_out, val_in, float(res.group(3))
            else:
                logging.error(f"Выбранной валюты нет в списке")
                return False

        else:
            logging.error(f"Неверный формат ввода")
            return False


        
        

        
    def find_in(self, msg, list_):
        
        a = list_.split('\n')
        s = [i for i in a if msg in i ]   
        
        if s:
            res = re.search(r'.* +([A-Z]{3}) +.*', s[0]).group(1)    
            return res
        else:
            return False


class Value:
    def __init__(self, iso = None):
        self.name_rus = None
        self.name_eng = None
        self.iso  = None
        self.nominal = None
        self.bank_name = None
        self.buy_rate = None
        self.sell_rate = None
        self.rate = None

        

   


if __name__ == "__main__":
    #get_currency_2()
    cbr = Bank(name = 'cbr')

    cbr.get_currency_codes()

       
