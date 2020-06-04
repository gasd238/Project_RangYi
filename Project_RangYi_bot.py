# -*- coding: utf-8 -*- 
import asyncio
import discord
import youtube_dl
import datetime
import re
import os
# import json
from Modules.hungry import Hungry
from Modules.morning import Morning
from Modules.help import Help
from Modules.Annseq import Annseq
from Modules.search import Search
from Modules.user import UserLevel
from Modules.calendar import Calender
from Modules.gamesave import Save
from Modules.game_play import Game
from Modules.setting import token

# Variables
client = discord.Client()
queues = {}
musiclist = []
suedUser = {}
sueingUser = {}
fcheck = [0]
players = []
game_stat = {}
game_channels = {}
level = 0
favper = 0
choice = 0

loop = asyncio.get_event_loop()


# Music --
def check_queue(qid, channel, info):
    if queues[qid]:
        song_there = os.path.isfile(".mp3")
        if song_there:
            os.remove("reservsong.mp3")
        player = queues[qid].pop(0)
        embed = discord.Embed(title="재생하겠느니라!!", description=musiclist[0] + "\n" + info["url"])
        del musiclist[0]
        say = channel.send(embed=embed)
        asyncio.run_coroutine_threadsafe(say, client.loop)
        voice.play(player, after=lambda: check_queue(guild.id, message.channel, info))


# Discord Client
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-----------------------')
    game = discord.Game("!설명으로 도움말")
    await client.change_presence(status=discord.Status.online, activity=game)

    loop.create_task(realtime())


