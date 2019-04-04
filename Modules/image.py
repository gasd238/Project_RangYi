import bs4
from urllib.request import urlopen, Request
import urllib
import random
import discord

def search_image(titleli):
    title = ''
    for i in titleli:
        title = title + i + ' '
    enc_location = urllib.parse.quote(title)
    hdr = {'User-Agent': 'Mozilla/5.0'}
    url = 'https://www.google.co.kr/search?hl=en&tbm=isch&q=' + enc_location 
    req = Request(url, headers=hdr)
    html = urllib.request.urlopen(req)
    bsObj = bs4.BeautifulSoup(html, "html.parser")
    embed = discord.Embed(colour=0xF7CAC9)
    imgfind1 = bsObj.find_all("img")   
    try:
        randomNum = random.randint(0, len(imgfind1)-1)
        imgsrc = imgfind1[randomNum].get('src')  
        embed.set_image(url=imgsrc) 
    except ValueError:
        embed.add_field(name = "검색된 사진이 없음...", value = "사진이 없느니라...")
    return embed