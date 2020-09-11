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
#from Modules.user import UserLevel
from Modules.schoolcalendar import Calender
from Modules.gamesave import Save
from Modules.game_play import Game
from Modules.setting import token
from Modules.baseball import Baseball
from Modules.yacht import *

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
# def check_queue(qid, channel, info):
#     if queues[qid]:
#         song_there = os.path.isfile(".mp3")
#         if song_there:
#             os.remove("reservsong.mp3")
#         player = queues[qid].pop(0)
#         embed = discord.Embed(title="재생하겠느니라!!", description=musiclist[0] + "\n" + info["url"])
#         del musiclist[0]
#         say = channel.send(embed=embed)
#         asyncio.run_coroutine_threadsafe(say, client.loop)
#         voice.play(player, after=lambda: check_queue(guild.id, message.channel, info))


# Discord Client
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-----------------------')
    game = discord.Game("!설명으로 도움말")
    await client.change_presence(status=discord.Status.online, activity=game)

    #loop.create_task(realtime())


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
    #userlevel = UserLevel()
    hungry = Hungry()
    morningC = Morning()
    ann = Annseq()
    search = Search()
    cal = Calender()
    save = Save()
    game = Game()
    baseball = Baseball()
    player=0
    # Bot이 하는 말은 반응하지 않음  

    if message.author.bot:
        return None

    # 경험치 상승 처리
            # if userlevel.levelIncrease(message.author, message.content):
            # await channel.send(free_chat, userlevel.showLevel(message.author, True))

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
    
    if message.content.startswith("!야추"):
        a = []
        a.append(message.author.name)
        msg = message.content.split(' ')
        if len(msg) > 1:
            if msg[1] == "도움":
                embed = discord.Embed(title="야추 도움말", description='점수 계산법 보기', url='https://namu.wiki/w/%EC%9A%94%ED%8A%B8(%EA%B2%8C%EC%9E%84)?from=%EC%95%BC%EC%B6%94#s-2.2', color=0xf7cac9)
                embed.add_field(name="!야추 [플레이어 언급]", value='언급을 통해 친구와 2명이서 또는 !야추 입력으로 혼자하기가 가능하니라.', inline=False)
                embed.add_field(name="규칙", value="51 Worldwide Games에 수록된 Yacht dice 의 규칙을 따르느니라\n 위에 점수 계산법 보기를 눌러서 점수 계산법을 익히고 오는게 좋으니라", inline=False)
                await channel.send(embed=embed)
                return
            try:
                id_ = re.findall(noma, msg[1])
                id_ = await client.fetch_user(id_[0])
                a.append(id_.name)
            except:
                await channel.send('없는 유저 이거나 고를 수 없는 유저입니다. 다시 해주세요.')
                return
        await yacht(message.guild, message.channel, a)

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

    if message.content.startswith("!야구"):
        msg1 = message.content.split(' ')
        if len(msg1) > 1:
            try:
                inning, embed1, embed2 = baseball.showBaseballScore(msg1[1])
                await channel.send(str(inning))
                await channel.send(embed = embed1)
                await channel.send(embed = embed2)
            except:
                await channel.send('팀명이 잘못됬거나 경기중이 아닙니다.')

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

    # # 고소 관련
    # if message.content.startswith('!고소'):
    #     msg1 = message.content.split(' ')
    #     id_ = re.findall(noma, msg1[1])
    #     if fcheck[0] == 0:
    #         role = discord.utils.get(guild.roles, name="COMPLAINTS")
    #         if not id_:  # ? 고소할 상대를 찾지 못했을때
    #             await channel.send('그런 사람은 찾을 수 없느니라...')
    #         elif id_[0] == message.author.id:  # ? 자기 자신을 고소하려고 할때
    #             await channel.send('자기 자신은 고소할 수 없느니라....')
    #         elif guild.get_member(id_[0]) is None:
    #             await channel.send('그런 사람은 고소할 수 없느니라....')
    #         elif guild.get_member(id_[0]).bot:
    #             await channel.send('봇은 고소할 수 없느니라....')
    #         else:
    #             id__ = await client.get_user_info(id_[0])
    #             gosomember = guild.get_member(id_[0])
    #             if str(message.author.id) not in list(suedUser.keys()):
    #                 suedUser[str(message.author.id)] = {}
    #             suedUser[str(message.author.id)][str(gosomember.id)] = gosomember.roles
    #             if str(message.author.id) not in list(sueingUser.keys()):
    #                 sueingUser[str(message.author.id)] = message.author.roles
    #             # ? 고소장 보내기(개인 메세지)
    #             em = discord.Embed(title='고-소-장',
    #                                description="<@" + message.author.id + ">" + "님이 당신을 고소하였느니라!! 법정에서 해결하자꾸나!",
    #                                color=0xf7cac9)
    #             await channel.send(id__, embed=em)
    #             for i in gosomember.roles:
    #                 if i.name == '@everyone':
    #                     continue
    #                 else:
    #                     await client.remove_roles(gosomember, i)
    #             for i in message.author.roles:
    #                 if i.name == '@everyone':
    #                     continue
    #                 else:
    #                     await client.remove_roles(message.author, i)
    #             await client.add_roles(message.author, role)
    #             await client.add_roles(gosomember, role)
    #             await channel.send(message.author, ':white_check_mark: 고소장을 무사히 보냈느니라!~~')
    #             fcheck[0] = 1
    #     elif fcheck[0] == 1:
    #         if str(message.author.id) in list(suedUser.keys()):  # Preventing Possible Error
    #             gosomember = guild.get_member(id_[0])
    #             try:
    #                 suedUser[str(message.author.id)][str(gosomember.id)]
    #                 await channel.send('이미 고소 했느니라...')
    #             except KeyError:
    #                 await channel.send('고소중에 고소할 수 없느니라...')
    #         else:
    #             await channel.send(':negative_squared_cross_mark: 재판이 진행중이니라....')

    # # 고소 취하
    # if message.content.startswith('!취하'):
    #     msg1 = message.content.split(' ')
    #     id_ = re.findall(noma, msg1[1])
    #     if not id_:  # ? 고소할 상대를 찾지 못했을때
    #         await channel.send('그런 사람은 찾을 수 없느니라...')
    #         return
    #     # id__ = client.get_user_info(id_[0])
    #     gosomember = guild.get_member(id_[0])
    #     try:
    #         if str(gosomember.id) not in suedUser[str(message.author.id)]:  # ? 고소하지 않은 사람과 취하하려고 할때
    #             await channel.send('고소하지 않은 사람의 고소는 취하할 수 없느니라..')
    #         else:
    #             # ? 미래에 머나먼 미래에 혹시 여러명을 고소하지는 않을까 하는 걱정으로 남겨둠
    #             # id__ = await client.get_user_info(id_[0]) 시발쓰지 마세요 한국의 전통 문화 입니다 미래의 서울 오버-시어 C-8
    #             # em = discord.Embed(title='고-소-장',
    #             #                    description="<@"+message.author.id+">" + "님이 당신을 고소하였느니라!! 법정에서 해결하자꾸나!",
    #             #                    color=0xf7cac9)
    #             # await channel.send(id__, embed = em)
    #             _role = discord.utils.get(guild.roles, name="COMPLAINTS")
    #             await client.remove_roles(gosomember, _role)
    #             await client.remove_roles(message.author, _role)
    #             for role in suedUser[str(message.author.id)][str(gosomember.id)]:
    #                 if role.name == '@everyone':
    #                     continue
    #                 else:
    #                     await client.add_roles(gosomember, role)
    #             for role in sueingUser[str(message.author.id)]:
    #                 if role.name == '@everyone':
    #                     continue
    #                 else:
    #                     await client.add_roles(message.author, role)

    #             await channel.send(gosomember, ':white_check_mark: 취하가 완료되었느니라~')
    #             await channel.send(message.author, ':white_check_mark: 취하가 완료되었느니라~')
    #             fcheck[0] = 0
    #     except KeyError:
    #         await channel.send('고소하지 않고 취하할 수 없느니라...')

    if message.content == '!일정':
        title = "%s년 %s월의 학사일정이니라!" % (now.year, now.month)
        em = discord.Embed(title=title, description=cal.get_calendar(), colour=0xf7cac9)
        await channel.send(embed=em)

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
        await channel.send(client.get_channel('급식을 내보낼 채널의 id'), embed=embed)
        recentTimeStamp = nextTimeStamp
        nextTimeStamp = selectedTime[(selectedTime.index(nextTimeStamp) + 1) % 3]
        timeToWait = nextTimeStamp - recentTimeStamp + 86400 if recentTimeStamp > nextTimeStamp else nextTimeStamp - recentTimeStamp

