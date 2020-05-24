import bs4
import lxml
import discord
from urllib.request import urlopen, Request
import urllib
import random
from youtube_search import YoutubeSearch

class Search:
    def search_youtube(self, titleli):
        title=''
        for i in titleli:
            title = title+i
        results = YoutubeSearch(title, max_results=10).to_dict()
        embed = discord.Embed(title = "검색 결과", description = "목록", colour=0xF7CAC9)
        for i in range(len(results)):
            embed.add_field(name=str(i+1)+". " + results[i-1]['title'], inline=False)
            # value='https://www.youtube.com'+results[i-1]['link']
        return embed

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
        except:
            embed.add_field(name="오류", value="검색할 수 없음")
        return embed