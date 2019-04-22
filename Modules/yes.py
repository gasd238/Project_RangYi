import urllib
import requests
from bs4 import BeautifulSoup
import discord
import re

def check():
    name = []
    book_name = []
    req = requests.get('http://www.yes24.com/searchcorner/Search?keywordAd=&keyword=&domain=ALL&qdomain=%C0%FC%C3%BC&query=%B3%AA%BF%CD+%C8%A3%B6%FB%C0%CC%B4%D4')
    soup=BeautifulSoup(req.text, 'lxml')
    temp = soup.find_all('p', class_="goods_name goods_icon")
    for i in temp:
        name.append(i.find('strong'))
    for i in name:
        List = re.sub('<.+?>', '', str(i), 0).strip()
        book_name.append(List)

    for i in book_name:
        if i == '나와 호랑이님 20':
            return true