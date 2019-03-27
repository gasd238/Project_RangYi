from urllib.request import urlopen, Request
import urllib
import bs4

location = '송정1동'
enc_location = urllib.parse.quote(location + '+날씨')
def morning():
    url = 'https://search.naver.com/search.naver?ie=utf8&query='+ enc_location

    req = Request(url)
    page = urlopen(req)
    html = page.read()
    soup = bs4.BeautifulSoup(html,'html.parser')
    weather = soup.find('div', class_='tomorrow_area _mainTabContent').find('p', class_='cast_txt').text
    dust = soup.find('div', class_='tomorrow_area _mainTabContent').find('div', class_='detail_box').text
    return weather, dust