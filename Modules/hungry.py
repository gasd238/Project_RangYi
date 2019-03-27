import requests
import datetime
from bs4 import BeautifulSoup
url='http://www.gsm.hs.kr/xboard/board.php?tbnum=8'
source_code=requests.get(url)
plain_text=source_code.text

soup=BeautifulSoup(plain_text, 'html.parser')
def hungry():
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
        if meal[i].startswith('*'):
            del meal[i:]
            break
    cmeal=[]
    for i in range(0,len(meal)):
        meal[i]=meal[i].split('\xa0')
        cmeal.append(meal[i][0])
    return cmeal