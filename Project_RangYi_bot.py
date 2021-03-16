# -*- coding: utf-8 -*- 
import asyncio
import discord
import youtube_dl
import datetime
import re
import os
from Modules.help import Help
from Modules.search import Search
from Modules.setting import token
from Modules.baseball import Baseball
from Modules.yacht import *

# Variables
client = discord.Client()
help = Help()
search = Search()
baseball = Baseball()


# functions out of async
def rename(old_dict,old_name,new_name):
    new_dict = {}
    for key,value in zip(old_dict.keys(),old_dict.values()):
        new_key = key if key != old_name else new_name
        new_dict[new_key] = old_dict[key]
    return new_dict

# Discord Client
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-----------------------')
    game = discord.Game("!설명으로 도움말")
    await client.change_presence(status=discord.Status.online, activity=game)


@client.event
async def on_message(message):
    global level, favper, choice
    # 숫자만 가려내기 위해
    noma = re.compile('[0-9]+')
    now = datetime.datetime.now()
    guild = message.guild
    channel = message.channel

    # Bot이 하는 말은 반응하지 않음  
    if message.author.bot:
        return None

    # 봇 설명
    if message.content == "!설명":
        createdEmbed = help.create_help_embed()
        await channel.send(embed=createdEmbed)

    # 봇 분양 관련
    if message.content == '!분양':
        embed = discord.Embed(title="링크를 보내주겠느니라!!", description='여기',
                              url='https://discordapp.com/api/oauth2/authorize'
                                  '?client_id=517176814804926484&permissions=8&scope=bot',
                              colour=0xf7cac9)
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


    # 유튜브 검색
    if message.content.startswith('!검색'):
        msg1 = message.content.split(' ')
        await channel.send(embed=search.search_youtube(msg1[1:]))

    # 사진 검색
    if message.content.startswith('!사진'):
        msg1 = message.content.split(' ')
        await channel.send(embed=search.search_image(msg1[1:]))

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


    if message.content.startswith('!test'):
        msg1 = message.content.split(' ')
        if len(msg1) > 1:
            try:
                id_ = re.findall(noma, msg1[1])
                id__ = await client.get_user_info(id_[0])
                profileurl = id__.avatar_url
            except:
                await channel.send('그 사람은 조회가 불가능하니라...')
        else:
            profileurl = message.author.avatar_url
        embed = discord.Embed(title='asdf', description='casasdf')
        embed.set_image(url=profileurl)
        await channel.send(embed=embed)

async def yacht(guild, channel, user):
    emoji = {'ace':"1️⃣", 'Deuces':'2️⃣', 'Threes':'3️⃣', 'Fours':'4️⃣', 'Fives':'5️⃣', 'Sixes':'6️⃣', 'Choice':'✅', '4 of a Kind':'💳', 'Full House':'🏠', 'Small Straight':'▶', 'Large Straight':'⏩', 'Yacht':'🎰'}
    users = {}
    users, user_dice, index = game_start(users, user)
    print(users)
    print(user_dice)
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
                while True:
                    if turn < 2:
                        await channel.send('고정시킬 칸의 번호를 , 로 나눠서 입력해 주세요. 고정시킬게 없으면 0을 보내주시고 점수를 고르실려면 결정을 보내세요 예)1,3,4 or 1,2 or 3')
                        try:
                            team = await client.wait_for('message', timeout=15.0, check=check)
                        except:
                            del users[index]
                            del user_dice[index]
                            print(users)
                            print(user_dice)
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
                            del users[index]
                            del user_dice[index]
                            print(users)
                            print(user_dice)
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
            del users[index]
            del user_dice[index]
            await channel.send("게임 모두 마쳐졌느니라!")
            if len(users[index]) == 2:
                await channel.send(user[check_winner(users[index])])

                
        
        

    

client.run(token)
