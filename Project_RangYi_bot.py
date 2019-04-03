# -*- coding: utf-8 -*- 
import asyncio
import discord
import youtube_dl
import datetime
from Modules.hungry import *
from Modules.morning import *
from Modules.help import *
from Modules.Annseq import *
from selenium import webdriver
from Modules.search import *
from Modules.image import *
from Modules.user import *

# Variables
client = discord.Client()
queues = {}
musiclist = []

# Music --
def check_queue(id, channel):
    if queues[id]!=[]:
        player = queues[id].pop(0)
        del musiclist[0]
        embed=discord.Embed(title="재생하겠느니라!!", description=player.title+"\n"+player.url)
        say = client.send_message(client.get_channel(channel), embed=embed)
        asyncio.run_coroutine_threadsafe(say, client.loop)
        player.volume=0.5
        player.start()

# Discord Client
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-----------------------')
    await client.change_presence(game=discord.Game(name="!설명으로 도움말", type=0))

@client.event
async def on_message(message):
    now = datetime.datetime.now()
    descriptions=''
    resings = ''
    title = ''

    # Bot이 하는 말은 반응하지 않음
    if message.author.bot:
        return None

    if levelIncrease(message.author, message.content):
        await client.send_message(message.channel, showLevel(message.author, True))

    # 봇 설명
    if message.content == "!설명":
        createdEmbed = create_help_embed()
        await client.send_message(message.channel, embed=createdEmbed)

    # 급식 파싱
    if message.content == '!급식':
        cmeal = hungry()
        if len(cmeal)==1:
            descriptions=cmeal[0]
        else:
            for i in range(0, len(cmeal)):
                descriptions=descriptions+'- '+cmeal[i]+'\n'
        embed = discord.Embed(title="오늘의 급식이니라!~~",description=descriptions, colour=0xf7cac9)
        await client.send_message(message.channel, embed=embed)

    # 봇 분양 관련
    if message.content == '!분양':
        embed = discord.Embed(title="링크를 보내주겠느니라!!", colour=0xf7cac9)
        embed.set_author(name='봇 추가 링크', url='https://discordapp.com/api/oauth2/authorize?client_id=517176814804926484&permissions=8&scope=bot')
        await client.send_message(message.channel, embed=embed)

    # 아침운동 정보
    if message.content == '!아침운동':
        weather, dust = morning()
        now=datetime.datetime.now()
        if now.weekday()>3 and now.weekday()<6:
            embed = discord.Embed(title="세희야! 내일 날씨 알려 주거라!",description='주말이니 편하게 쉬도록 하자꾸나!!', color=0xf7cac9)
            await client.send_message(message.channel, embed=embed)
        else:
            if '비' in weather or '나쁨' in dust:
                embed = discord.Embed(title="세희야! 내일 날씨 알려 주거라!",description='경비서는 날', color=0xf7cac9)
                await client.send_message(message.channel, embed=embed)
            else:
                embed = discord.Embed(title="세희야! 내일 날씨 알려 주거라!",description='아침운동 해야 할 것 같으니라...', color=0xf7cac9)
                await client.send_message(message.channel, embed=embed)

    # 음악 종료
    if message.content == '!종료':
        server = message.server
        del queues[server.id]
        for i in range(0, len(musiclist)):
            del musiclist[0]
        voice_client = client.voice_client_in(server)
        await voice_client.disconnect()
        await client.send_message(message.channel, '종료했느니라!!')

    # 음악 재생
    if message.content.startswith("!재생"):
        server = message.server
        if client.voice_client_in(server) == None:
            await client.join_voice_channel(message.author.voice.voice_channel)
        voice_client = client.voice_client_in(server)
        msg1 = message.content.split(' ')
        url = msg1[1]
        player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id, message.channel.id), before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5")
        player.volume = 0.5
        player.start()
        embed=discord.Embed(title="재생하겠느니라!!", description=player.title+"\n"+player.url)
        await client.send_message(message.channel, embed=embed)
    
    # 음악 예약
    if message.content.startswith('!예약'):
        msg1 = message.content.split(' ')
        url = msg1[1]
        server = message.server
        voice_client = client.voice_client_in(server)
        player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id, message.channel.id), before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5")
        if server.id in queues:
            queues[server.id].append(player)
        else:
            queues[server.id] = [player]
        await client.send_message(message.channel,'예약 완료 했느니라!')
        musiclist.append(player.title+"\n"+url)      

    # 음악 큐
    if message.content.startswith('!큐'):
        server = message.server
        msg1 = message.content.split(" ")
        check = msg1[1]
        # 큐 보기
        if check =='보기':
            for i in range(0, len(musiclist)):
                resings = resings + i+1 + '번 예약곡' + '-' + ' ' + musiclist[i] + '\n\n'
            embed = discord.Embed(title='대기중인 곡들이니라~', description = resings, color=0xf7cac9)
            await client.send_message(message.channel, embed=embed)
        # 큐에 있는 음악 삭제
        if check=='삭제':
            del musiclist[int(msg1[2])-1]
            del queues[server.id][int(msg1[2])-1]
            await client.send_message(message.channel, msg1[2]+ '번 예약곡을 취소 했느니라!')

    #서버 글 삭제
    if message.content.startswith('!삭제'):
        msg = message.content.split(' ')
        await client.purge_from(message.channel, limit=int(msg[1]))
    
    #발표 순서 정하기
    if message.content == '!발표':
        annsequence = rand()
        embed = discord.Embed(title='발표순서이니라!!', description = annsequence, color=0xf7cac9)
        await client.send_message(message.channel, embed=embed) 

    #링크 검색
    if message.content.startswith('!검색'):
        msg1 = message.content.split(' ')
        await client.send_message(message.channel, embed=get_video_link(msg1[1:]))

    if message.content.startswith('!사진'):
        msg1 = message.content.split(' ')
        await client.send_message(message.channel, embed=search_image(msg1[1:]))
    
    if message.content == '!시뮬':
        embed = discord.Embed(title = "랑이 연애 시뮬레이터", description = "<@"+message.author.id+">" + ' ' + "나와 놀아주러 왔구나!", colour = 0xf7cac9)
        embed.set_image(url='https://postfiles.pstatic.net/MjAxOTA0MDJfMjcg/MDAxNTU0MTc5NTgyNTYx.8IWLYICA0SyYKGzlMAodT1Bx9i-FCnMw3DSDvMhUiH4g.Pn14U9OyaKyaJLlkFXrgo1OwkzptEP0P8n0HOACaS6Ig.JPEG.gasd238/BandPhoto_5258877056.jpg?type=w580')
        await client.send_message(message.channel, embed = embed)

    # 링크 검색
    if message.content.startswith('!레벨'):
        await client.send_message(message.channel, showLevel(message.author, True))


# 실행
client.run('NTE3MTc2ODE0ODA0OTI2NDg0.Dt_YxA.V5rqQnIId1IVWr7oOZ-J18nmC5k')
