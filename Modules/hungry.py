import requests
import datetime
import re
from bs4 import BeautifulSoup
import discord

weekend_string = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]

def hungry():
    soup=BeautifulSoup(requests.get('http://www.gsm.hs.kr/xboard/board.php?tbnum=8').text, 'html.parser')
    now=datetime.datetime.now()
    temp=soup.find_all('div', class_="food_list_box")
    if now.weekday() == 4 and now.hour>=13 or now.weekday() == 5 or now.weekday() == 6 and now.hour < 19:
        meal = '급식이 없느니라...'
    elif now.weekday() >= 0  and now.weekday() < 5 or now.weekday() == 6 and now.hour >= 19:
        if now.hour>=19:
            today = temp[now.day].find_all('div', class_="content_info")
        else:
            today = temp[now.day - 1].find_all('div', class_="content_info")
        if now.hour>=19 or now.hour<8:
            meal=today[0].getText()
            tm = '아침'
        elif now.hour>=8 and now.hour<13:
            meal=today[1].getText()
            tm ='점심'
        elif now.hour>=13 and now.hour<19:
            meal=today[2].getText()
            tm = '저녁'
    meal=meal.split('\n')
    for i in range(0, len(meal)):
        if re.compile('[0-9]+').match(meal[i]):
            del meal[i]
        if meal[i].startswith('*'):
            del meal[i:]
            break
    cmeal=[]
    descriptions = ''
    for i in range(0,len(meal)):
        meal[i]=meal[i].split('\xa0')
        meal[i][0] = meal[i][0].strip('/')
        cmeal.append(meal[i][0])
    if len(cmeal)==1:
            descriptions=cmeal[0]
    else:
        for i in range(0, len(cmeal)):
            descriptions=descriptions+'- '+cmeal[i]+'\n'
    embed = discord.Embed(title="%s년 %s월 %s일 %s의 %s 식단표이니라~~" % (now.year, now.month, now.day, weekend_string[int(now.weekday())], tm),description=descriptions, colour=0xf7cac9)
    return embed