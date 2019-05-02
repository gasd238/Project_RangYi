import requests
from bs4 import BeautifulSoup
import datetime
class Calender:
    def get_calendar():
        today = datetime.datetime.now()

        req = requests.get("http://www.gsm.hs.kr/xboard/board.php?tbnum=4")
        soup = BeautifulSoup(req.text, 'lxml')

        try:
            info = soup.select("#xb_fm_list > div.calendar > ul > li > dl")
            
            result = "```"
            for i in info:
                if not i.find("dd") == None:
                    text = i.text.replace("\n", "")
                    result += "%6s -%s\n" % (text.split("-")[0], text.split("-")[1])
                    for i in text.split("-")[2:]:
                        result += "%7s -%s\n" % ("", i)
            result += "```"
            return result

        except AttributeError:
            return "%s년 %s월 학사일정을 불러올 수 없느니라..." % (today.year, today.month)