@client.event
async def on_message(message):
    global level, favper, choice
    # 숫자만 가려내기 위해
    noma = re.compile('[0-9]+')
    now = datetime.datetime.now()
    resings = ''
    title = ''
    guild = message.guild
    channel = message.channel
    free_chat = client.get_channel(514392468402208768)
    help = Help()
    save = Save()
    userlevel = UserLevel()
    hungry = Hungry()
    morningC = Morning()
    ann = Annseq()
    search = Search()
    cal = Calender()
    save = Save()
    game = Game()
    player=0
    # Bot이 하는 말은 반응하지 않음  
    

    if message.author.bot:
        return None

    # 경험치 상승 처리
            # if userlevel.levelIncrease(message.author, message.content):
            #     await channel.send(free_chat, userlevel.showLevel(message.author, True))

    # 봇 설명
    if message.content == "!설명":
        createdEmbed = help.create_help_embed()
        await channel.send(embed=createdEmbed)

    # 급식 파싱
    if message.content == "!급식":
        embed = hungry.hungry()
        await channel.send(embed=embed)

    # 봇 분양 관련
    if message.content == '!분양':
        embed = discord.Embed(title="링크를 보내주겠느니라!!", description='여기',
                              url='https://discordapp.com/api/oauth2/authorize'
                                  '?client_id=517176814804926484&permissions=8&scope=bot',
                              colour=0xf7cac9)
        await channel.send(embed=embed)

    # 아침운동 정보
    if message.content == '!아침운동':
        weather, dust = morningC.morning()
        if 3 < datetime.datetime.now().weekday() < 6:
            embed = discord.Embed(title="세희야! 내일 날씨 알려 주거라!", description='주말이니 편하게 쉬도록 하자꾸나!!', color=0xf7cac9)
            await channel.send(embed=embed)
        else:
            if '비' in weather or '나쁨' in dust:
                embed = discord.Embed(title="세희야! 내일 날씨 알려 주거라!", description='학교도는 날이니라...', color=0xf7cac9)
                await channel.send(embed=embed)
            else:
                embed = discord.Embed(title="세희야! 내일 날씨 알려 주거라!", description='아침운동 해야 할 것 같으니라...', color=0xf7cac9)
                await channel.send(embed=embed)

    # # 음악 종료
    # if message.content == '!종료':
    #     try:
    #         for key in queues:
    #             if key == guild.id:
    #                 del queues[guild.id]
    #     except RuntimeError:
    #         for key in queues:
    #             if key == guild.id:
    #                 del queues[guild.id]
    #     if musiclist:
    #         musiclist.clear()
    #     try:
    #         voice_client = client.voice_client_in(guild)
    #         await voice_client.disconnect()
    #         await channel.send('종료했느니라!!')
    #     except discord.DiscordException:
    #         return

    # # 음악 재생
    # if message.content.startswith("!재생"):
    #     voicemember = message.author.voice.channel.members
    #     for i in range(len(voicemember)):
    #         voicemember[i] = voicemember[i].name
    #     if message.author.name not in voicemember:
    #         await channel.send('음성방에 들어와야 사용이 가능하니라')
    #     try:
    #         voice = await message.author.voice.channel.connect()
    #     except:
    #         for i in client.voice_clients:
    #             if i.channel == message.author.voice.channel:
    #                 voice = i
    #     msg1 = message.content.split(' ')
    #     url = msg1[1]
    #     ydl_opts = {
    #         'format': 'bestaudio/best',
    #         'postprocessors': [{
    #             'key': 'FFmpegExtractAudio',
    #             'preferredcodec': 'mp3',
    #             'preferredquality': '192',
    #         }],
    #     }
    #     with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    #         info = ydl.extract_info(url)
    #         ydl.download([url])
    #     voice.play(discord.FFmpegPCMAudio('./' + info["title"] + '.mp3'), after=lambda: check_queue(guild.id, message.channel, info))
    #     voice.volume = 100
    #     embed = discord.Embed(title="재생하겠느니라!!", description=info['title'] + "\n" + url)
    #     await channel.send(embed=embed)

    # # 음악 예약
    # if message.content.startswith('!예약'):
    #     msg1 = message.content.split(' ')
    #     url = msg1[1]
    #     song_there = os.path.isfile("reservsong.mp3")
    #     if song_there:
    #         os.remove("reservsong.mp3")
    #     ydl_opts = {
    #         'format': 'bestaudio/best',
    #         'postprocessors': [{
    #             'key': 'FFmpegExtractAudio',
    #             'preferredcodec': 'mp3',
    #             'preferredquality': '192',
    #         }],
    #     }
    #     with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    #         ydl.download([url])
    #     for file in os.listdir("./"):
    #         if file.endswith(".mp3"):
    #             os.rename(file, info['title'] + '.mp3')
    #             player = discord.FFmpegPCMAudio(info['title'] + '.mp3')
    #         if guild.id in queues:
    #             queues[guild.id].append(player)
    #         else:
    #             queues[guild.id] = [player]
    #         await channel.send('예약 완료 했느니라!')
    #         musiclist.append(info['title'] + "\n" + url)

    # # 음악 큐
    # if message.content.startswith('!큐'):
    #     msg1 = message.content.split(" ")
    #     check = msg1[1]
    #     # 큐 보기
    #     if check == '보기':
    #         for i in range(0, len(musiclist)):
    #             resings = resings + str(i + 1) + '번 예약곡' + '-' + ' ' + musiclist[i] + '\n\n'
    #         embed = discord.Embed(title='대기중인 곡들이니라~', description=resings, color=0xf7cac9)
    #         await channel.send(embed=embed)
    #     # 큐에 있는 음악 삭제
    #     if check == '삭제':
    #         del musiclist[int(msg1[2]) - 1]
    #         del queues[guild.id][int(msg1[2]) - 1]
    #         await channel.send(msg1[2] + '번 예약곡을 취소 했느니라!')

    # 서버 글 삭제
    if message.content.startswith('!삭제'):
        msg = message.content.split(' ')
        try:
            if int(msg[1]) < 100:
                await message.delete()
                await message.channel.purge(limit=int(msg[1]))
            else:
                await message.delete()
                await channel.send('100개 이상 메세지는 삭제할 수 없느니라....')
        except discord.DiscordException:
            return

    # 발표 순서 정하기
    if message.content.startswith('!발표'):
        msg1 = message.content.split(' ')
        if len(msg1) > 1:
            annsequence = ann.rand_self(msg1[1:])
        else:
            annsequence = ann.rand()
        embed = discord.Embed(title='발표순서이니라!!', description=annsequence, color=0xf7cac9)
        await channel.send(embed=embed)

    # 유튜브 검색
    if message.content.startswith('!검색'):
        msg1 = message.content.split(' ')
        await channel.send(embed=search.search_youtube(msg1[1:]))

    # 사진 검색
    if message.content.startswith('!사진'):
        msg1 = message.content.split(' ')
        await channel.send(embed=search.search_image(msg1[1:]))

    # 유저 레벨 관련
    if message.content.startswith('!레벨'):
        msg1 = message.content.split(' ')
        if len(msg1) > 1:
            try:
                id_ = re.findall(noma, msg1[1])
                id__ = await client.get_user_info(id_[0])
                await channel.send(userlevel.showLevel(id__))  # 유저 지정 처리
            except discord.DiscordException:
                await channel.send('그 사람은 조회가 불가능하니라...')
            except TypeError:
                await channel.send('그 사람은 조회가 불가능하니라...')
        else:
            await channel.send(userlevel.showLevel(message.author))

    # 서버 레벨 랭킹
    if message.content == '!랭킹':
        rank = userlevel.showRanking(guild)
        if rank.count() > 10:
            rankLength = 10
        else:
            rankLength = rank.count()
        if rankLength == 0:
            embed = discord.Embed(title='서버의 랭킹이니라!', description='표시할 사람이 없습니다.')
        else:
            embed = discord.Embed(title='서버의 랭킹이니라!', description='{}위까지 표시되느니라~'.format(rankLength))
        count = 0
        for doc in rank:
            count += 1
            userobj = await client.get_user_info(doc['userid'])
            embed.add_field(name='**' + userobj.name + '**',
                            value="{} 레벨\n현재 경험치: **{} XP**,"
                                  "다음 레벨까지 {} XP".format(doc['level'],
                                                         doc['currentxp'],
                                                         userlevel.LevelExpGetter(doc['level']) - doc[
                                                             'currentxp']),
                            inline=False)
            if count > rankLength - 1:
                break

        await channel.send(embed=embed)

    if message.content == '!일정':
        title = "%s년 %s월의 학사일정이니라!" % (now.year, now.month)
        em = discord.Embed(title=title, description=cal.get_calendar(), colour=0xf7cac9)
        await channel.send(embed=em)

        else:
            embed = discord.Embed(title='설명', description='!게임 명령어 관련', color=0xf7cac9)
            embed.add_field(name='시작', value='게임을 시작합니다.')
            embed.add_field(name='종료', value='게임을 종료합니다.')
            await channel.send(embed=embed)

    #if message.content.startswith('!test'):
    #     msg1 = message.content.split(' ')
    #     if len(msg1) > 1:
    #         try:
    #             id_ = re.findall(noma, msg1[1])
    #             id__ = await client.get_user_info(id_[0])
    #             profileurl = id__.avatar_url
    #         except:
    #             await channel.send('그 사람은 조회가 불가능하니라...')
    #     else:
    #         profileurl = message.author.avatar_url
    #     embed = discord.Embed(title='asdf', description='casasdf')
    #     embed.set_image(url=profileurl)
    #     await channel.send(embed=embed)


async def realtime():
    selectedTime = [27000, 45600, 67200]
    await asyncio.sleep(0.01)
    recentTimeStamp = (datetime.datetime.now().timestamp() + 32400) % 86400
    if recentTimeStamp < 27000 or recentTimeStamp > 67200:
        nextTimeStamp = 27000
    elif recentTimeStamp < 45600:
        nextTimeStamp = 45600
    else:
        nextTimeStamp = 67200
    timeToWait = nextTimeStamp - recentTimeStamp + 86400 if recentTimeStamp > nextTimeStamp else nextTimeStamp - recentTimeStamp
    while True:
        await asyncio.sleep(timeToWait)
        embed = hungry.hungry()
        await channel.send(client.get_channel('615768384554139699'), embed=embed)
        recentTimeStamp = nextTimeStamp
        nextTimeStamp = selectedTime[(selectedTime.index(nextTimeStamp) + 1) % 3]
        timeToWait = nextTimeStamp - recentTimeStamp + 86400 if recentTimeStamp > nextTimeStamp else nextTimeStamp - recentTimeStamp


client.run(token)
