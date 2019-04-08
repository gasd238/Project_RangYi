import bs4
import lxml
from selenium import webdriver
import discord

def get_video_link(titleli):
    title = ''
    for i in titleli:
        title = title + i + ' '
    chromedriver_dir = 'C:\chromedriver.exe'
    driver = webdriver.Chrome(chromedriver_dir)
    driver.get('https://www.youtube.com/results?search_query='+ title)
    entire = bs4.BeautifulSoup(driver.page_source, 'lxml').find_all('a', {'id': 'video-title'})
    driver.quit()
    embed = discord.Embed(title="영상 목록 이니라~~", description="검색한 영상 결과이니라~~", colour=0xf7cac9)
    if entire == []:
        embed.add_field(name='영상 없음..', value='검색된 영상이 없느니라...')
    else:
        if len(entire)<5:
            for i in range(0, len(entire)):
                entireText = entire[i].text.strip()
                test1 = entire[i].get('href')
                link = 'https://www.youtube.com'+test1
                embed.add_field(name=str(i+1)+'번째 영상',value=entireText + '\n링크 : '+link)
        else:
             for i in range(0, 5):
                entireText = entire[i].text.strip()
                test1 = entire[i].get('href')
                link = 'https://www.youtube.com'+test1
                embed.add_field(name=str(i+1)+'번째 영상',value=entireText + '\n링크 : '+link)           
    return embed