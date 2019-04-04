import requests
import datetime
import re
from bs4 import BeautifulSoup

def hungry():
    url='http://www.gsm.hs.kr/xboard/board.php?tbnum=8'
    source_code=requests.get(url)
    plain_text=source_code.text
    noma = re.compile('[0-9]+')
    soup=BeautifulSoup(plain_text, 'html.parser')
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
        elif now.hour>=8 and now.hour<13:
            meal=today[1].getText()
        elif now.hour>=13 and now.hour<19:
            meal=today[2].getText()
    meal=meal.split('\n')
    for i in range(0, len(meal)):
        if noma.match(meal[i]):
            del meal[i]
        if meal[i].startswith('*'):
            del meal[i:]
            break
    cmeal=[]
    for i in range(0,len(meal)):
        meal[i]=meal[i].split('\xa0')
        meal[i][0] = meal[i][0].strip('/')
        cmeal.append(meal[i][0])
    return cmeal