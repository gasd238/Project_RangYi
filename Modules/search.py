import nextcord
from urllib.request import urlopen, Request
import urllib
import random
import json
from youtube_search import YoutubeSearch
from Modules.setting import id, secret


class Search:
    def search_youtube(self, titleli):
        title = ""
        for i in titleli:
            title = title + i
        results = YoutubeSearch(title, max_results=10).to_dict()
        embed = nextcord.Embed(title="검색 결과", description="목록", colour=0xF7CAC9)
        for i in range(len(results)):
            embed.add_field(
                name=str(i + 1) + ". " + results[i - 1]["title"],
                value="https://www.youtube.com" + results[i - 1]["url_suffix"],
                inline=False,
            )
        return embed

    def search_image(self, titleli):
        link = []
        title = ""
        for i in titleli:
            title = title + i + " "
        name = urllib.parse.quote(title)
        hdr = {"X-Naver-Client-Id": id, "X-Naver-Client-Secret": secret}
        url = "https://openapi.naver.com/v1/search/image?&display=50&sort=sim&filter=large&query={}".format(
            name
        )
        req = Request(url, headers=hdr)
        html = urllib.request.urlopen(req)
        imgs = json.loads(html.read())
        for info in imgs["items"]:
            link.append(info["link"])
        embed = nextcord.Embed(colour=0xF7CAC9)
        try:
            randomNum = random.randint(0, len(link) - 1)
            imgsrc = link[randomNum]
            embed.set_image(url=imgsrc)
        except ValueError:
            embed.add_field(name="검색된 사진이 없음...", value="사진이 없느니라...")
        except:
            embed.add_field(name="오류", value="검색할 수 없음")
        return embed
