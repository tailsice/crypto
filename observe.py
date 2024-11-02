#!/usr/bin/python3

import requests
import const
from bs4 import BeautifulSoup
from datetime import datetime
import time
import configparser
import os


def load_conf():
    if False == os.path.exists('./app.ini'):
        raise("please check the ./app.ini")
    config = configparser.ConfigParser()
    config.read('./app.ini')
    return config['app']

def send_msg(key: str, chat_id: str, msg: str):
    assert type(msg) == str, "Hello, World!!"
    url = f'https://api.telegram.org/bot{key}/sendMessage?chat_id={chat_id}&text={msg}'
    requests.get(url)


conf = load_conf()
current_time = datetime.now()

formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
print(f"\n請求時間：{formatted_time}")

### MAX
def get_max_exchange() -> float:
    response = requests.get(const.MAXExchangeURL)
    if response.status_code == 200:
        data = response.json()
        MAX_usdt_twd = data.get("usdttwd").get("last")
        print(f"MAX 的USDT/TWD匯率: {MAX_usdt_twd}")
        return float(MAX_usdt_twd)
    else :
        print("壞了，根本就不能用啊，ERROR CODE:",response.status_code)

def get_taiwan_bank_exchange() -> float:
    #台灣銀行牌告匯率網頁
    response = requests.get(const.TaiwanBankURL)
    html_doc = response.text

    soup = BeautifulSoup(html_doc, "html.parser")
    element = soup.find("td", {"data-table": "本行即期賣出", "class": "rate-content-sight"})
    number_sell = element.text.strip()
    print(f"台灣銀行即期賣出的 USD/TWD 匯率 : {number_sell}")

    element = soup.find("td", {"data-table": "本行即期買入", "class": "rate-content-sight"})
    number_buy = element.text.strip()
    print(f"台灣銀行即期買入的 USD/TWD 匯率 : {number_buy}")

    number_total = ( float(number_sell) + float(number_buy) ) / 2
    number_total_format = format(number_total, '.3f')
    print(f"匯率:{number_total_format}")

    number_obv = ( format(float(number_total) * 1.02, '.3f') )
    print(f"觀察匯率:{number_obv}")
    return float(number_obv)

while True:
    MAX_usdt_twd = get_max_exchange()
    number_total_format = get_taiwan_bank_exchange()
    if MAX_usdt_twd > number_total_format:
        msg = f"超過2%了，趕快套利!!\n匯率:{number_total_format}\nMAX 的USDT/TWD匯率:{MAX_usdt_twd}"
        send_msg(conf["api_key"], conf["chat_id"], msg)
        print(f"超過2%了，趕快套利")
    else:
        # msg = f"等待下次機會!!\n觀察匯率:{number_total_format}\nMAX 的USDT/TWD匯率:{MAX_usdt_twd}"
        # send_msg(conf["api_key"], conf["chat_id"], msg)
        print(f"等待下次機會!!")
    time.sleep(60 * 5)

