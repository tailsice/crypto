#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup
from datetime import datetime

def send_msg(msg:str):
    assert type(msg) == str, "Hello, World!!"
    url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={-4584076509}&text={msg}'
    requests.get(url)

current_time = datetime.now()

formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
print(f"\n請求時間：{formatted_time}")

### MAX
url = "https://max-api.maicoin.com/api/v2/tickers"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    MAX_usdt_twd = data.get("usdttwd").get("last")

    print(f"MAX 的USDT/TWD匯率: {MAX_usdt_twd}")

else :
    print("壞了，根本就不能用啊，ERROR CODE:",response.status_code)


#台灣銀行牌告匯率網頁
url = "https://rate.bot.com.tw/xrt?Lang=zh-TW"
response = requests.get(url)
html_doc = response.text

soup = BeautifulSoup(html_doc, "html.parser")
element = soup.find("td", {"data-table": "本行現金賣出", "class": "rate-content-cash"})
number_sell = element.text.strip()
print(f"台灣銀行現金賣出的 USD/TWD 匯率 : {number_sell}")

element = soup.find("td", {"data-table": "本行現金買入", "class": "rate-content-cash"})
number_buy = element.text.strip()
print(f"台灣銀行現金買入的 USD/TWD 匯率 : {number_buy}")

number_total = ( float(number_sell) + float(number_buy) ) / 2
number_total_format = format(number_total, '.3f')
print(f"匯率:{number_total_format}")

number_obv = ( format(float(number_total) * 1.02, '.3f') )
print(f"觀察匯率:{number_obv}")

if float(MAX_usdt_twd) > float(number_obv):
    send_msg("超過2%了，趕快套利!!\n匯率:{number_total_format}\nMAX 的USDT/TWD匯率:{MAX_usdt_twd}")
    print(f"超過2%了，趕快套利")
else:
    #send_msg(f"等待下次機會!!\n觀察匯率:{number_total_format}\nMAX 的USDT/TWD匯率:{MAX_usdt_twd}")
    print(f"等待下次機會!!")
