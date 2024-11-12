#!/usr/bin/python3

import requests
import re
from lxml import html
from bs4 import BeautifulSoup
import requests

normal_rate = 0.0001
path = 'rate.txt'

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

def get_funding_rate(symbol='BTCUSDT') -> float:
    url = 'https://api.bybit.com/v5/market/funding/history'
    params = {
        'symbol' : 'BTCUSDT',
        'category' : 'linear',
        'limit' : 1
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data['retCode'] == 0:
            funding_rate = data['result']['list'][0]['fundingRate']
            return funding_rate
        else:
            print(f"Error: {data['ret_msg']}")
    else:
        print(f"HTTP Error: {response.status_code}")

conf = load_conf()


while (True):
    f = open(path, 'r')
    benchmark_rate = f.read()

    funding_rate = get_funding_rate()
    f = open(path, 'w')
    f.write(funding_rate)
    f.close()

    if float(funding_rate) == float(benchmark_rate):
        exit()
    elif float(funding_rate) < float(benchmark_rate):
        send_msg(f"Funding Rate continue to rise\nLast 30 minutes Funding Rate (Bybit) : {benchmark_rate}\nBTC/USDT Funding Rate (Bybit) : {funding_rate}")
    else:
        send_msg(f"Funding Rate continue to fall\nLast 30 minutes Funding Rate (Bybit) : {benchmark_rate}\nBTC/USDT Funding Rate (Bybit) : {funding_rate}")
    time.sleep(60 * 5)
