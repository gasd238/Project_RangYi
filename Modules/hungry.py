import requests
import datetime
import re
from bs4 import BeautifulSoup
import discord

weekend_string = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]


class Hungry:
    def hungry(self):
        tm = ''
        cmeal = []
        descriptions = ''
        now = datetime.datetime.now()
        soup = BeautifulSoup(requests.get("http://gsm.gen.hs.kr/xboard/board.php?tbnum=8&sYear=%s&sMonth=%s" % (now.year, now.month)).text, 'lxml')
        temp = soup.find_all('div', class_="food_list_box")
        if now.weekday() == 4 and now.hour > 13 or now.weekday() == 5 or now.weekday() == 6 and now.hour < 19:
            embed = discord.Embed(title="급식이 없음...", description='급식이 없느니라...', colour=0xf7cac9)
            return embed
        else:
            try:
                if now.hour >= 19 and now.hour <= 24:
                    today = temp[now.day].find_all('div', class_="content_info")
                else:
                    today = temp[now.day - 1].find_all('div', class_="content_info")
                if now.hour >= 8 and now.hour < 13:
                    meal=today[1].getText()
                    tm = '점심'
                elif now.hour >= 13 and now.hour < 18:
                    meal=today[2].getText()
                    tm = '저녁'
                else:
                    meal=today[0].getText()
                    tm = '아침'
            except:
                embed = discord.Embed(title="급식을 불러올 수 없느니라...", description='급식을 불러올 수 없음', colour=0xf7cac9)
                return embed
            meal = meal.split('\n')
            for i in range(0, len(meal)):
                meal[i] = re.sub(r'\([^)]*\)', '', meal[i])
                meal[i]=meal[i].split('\xa0')
                meal[i][0] = meal[i][0].strip('/')
                meal[i][0] = meal[i][0].strip('*')
                meal[i][0] = meal[i][0].strip('..')
                meal[i][0] = meal[i][0].replace('*', '')
                if meal[i][0] == '생일을' or meal[i][0] == '선생님':
                    continue
                if re.compile('[0-9]+').match(meal[i][0]):
                    continue
                cmeal.append(meal[i][0])
            if len(cmeal) == 1:
                descriptions = cmeal[0]
            else:
                for i in range(0, len(cmeal)):
                    if cmeal[i] == '':
                        continue
                    descriptions = descriptions+'- '+cmeal[i]+'\n'

                embed = discord.Embed(title="%s년 %s월 %s일 %s의 %s 식단표이니라~~" % (now.year, now.month, now.day, weekend_string[int(now.weekday())], tm), description=descriptions, colour=0xf7cac9)
                return embed
        
