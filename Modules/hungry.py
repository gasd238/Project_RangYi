import requests
import datetime
import re
from bs4 import BeautifulSoup
import discord

weekend_string = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]


class Hungry:
    def hungry(self):
        now = datetime.datetime.now()

        def get_nextMeal(now):
            time = [480, 780, 1140]
            for i in range(len(time)):
                if (now.hour * 60 + now.minute) < time[i]:
                    return i
            return len(time)

        def get_nextDay(now):
            nextMeal = get_nextMeal(now)

            try:
                now = now.replace(day=now.day + int(nextMeal / 3))
            except ValueError:
                try:
                    now = now.replace(month=today.month + 1, day=1, hour=0)
                except ValueError:
                    now = now.replace(year=today.year + 1, month=1, day=1, hour=0)

            return now
        soup = BeautifulSoup(
        requests.get("http://www.gsm.hs.kr/xboard/board.php?tbnum=8&sYear=%s&sMonth=%s"% (now.year, now.month)).text, 'lxml')
        temp = soup.find_all('div', class_="food_list_box")
        if now.weekday() == 4 and now.hour >= 13 or now.weekday() == 5 or now.weekday() == 6 and now.hour < 19:
            descriptions = '급식이 없느니라...'
            embed = discord.Embed(title="급식이 없음...", description=descriptions, colour=0xf7cac9)
        elif 0 <= now.weekday() < 5 or now.weekday() == 6 and now.hour >= 19:
            try:
                if now.hour >= 19:
                    today = temp[now.day].find_all('div', class_="content_info")
                    now = now.replace(day=today.day + 1)
                else:
                    today = temp[now.day - 1].find_all('div', class_="content_info")
                if now.hour >= 8 and now.hour < 13:
                    meal=today[1].getText()
                    tm = '점심'
                elif now.hour >13 and now.hour < 19:
                    meal=today[2].getText()
                    tm = '저녁'
                elif 19 <= now.hour and now.hour < 8:
                    meal=today[4].getText()
                    tm = '아침'
            except:
                descriptions = '급식을 불러올 수 없음'
                embed = discord.Embed(title="급식을 불러올 수 없느니라...", description=descriptions, colour=0xf7cac9)
                return embed
            meal = meal.split('\n')
            cmeal = []
            descriptions = ''
            for i in range(0, len(meal)):
                meal[i]=meal[i].split('\xa0')
                meal[i][0] = meal[i][0].strip('/')
                meal[i][0] = meal[i][0].strip('*')
                meal[i][0] = meal[i][0].strip('..')
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