def rename(old_dict,old_name,new_name):
    new_dict = {}
    for key,value in zip(old_dict.keys(),old_dict.values()):
        new_key = key if key != old_name else new_name
        new_dict[new_key] = old_dict[key]
    return new_dict

async def yacht(guild, channel, user):
    emoji = {'ace':"1️⃣", 'Deuces':'2️⃣', 'Threes':'3️⃣', 'Fours':'4️⃣', 'Fives':'5️⃣', 'Sixes':'6️⃣', 'Choice':'✅', '4 of a Kind':'💳', 'Full House':'🏠', 'Small Straight':'▶', 'Large Straight':'⏩', 'Yacht':'🎰'}
    users = {}
    users, user_dice, index = game_start(users, user)
    while True:
        for u in range(len(user)):
            await channel.send(user[u]+"차례")
            def check(m):
                return m.channel == channel and m.author.name == user[u]
            user_dice[index] = {1: 1, 2:1, 3: 1, 4: 1, 5: 1}
            endFlag = False
            for turn in range(3):
                if endFlag == True:
                    break
                dice = ''
                dicelist = roll_dice(user_dice[index])
                board = dice_check(dicelist)
                for j in dicelist.keys():
                    if type(j) == str:
                        dice += '['+str(dicelist[j])+']' + ' '
                    else:
                        dice += str(dicelist[j])+' '
                await channel.send(dice)
                await channel.send('고정시킬 칸의 번호를 , 로 나눠서 입력해 주세요. 고정시킬게 없으면 0을 보내주시고 점수를 고르실려면 결정을 보내세요 예)1,3,4 or 1,2 or 3')
                while True:
                    try:
                        team = await client.wait_for('message', timeout=15.0, check=check)
                    except:
                        return await channel.send("게임이 종료 됬느니라....")
                    if team.content == "결정" or turn == 2:
                        scorelist = []
                        embed = discord.Embed(title="점수 목록", color=0xf7cac9)
                        for i in board.keys():
                            if users[index][u][0][i] == False:
                                if i == 'Choice' or i == '4 of a Kind' or i == 'Full House':
                                    scorelist.append(i)
                                    if board[i] == 0:
                                        embed.add_field(name=i, value=0)
                                    else:
                                        embed.add_field(name=i, value=plus_all(dicelist))
                                elif i == 'Small Straight':
                                    scorelist.append(i)
                                    if board[i] == 0:
                                        embed.add_field(name=i, value=0)
                                    else:
                                        embed.add_field(name=i, value='15')
                                elif i == 'Large Straight':
                                    scorelist.append(i)
                                    if board[i] == 0:
                                        embed.add_field(name=i, value=0)
                                    else:
                                        embed.add_field(name=i, value='30')
                                elif i=='Yacht':
                                    scorelist.append(i)
                                    if board[i] == 0:
                                        embed.add_field(name=i, value=0)
                                    else:
                                        embed.add_field(name=i, value='50')
                                else:
                                    scorelist.append(i)
                                    num = get_num(dicelist)
                                    for h in enum.keys():
                                        if enum[h] == i:
                                            if board[i] == 0:
                                                embed.add_field(name=i, value=0)
                                            else:
                                                embed.add_field(name=i, value=str(int(h)*num[h]))
                        
                        def reaction_check(reaction, user):
                            return user == team.author and str(reaction.emoji) == '1️⃣' or str(reaction.emoji) == '2️⃣' or str(reaction.emoji) == '3️⃣' or str(reaction.emoji) == '4️⃣' or str(reaction.emoji) == '5️⃣' or str(reaction.emoji) == '6️⃣' or str(reaction.emoji) == '✅' or str(reaction.emoji) == '💳' or str(reaction.emoji) == '🏠' or str(reaction.emoji) == '▶' or str(reaction.emoji) == '⏩' or str(reaction.emoji) == '🎰'
                        a = await channel.send(embed=embed)
                        if scorelist == []:
                            scorelist = emoji.keys()
                        for i in scorelist:
                            if i == "Bonus":
                                continue
                            await a.add_reaction(emoji[i])
                        await asyncio.sleep(1)
                        try:
                            reaction, reactuser = await client.wait_for('reaction_add', timeout=15.0, check=reaction_check)
                        except:
                            return await channel.send("게임이 종료 됬느니라....")
                        def change_sheet(reaction, board):
                            for i in emoji.keys():
                                if emoji[i] == reaction.emoji:
                                    for j in enum.keys():
                                        if enum[j] == i:
                                            if board[i] == 0:
                                                users[index][u][0][i] = '[0]'
                                                users[index][u][1]['score'] += 0
                                                users[index][u][1][int(j)] += 0
                                                break
                                            else:
                                                users[index][u][0][i] = int(j)*num[j]
                                                users[index][u][1]['score'] += int(j)*num[j]
                                                users[index][u][1][int(j)] += int(j)*num[j]
                                                break
                                    if emoji[i] == '✅' or emoji[i] == '💳' or emoji[i] == '🏠':
                                        if board[i] == 0:
                                            users[index][u][0][i] = '[0]'
                                            users[index][u][1]['score'] += 0
                                            break
                                        else:
                                            users[index][u][0][i] = plus_all(dicelist)
                                            users[index][u][1]['score'] += plus_all(dicelist)
                                            break

                                    if emoji[i] == '▶':
                                        if board[i] == 0:
                                            users[index][u][0][i] = '[0]'
                                            users[index][u][1]['score'] += 0
                                            break
                                        else:
                                            users[index][u][0][i] = 15
                                            users[index][u][1]['score'] += 15
                                            break
                                    
                                    if emoji[i] == '⏩':
                                        if board[i] == 0:
                                            users[index][u][0][i] = '[0]'
                                            users[index][u][1]['score'] += 0
                                            break
                                        else:
                                            users[index][u][0][i] = 30
                                            users[index][u][1]['score'] += 30
                                            break
                                                
                                    if emoji[i] == '🎰':
                                        if board[i] == 0:
                                            users[index][u][0][i] = '[0]'
                                            users[index][u][1]['score'] += 0
                                            break
                                        else:
                                            users[index][u][0][i] = 50
                                            users[index][u][1]['score'] += 50
                                            break
                                            
                        await a.delete()
                        change_sheet(reaction, board)
                        user_dice[index] = {1: 1, 2:1, 3: 1, 4: 1, 5: 1} 
                        if homework(users[index][u][1]):
                            users[index][u][0]['Bonus'] = 35
                            users[index][u][1]['score'] += 35
                            await channel.send(user[u] + '숙제 다 마쳤느니라!')

                        for asdf in range(len(user)):
                            embed = discord.Embed(title=user[asdf]+"님의 점수판", color=0xf7cac9)
                            for i in users[index][u][0].keys():
                                if users[index][u][0][i] == False:
                                    embed.add_field(name=i, value=0)
                                else:
                                    embed.add_field(name=i, value=users[index][u][0][i])
                            embed.add_field(name='score', value=users[index][u][1]['score'], inline=False)
                            await channel.send(embed = embed)
                        endFlag = True
                        break

                    else:
                        msg = list(reversed(team.content.split(',')))
                        try:
                            a = int(msg[0])
                        except:
                            continue
                        for i in msg:
                            if i == '' or int(i) > 5 or i == '0':
                                continue
                            else:
                                try:
                                    user_dice[index][i] = user_dice[index][i]
                                    user_dice[index] = rename(user_dice[index], i, int(i))
                                except:
                                    user_dice[index] = rename(user_dice[index], int(i), i)
                        break
                        

        if check_score(users[index]):
            await channel.send("게임 모두 마쳐졌느니라!")
            if len(users[index]) == 2:
                await channel.send(user[check_winner(users[index])])

                
        
        

    

client.run(token)
