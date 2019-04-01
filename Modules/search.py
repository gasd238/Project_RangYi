import bs4
import lxml
from selenium import webdriver
import discord

def get_video_link(titleli):
    title = ''
    for i in titleli:
        title = title + i + ' '
    print(title)
    chromedriver_dir = 'C:\chromedriver.exe'
    driver = webdriver.Chrome(chromedriver_dir)
    driver.get('https://www.youtube.com/results?search_query='+ title)
    source = driver.page_source
    bs = bs4.BeautifulSoup(source, 'lxml')
    entire = bs.find_all('a', {'id': 'video-title'})
    embed = discord.Embed(title="영상 목록 이니라~~", description="검색한 영상 결과이니라~~", colour=0xf7cac9)
    if entire == []:
        embed.add_field(name='영상 없음..', value='검색된 영상이 없느니라...')
    else:
        for i in range(0, 5):
            entireNum = entire[i]
            entireText = entireNum.text.strip()
            test1 = entireNum.get('href')
            link = 'https://www.youtube.com'+test1
            embed.add_field(name=str(i+1)+'번째 영상',value=entireText + '\n링크 : '+link)
    driver.quit()
    return embed