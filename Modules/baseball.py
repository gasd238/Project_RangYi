import requests
from bs4 import BeautifulSoup
import discord

class Baseball:
    def showBaseballScore(self, teamName):
        soup = BeautifulSoup(requests.get("https://sports.news.naver.com/kbaseball/index.nhn").text, 'lxml')
        home = soup.find_all('li', class_="hmb_list_items")
        try:
            teamName = teamName.upper()
        except:
            pass
        for i in home:
            if teamName in i.text:
                inning = i.find('em')
                if inning.text == "종료":
                    team = i.find_all('span', class_="name")
                    pitcher = i.select('div > div > span:nth-child(4)')
                    picture = i.find_all('img', class_="emblem")
                    score = i.select('div.inner > div')
                    embed1 = discord.Embed(title=team[0].text+"\n"+pitcher[0].text, description=score[0].text.replace("\t", "").replace("\n", ""), colour=0xf7cac9)
                    embed1.set_thumbnail(url = str(picture[0]['src'].replace("https://dthumb-phinf.pstatic.net?src=" ,"").replace("&type=f28_28&refresh=1", "")))
                    embed2 = discord.Embed(title=team[1].text+"\n"+pitcher[1].text, description=score[1].text.replace("\t", "").replace("\n", ""), colour=0xf7cac9)
                    embed2.set_thumbnail(url = str(picture[1]['src'].replace("https://dthumb-phinf.pstatic.net?src=" ,"").replace("&type=f28_28&refresh=1", "")))
                    return inning.text, embed1, embed2
                elif inning.text == "경기취소":
                    team = i.find_all('span', class_="name")
                    pitcher = i.select('div > div > span:nth-child(3)')
                    picture = i.find_all('img', class_="emblem")
                    embed1 = discord.Embed(title=team[0].text+"\n"+pitcher[0].text, description=inning.text, colour=0xf7cac9)
                    embed1.set_thumbnail(url = str(picture[0]['src'].replace("https://dthumb-phinf.pstatic.net?src=" ,"").replace("&type=f28_28&refresh=1", "")))
                    embed2 = discord.Embed(title=team[1].text+"\n"+pitcher[1].text, description=inning.text, colour=0xf7cac9)
                    embed2.set_thumbnail(url = str(picture[1]['src'].replace("https://dthumb-phinf.pstatic.net?src=" ,"").replace("&type=f28_28&refresh=1", "")))
                    return inning.text, embed1, embed2
                else:
                    team = i.find_all('span', class_="name")
                    pitcher = i.select('div > div > span:nth-child(4)')
                    score = i.find_all('div', class_="score")
                    picture = i.find_all('img', class_="emblem")
                    embed1 = discord.Embed(title=team[0].text+"\n"+pitcher[0].text, description=score[0].text.replace("\t", "").replace("\n", ""), colour=0xf7cac9)
                    embed1.set_thumbnail(url = str(picture[0]['src'].replace("https://dthumb-phinf.pstatic.net?src=" ,"").replace("&type=f28_28&refresh=1", "")))
                    embed2 = discord.Embed(title=team[1].text+"\n"+pitcher[1].text, description=score[1].text.replace("\t", "").replace("\n", ""), colour=0xf7cac9)
                    embed2.set_thumbnail(url = str(picture[1]['src'].replace("https://dthumb-phinf.pstatic.net?src=" ,"").replace("&type=f28_28&refresh=1", "")))
                    return inning.text, embed1, embed2
        return None