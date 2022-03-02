import requests
import json
import pymongo
from Modules.setting import *  # Import Settings

client = pymongo.MongoClient(database)
db = client.rangyibot
stockcol = db.stock


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


class StockDB:
    def insert_stock(self, id):
        result = stockcol.find_one({"stockid": id})
        if not result:
            result = {"stockid": id}
            stockcol.insert_one(result)
            return "완료"
        else:
            return "이미 존재하는 id"

    def delete_stock(self, id):
        result = stockcol.find_one({"stockid": id})
        if result:
            stockcol.delete_one({"stockid": id})
            return "완료"
        else:
            return "존재하지 않는 id"

    def get_stock(self):
        result = stockcol.find({})
        if result:
            results = []
            for i in result:
                results.append(i["stockid"])
            return results
        else:
            return []
