# -*- coding: utf-8 -*- 
import asyncio
import discord
import youtube_dl
import datetime
import re
import json
from Modules.hungry import Hungry
from Modules.morning import Morning
from Modules.help import Help
from Modules.Annseq import Annseq
from selenium import webdriver
from Modules.search import Search
from Modules.user import UserLevel
from Modules.calendar import Calender

# Variables
client = discord.Client()
queues = {}
musiclist = []
suedUser = {}
sueingUser = {}
fcheck = [0]
players = []

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
    #숫자만 가려내기 위해
    noma = re.compile('[0-9]+')
    now = datetime.datetime.now()
    descriptions=''
    resings = ''
    title = ''
    # Bot이 하는 말은 반응하지 않음
    if message.author.bot:
        return None

    # 경험치 상승 처리
    userlevel = UserLevel()
    if userlevel.levelIncrease(message.author, message.content):
        free_chat = client.get_channel('514392468402208768')
        await client.send_message(free_chat, userlevel.showLevel(message.author, True))

    # 봇 설명
    if message.content == "!설명":
        help = Help()
        createdEmbed = help.create_help_embed()
        await client.send_message(message.channel, embed=createdEmbed)

    # 급식 파싱
    if message.content == '!급식':
        hungry = Hungry()
        embed = hungry.hungry()
        await client.send_message(message.channel, embed=embed)

    # 봇 분양 관련
    if message.content == '!분양':
        embed = discord.Embed(title="링크를 보내주겠느니라!!", description = '여기', url = 'https://discordapp.com/api/oauth2/authorize?client_id=517176814804926484&permissions=8&scope=bot', colour=0xf7cac9)
        await client.send_message(message.channel, embed=embed)

    # 아침운동 정보
    if message.content == '!아침운동':
        morningC = Morning()
        weather, dust = morningC.morning()
        now=datetime.datetime.now()
        if now.weekday()>3 and now.weekday()<6:
            embed = discord.Embed(title="세희야! 내일 날씨 알려 주거라!",description='주말이니 편하게 쉬도록 하자꾸나!!', color=0xf7cac9)
            await client.send_message(message.channel, embed=embed)
        else:
            if '비' in weather or '나쁨' in dust:
                embed = discord.Embed(title="세희야! 내일 날씨 알려 주거라!",description='학교도는 날이니라...', color=0xf7cac9)
                await client.send_message(message.channel, embed=embed)
            else:
                embed = discord.Embed(title="세희야! 내일 날씨 알려 주거라!",description='아침운동 해야 할 것 같으니라...', color=0xf7cac9)
                await client.send_message(message.channel, embed=embed)

    # 음악 종료
    if message.content == '!종료':
        server = message.server
        try:
            for key in queues:
                if key == server.id:
                    del queues[server.id]
        except RuntimeError:
            for key in queues:
                if key == server.id:
                    del queues[server.id]
        if musiclist:
            musiclist.clear()
        try:
            voice_client = client.voice_client_in(server)
            await voice_client.disconnect()
            await client.send_message(message.channel, '종료했느니라!!')
        except:
            return

    # 음악 재생
    if message.content.startswith("!재생"):
        if len(players) == 0 or players[0].is_playing() == 0:
            server = message.server
            if client.voice_client_in(server) == None:
                await client.join_voice_channel(message.author.voice.voice_channel)
            voice_client = client.voice_client_in(server)
            msg1 = message.content.split(' ')
            url = msg1[1]
            try:
                player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id, message.channel.id), before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5")
                player.volume = 0.5
                player.start()
                if len(players) == 0:
                    players.append(player)
                else:
                    players[0] = player
                embed=discord.Embed(title="재생하겠느니라!!", description=player.title+"\n"+player.url)
                await client.send_message(message.channel, embed=embed)
            except:
                await client.send_message(message.channel, '유튜브 링크가 아니거나 재생할 수 없는 주소 이니라...')
    
    # 음악 예약
    if message.content.startswith('!예약'):
        try:
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
        except:
            await client.send_message(message.channel,'음성방에 들어가있지 않으면 예약이 불가능하니라...')

    # 음악 큐
    if message.content.startswith('!큐'):
        server = message.server
        msg1 = message.content.split(" ")
        check = msg1[1]
        # 큐 보기
        if check =='보기':
            for i in range(0, len(musiclist)):
                resings = resings + str(i+1) + '번 예약곡' + '-' + ' ' + musiclist[i] + '\n\n'
            embed = discord.Embed(title='대기중인 곡들이니라~', description = resings, color=0xf7cac9)
            await client.send_message(message.channel, embed=embed)
        # 큐에 있는 음악 삭제
        if check=='삭제':
            del musiclist[int(msg1[2])-1]
            del queues[server.id][int(msg1[2])-1]
            print(musiclist)
            print(queues)
            await client.send_message(message.channel, msg1[2]+ '번 예약곡을 취소 했느니라!')

    # 서버 글 삭제
    if message.content.startswith('!삭제'):
        msg = message.content.split(' ')
        try:
            if int(msg[1]) < 100:
                await client.purge_from(message.channel, limit=int(msg[1]))
        except:
            return
    
    # 발표 순서 정하기
    if message.content.startswith('!발표'):
        ann = Annseq()
        msg1 = message.content.split(' ')
        if len(msg1) > 1:
            annsequence = ann.rand_self(msg1[1:])
        else:
            annsequence = ann.rand()
        embed = discord.Embed(title='발표순서이니라!!', description = annsequence, color=0xf7cac9)
        await client.send_message(message.channel, embed=embed) 

    # 유튜브 검색
    if message.content.startswith('!검색'):
        search = Search()
        msg1 = message.content.split(' ')
        await client.send_message(message.channel, embed=search.get_video_link(msg1[1:]))

    # 사진 검색
    if message.content.startswith('!사진'):
        search = Search()
        msg1 = message.content.split(' ')
        await client.send_message(message.channel, embed=search.search_image(msg1[1:]))

    # 유저 레벨 관련
    if message.content.startswith('!레벨'):
        msg1 = message.content.split(' ')
        if len(msg1) > 1:
            try:
                id_ = re.findall(noma, msg1[1])
                id__ = await client.get_user_info(id_[0])
                await client.send_message(message.channel, userlevel.showLevel(id__))  # 유저 지정 처리
            except:
                await client.send_message(message.channel, '그 사람은 조회가 불가능하니라...')
        else:
            await client.send_message(message.channel, userlevel.showLevel(message.author))

    # 서버 레벨 랭킹
    if message.content == '!랭킹':
        rank = userlevel.showRanking(message.server)
        if len(rank['data'].keys()) > 10:
            rankLength = 10
        else:
            rankLength = len(rank['data'].keys())
        embed = discord.Embed(title='서버의 랭킹이니라!', description='10위까지 표시되느니라~')
        count = 0
        for user in rank['data'].keys():
            count += 1
            userobj = await client.get_user_info(user)
            embed.add_field(name='**'+userobj.name+'**', value="{} 레벨\n현재 경험치: **{} XP**, 다음 레벨까지 {} XP".format(rank['data'][user]['level'], rank['data'][user]['currentxp'], rank['data'][user]['targetxp'] - rank['data'][user]['currentxp']), inline = False)
            if count > rankLength - 1:
                break;

        await client.send_message(message.channel, embed=embed)


    # 고소 관련
    if message.content.startswith('!고소'):
        server = message.server
        msg1 = message.content.split(' ')
        id_ = re.findall(noma, msg1[1])
        if fcheck[0] == 0:
            role = discord.utils.get(server.roles, name="COMPLAINTS")
            if id_ == []: # ? 고소할 상대를 찾지 못했을때
                await client.send_message(message.channel, '그런 사람은 찾을 수 없느니라...')
            elif id_[0] == message.author.id: # ? 자기 자신을 고소하려고 할때
                await client.send_message(message.channel, '자기 자신은 고소할 수 없느니라....')
            elif server.get_member(id_[0]) == None:
                await client.send_message(message.channel, '그런 사람은 고소할 수 없느니라....')
            elif server.get_member(id_[0]).bot:
                await client.send_message(message.channel, '봇은 고소할 수 없느니라....')
            else:
                id__ = await client.get_user_info(id_[0])
                gosomember = server.get_member(id_[0])
                if str(message.author.id) not in list(suedUser.keys()):
                    suedUser[str(message.author.id)] = {}
                suedUser[str(message.author.id)][str(gosomember.id)] = gosomember.roles 
                if str(message.author.id) not in list(sueingUser.keys()):
                    sueingUser[str(message.author.id)] = message.author.roles
                # ? 고소장 보내기(개인 메세지)
                em = discord.Embed(title='고-소-장', description = "<@"+message.author.id+">" + "님이 당신을 고소하였느니라!! 법정에서 해결하자꾸나!", color=0xf7cac9)
                await client.send_message(id__, embed = em)
                for i in gosomember.roles:
                    if i.name == '@everyone':
                        continue
                    else:
                        await client.remove_roles(gosomember, i)
                for i in message.author.roles:
                    if i.name == '@everyone':
                        continue
                    else:
                        await client.remove_roles(message.author, i)  
                await client.add_roles(message.author, role)
                await client.add_roles(gosomember, role)
                await client.send_message(message.author, ':white_check_mark: 고소장을 무사히 보냈느니라!~~')
                fcheck[0] = 1
        elif fcheck[0] == 1:
            if str(message.author.id) in list(suedUser.keys()): # Preventing Possible Error
                    gosomember = server.get_member(id_[0])
                    try:
                        suedUser[str(message.author.id)][str(gosomember.id)]
                        await client.send_message(message.channel, '이미 고소 했느니라...')
                    except KeyError:
                        await client.send_message(message.channel, '고소중에 고소할 수 없느니라...')
            else:                    
                await client.send_message(message.channel, ':negative_squared_cross_mark: 재판이 진행중이니라....')

    # 고소 취하
    if message.content.startswith('!취하'): 
        server = message.server
        msg1 = message.content.split(' ')
        id_ = re.findall(noma, msg1[1])
        if id_ == []: # ? 고소할 상대를 찾지 못했을때
            await client.send_message(message.channel, '그런 사람은 찾을 수 없느니라...')
            return
        id__ = client.get_user_info(id_[0])
        gosomember = server.get_member(id_[0])
        try:
            if str(gosomember.id) not in suedUser[str(message.author.id)]: # ? 고소하지 않은 사람과 취하하려고 할때
                await client.send_message(message.channel, '고소하지 않은 사람의 고소는 취하할 수 없느니라..')
            else:
                #? 미래에 머나먼 미래에 혹시 여러명을 고소하지는 않을까 하는 걱정으로 남겨둠
                # id__ = await client.get_user_info(id_[0]) 시발쓰지 마세요 한국의 전통 문화 입니다 미래의 서울 오버-시어 C-8
                # em = discord.Embed(title='고-소-장', description = "<@"+message.author.id+">" + "님이 당신을 고소하였느니라!! 법정에서 해결하자꾸나!", color=0xf7cac9)
                # await client.send_message(id__, embed = em)
                _role = discord.utils.get(server.roles, name="COMPLAINTS")
                await client.remove_roles(gosomember, _role)
                await client.remove_roles(message.author, _role)
                for role in suedUser[str(message.author.id)][str(gosomember.id)]:
                    if role.name == '@everyone':
                        continue
                    else:
                        await client.add_roles(gosomember, role)
                for role in sueingUser[str(message.author.id)]:
                    if role.name == '@everyone':
                        continue
                    else:
                        await client.add_roles(message.author, role)
                
                await client.send_message(gosomember, ':white_check_mark: 취하가 완료되었느니라~')
                await client.send_message(message.author, ':white_check_mark: 취하가 완료되었느니라~')
                fcheck[0] = 0
        except KeyError:
            await client.send_message(message.channel, '고소하지 않고 취하할 수 없느니라...')

    if message.content == '!일정':
        cal = Calender()
        title = "%s년 %s월의 학사일정이니라!" % (now.year, now.month)
        em = discord.Embed(title=title, description=cal.get_calendar(), colour=0xf7cac9)
        await client.send_message(message.channel, embed=em)


client.run('token')
