import requests
import bs4
import json

def get_temp():
    url = 'https://api.hangang.msub.kr'
    soup = bs4.BeautifulSoup(requests.get(url).text, 'lxml')
    river = json.loads(soup.find('p').text)
    return river['temp']
    

get_temp()