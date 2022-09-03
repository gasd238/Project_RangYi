import requests
from bs4 import BeautifulSoup
import nextcord


class Baseball:
    def showBaseballScore(self, teamName):
        if teamName == "기아" or teamName == "갸":
            teamName = "KIA"
        elif teamName == "케이티" or teamName == "크트" or teamName == "킅":
            teamName = "KT"
        elif teamName == "롯" or teamName == "꼴데" or teamName == "꼴":
            teamName = "롯데"
        elif teamName == "쓱" or teamName == "신세계":
            teamName = "SSG"
        elif teamName == "엔시" or teamName == "엔씨":
            teamName = "NC"
        elif teamName == "엘쥐" or teamName == "엘지" or teamName == "쥐":
            teamName = "LG"

        soup = BeautifulSoup(
            requests.get("https://sports.news.naver.com/kbaseball/index.nhn").text,
            "lxml",
        )
        date = soup.find("span", class_="day").text
        home = soup.find_all("li", class_="hmb_list_items")
        try:
            teamName = teamName.upper()
        except:
            pass
        for i in home:
            if teamName in i.text:
                inning = i.find("em")
                if inning.text == "종료":
                    team = i.find_all("span", class_="name")
                    pitcher = i.select("div > div > span:nth-child(4)")
                    picture = i.select("span.image.emblem > img")
                    score = i.select("div.inner > div")
                    embed1 = nextcord.Embed(
                        title=team[0].text + "\n" + pitcher[0].text,
                        description=score[0].text.replace("\t", "").replace("\n", ""),
                        colour=0xF7CAC9,
                    )
                    embed1.set_thumbnail(
                        url=str(
                            picture[0]["src"]
                            .replace("https://dthumb-phinf.pstatic.net?src=", "")
                            .replace("&type=f28_28&refresh=1", "")
                        )
                    )
                    embed2 = nextcord.Embed(
                        title=team[1].text + "\n" + pitcher[1].text,
                        description=score[1].text.replace("\t", "").replace("\n", ""),
                        colour=0xF7CAC9,
                    )
                    embed2.set_thumbnail(
                        url=str(
                            picture[1]["src"]
                            .replace("https://dthumb-phinf.pstatic.net?src=", "")
                            .replace("&type=f28_28&refresh=1", "")
                        )
                    )
                    return date, inning.text, embed1, embed2
                elif inning.text == "경기취소":
                    team = i.find_all("span", class_="name")
                    pitcher = i.select("div > div > span:nth-child(3)")
                    picture = i.select("span.image.emblem > img")
                    embed1 = nextcord.Embed(
                        title=team[0].text + "\n" + pitcher[0].text,
                        description=inning.text,
                        colour=0xF7CAC9,
                    )
                    embed1.set_thumbnail(
                        url=str(
                            picture[0]["src"]
                            .replace("https://dthumb-phinf.pstatic.net?src=", "")
                            .replace("&type=f28_28&refresh=1", "")
                        )
                    )
                    embed2 = nextcord.Embed(
                        title=team[1].text + "\n" + pitcher[1].text,
                        description=inning.text,
                        colour=0xF7CAC9,
                    )
                    embed2.set_thumbnail(
                        url=str(
                            picture[1]["src"]
                            .replace("https://dthumb-phinf.pstatic.net?src=", "")
                            .replace("&type=f28_28&refresh=1", "")
                        )
                    )
                    return date, inning.text, embed1, embed2
                else:
                    try:
                        test = int(inning.text.replace(":", "")) / 2
                        pitcher = i.select("div > div > span:nth-child(3)")
                    except:
                        date = ""
                        pitcher = i.select("div > div > span:nth-child(4)")
                    team = i.find_all("span", class_="name")
                    score = i.find_all("div", class_="score")
                    picture = i.select("span.image.emblem > img")
                    if not pitcher:
                        pitcher1 = "TBD"
                        pitcher2 = "TBD"
                    else:
                        pitcher1 = pitcher[0].text
                        pitcher2 = pitcher[1].text

                    if not score:
                        score1 = "0"
                        score2 = "0"
                    else:
                        score1 = score[0].text.replace("\t", "").replace("\n", "")
                        score2 = score[1].text.replace("\t", "").replace("\n", "")

                    embed1 = nextcord.Embed(
                        title=team[0].text + "\n" + pitcher1,
                        description=score1,
                        colour=0xF7CAC9,
                    )
                    embed1.set_thumbnail(
                        url=str(
                            picture[0]["src"]
                            .replace("https://dthumb-phinf.pstatic.net?src=", "")
                            .replace("&type=f28_28&refresh=1", "")
                        )
                    )
                    embed2 = nextcord.Embed(
                        title=team[1].text + "\n" + pitcher2,
                        description=score2,
                        colour=0xF7CAC9,
                    )
                    embed2.set_thumbnail(
                        url=str(
                            picture[1]["src"]
                            .replace("https://dthumb-phinf.pstatic.net?src=", "")
                            .replace("&type=f28_28&refresh=1", "")
                        )
                    )
                    return date, inning.text, embed1, embed2
        return None
