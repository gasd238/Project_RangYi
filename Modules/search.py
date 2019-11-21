import bs4
import lxml
#from selenium import webdriver
import discord
from urllib.request import urlopen, Request
import urllib
import random


class Search:
    def get_video_link(self, titleli):
        return

    def search_image(self, titleli):
        title = ''
        for i in titleli:
            title = title + i + ' '
        enc_location = urllib.parse.quote(title)
        hdr = {'User-Agent': 'Mozilla/5.0'}
        url = 'https://www.google.co.kr/search?hl=en&tbm=isch&q=' + enc_location
        req = Request(url, headers=hdr)
        html = urllib.request.urlopen(req)
        bsObj = bs4.BeautifulSoup(html, "lxml")
        embed = discord.Embed(colour=0xF7CAC9)
        imgfind1 = bsObj.find_all("img")
        try:
            randomNum = random.randint(0, len(imgfind1) - 1)
            imgsrc = imgfind1[randomNum].get('src')
            embed.set_image(url=imgsrc)
        except ValueError:
            embed.add_field(name="검색된 사진이 없음...", value="사진이 없느니라...")
        return embed