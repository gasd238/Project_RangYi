from urllib.request import urlopen, Request
import urllib
import bs4


class Morning:
    def morning(self):
        url = 'https://search.naver.com/search.naver?ie=utf8&query='+ urllib.parse.quote('송정1동+날씨')
        soup = bs4.BeautifulSoup(urlopen(Request(url)).read(),'html.parser')
        weather = soup.find('div', class_='tomorrow_area _mainTabContent').find('p', class_='cast_txt').text
        dust = soup.find('div', class_='tomorrow_area _mainTabContent').find('div', class_='detail_box').text
        return weather, dust
