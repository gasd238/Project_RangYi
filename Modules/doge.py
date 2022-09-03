import requests
import json
from Modules.setting import *  # Import Settings

class PrintDoge:
    def __init__(self):
        self.price = 0
        self.percent = ""

    def get_api_json(self):
        url = "https://api.bithumb.com/public/ticker/DOGE_KRW"
        response = requests.get(url)
        jsondata = json.loads(response.text).get("data")
        self.price = jsondata["closing_price"]
        self.percent = (
            (float(self.price) - float(jsondata["prev_closing_price"]))
            / float(self.price)
            * 100
        )
        return self.price, self.percent

    def get_stock(self, stock):
        url = (
            f"https://polling.finance.naver.com/api/realtime?query=SERVICE_ITEM:{stock}"
        )
        response = requests.get(url)
        jsondata = json.loads(response.text)
        name = jsondata["result"]["areas"][0]["datas"][0]["nm"]
        price = jsondata["result"]["areas"][0]["datas"][0]["nv"]
        prev_price = jsondata["result"]["areas"][0]["datas"][0]["sv"]
        percent = (price - prev_price) / prev_price * 100
        return name, price, percent
