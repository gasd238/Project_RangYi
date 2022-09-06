# -*- coding: utf-8 -*-
import asyncio
import discord
import datetime
import re
import pymongo
from Modules.help import Help
from Modules.search import Search
from Modules.setting import *
from Modules.baseball import Baseball
from Modules.yacht import *
from Modules.user import *
from Modules.doge import PrintDoge
import emoji

# Variables
client = discord.Client(intents=discord.Intents.all())
help = Help()
search = Search()
baseball = Baseball()
userlevel = UserLevel()
ban = Ban()
doge = PrintDoge()

custom_emoji = re.compile("([\:])(.*?)([\:])")

# 유지 보수시 레벨업 방지
userFuncActive = True

# functions out of async
def rename(old_dict, old_name, new_name):
    new_dict = {}
    for key, value in zip(old_dict.keys(), old_dict.values()):
        new_key = key if key != old_name else new_name
        new_dict[new_key] = old_dict[key]
    return new_dict


# discord Client
@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("-----------------------")
    game = discord.Game("!설명으로 도움말")
    await client.change_presence(status=discord.Status.online, activity=game)
    asyncio.new_event_loop()
    loop = asyncio.get_running_loop()
    loop.create_task(checkcoin())


@client.event
async def on_message(message):
    # 숫자만 가려내기 위해
    noma = re.compile("[0-9]+")
    now = datetime.datetime.now()
    try:
        guild = message.guild
        ad = guild.audit_logs()
    except:
        pass
    channel = message.channel
    result = bancol.find_one({"userid": message.author.id})

    # Bot이 하는 말은 반응하지 않음
    if message.author.bot:
        return None
    # 밴 된 사람은 반응하지
    if result:
        return None

    # 봇 설명
    if message.content == "!설명":
        createdEmbed = help.create_help_embed()
        await channel.send(embed=createdEmbed)

    if userFuncActive:
        # 경험치 상승 처리
        if userlevel.levelIncrease(message.author, message.content):
            await channel.send(
                embed=userlevel.showLevel(
                    message.author, message.author.avatar_url, True
                )
            )
            # 유저 레벨 관련
        if message.content.startswith("!레벨"):
            msg1 = message.content.split(" ")
            if len(msg1) > 1:
                try:
                    id_ = re.findall(noma, msg1[1])
                    id__ = await client.fetch_user(int(id_[0]))
                    profileurl = id__.avatar.url
                    await channel.send(
                        embed=userlevel.showLevel(id__, profileurl)
                    )  # 유저 지정 처리
                except TypeError:
                    await channel.send("그 사람은 조회가 불가능하니라...")
            else:
                await channel.send(
                    embed=userlevel.showLevel(message.author, message.author.avatar.url)
                )

        # 밴 관련
        if message.content.startswith('!밴'):
            msg1 = message.content.split(' ')
            if len(msg1) > 1:
                try:
                    id_ = re.findall(noma, msg1[1])
                    id__ = await client.fetch_user(int(id_[0]))
                    await channel.send(ban.banUser(id__))

                except discord.discordException:
                    await channel.send('그 사람은 조회가 불가능하니라...')
                except TypeError:
                    await channel.send('그 사람은 조회가 불가능하니라...')

        # 서버 레벨 랭킹
        if message.content == "!랭킹":
            rank = userlevel.showRanking(guild)
            count = len(rank)
            if count > 10:
                rankLength = 10
            else:
                rankLength = count
            if rankLength == 0:
                embed = discord.Embed(title="서버의 랭킹이니라!", description="표시할 사람이 없습니다.")
            else:
                embed = discord.Embed(
                    title="서버의 랭킹이니라!", description="{}위까지 표시되느니라~".format(rankLength)
                )
            count = 0
            for doc in rank:
                count += 1
                userobj = await client.fetch_user(doc["userid"])
                embed.add_field(
                    name="**" + "{}등 ".format(str(count)) + userobj.name + "**",
                    value="{} 레벨\n현재 경험치: **{} XP**,"
                    "다음 레벨까지 {} XP".format(
                        doc["level"],
                        doc["currentxp"],
                        userlevel.LevelExpGetter(doc["level"]) - doc["currentxp"],
                    ),
                    inline=False,
                )
                if count > rankLength - 1:
                    break

            await channel.send(embed=embed)

    # 봇 분양 관련
    if message.content == "!초대":
        await channel.send("내 프로필을 누르고 서버에 추가를 누르면 되느니라!!")

    if message.content.startswith("!야추"):
        a = []
        a.append(message.author.name)
        msg = message.content.split(" ")
        if len(msg) == 2:
            if msg[1] == "도움":
                embed = discord.Embed(
                    title="야추 도움말",
                    description="점수 계산법 보기",
                    url="https://namu.wiki/w/%EC%9A%94%ED%8A%B8(%EA%B2%8C%EC%9E%84)?from=%EC%95%BC%EC%B6%94#s-2.2",
                    color=0xF7CAC9,
                )
                embed.add_field(
                    name="!야추 [플레이어 언급]",
                    value="언급을 통해 친구와 2명이서 또는 !야추 혼자 입력으로 혼자하기가 가능하니라.",
                    inline=False,
                )
                embed.add_field(
                    name="규칙",
                    value="Nintentdo Switch 51 Worldwide Games에 수록된 Yacht dice 의 규칙을 따르느니라\n 위에 점수 계산법 보기를 눌러서 점수 계산법을 익히고 오는게 좋으니라",
                    inline=False,
                )
                embed.add_field(
                    name="!야추 이모티콘",
                    value="자신이 먹을 점수 선택시 이모티콘을 누르는 방식으로 고르게 되는데 각 이모티콘이 무엇을 의미하는지에 대한 설명이니라!",
                    inline=False,
                )
                return await channel.send(embed=embed)

            elif msg[1] == '이모티콘':            
                return await channel.send(embed=await yacht(1,1,1))
            else:
                try:
                    if msg[1] != "혼자":
                        id_ = re.findall(noma, msg[1])
                        id_ = await client.fetch_user(id_[0])
                        a.append(id_.name)
                except:
                    return await channel.send("없는 유저거나 고를 수 없는 상대이니라..")

        else:
            return await channel.send("한명만 골라주거라...")

        await yacht(message.guild, message.channel, a)

    # 서버 글 삭제
    if message.content.startswith("!삭제"):
        msg = message.content.split(" ")
        try:
            if int(msg[1]) < 100:
                await message.delete()
                await message.channel.purge(limit=int(msg[1]))
            else:
                await message.delete()
                await channel.send("100개 이상 메세지는 삭제할 수 없느니라....")
        except discord.discordException:
            return

    if message.content.startswith("!test"):
        msg1 = message.content.split(" ")
        if len(msg1) > 1:
            try:
                id_ = re.findall(noma, msg1[1])
                id__ = await client.get_user_info(id_[0])
                profileurl = id__.avatar_url
            except:
                await channel.send("그 사람은 조회가 불가능하니라...")
        else:
            profileurl = message.author.avatar_url
        embed = discord.Embed(title="asdf", description="casasdf")
        embed.set_image(url=profileurl)
        await channel.send(embed=embed)

    # 유튜브 검색
    if message.content.startswith("!검색"):
        msg1 = message.content.split(" ")
        await channel.send(embed=search.search_youtube(msg1[1:]))

    # 사진 검색
    if message.content.startswith("!사진"):
        msg1 = message.content.split(" ")
        await channel.send(embed=search.search_image(msg1[1:]))

    if message.content.startswith("!야구"):
        msg1 = message.content.split(" ")
        if len(msg1) > 1:
            try:
                date, inning, embed1, embed2 = baseball.showBaseballScore(msg1[1])
                if date != "":
                    await channel.send(str(date))
                await channel.send(str(inning))
                await channel.send(embed=embed1)
                await channel.send(embed=embed2)
            except:
                await channel.send('팀명이 잘못됬거나 존재하지 않는 팀이니라..')


async def yacht(guild, channel, user):
    emoji = {
        "ace": "1️⃣",
        "Deuces": "2️⃣",
        "Threes": "3️⃣",
        "Fours": "4️⃣",
        "Fives": "5️⃣",
        "Sixes": "6️⃣",
        "Choice": "✅",
        "4 of a Kind": "💳",
        "Full House": "🏠",
        "Small Straight": "▶",
        "Large Straight": "⏩",
        "Yacht": "🎰",
    }
    users = {}
    scorelist = []
    if guild == 1 and channel == 1 and user == 1:
        embed = discord.Embed(
                    title="야추 이모티콘",
                    description="각 이모티콘별 의미",
                    color=0xF7CAC9,
                )
        for i in emoji.keys():
            embed.add_field(name = emoji[i], value = i)
        return embed
    users, user_dice, index = game_start(users, user)
    while True:
        for u in range(len(user)):
            await channel.send(user[u] + "차례")

            def check(m):
                return m.channel == channel and m.author.name == user[u]

            user_dice[index] = {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}
            endFlag = False
            for turn in range(3):
                if endFlag == True:
                    break
                user_dice[index] = roll_dice(user_dice[index])
                while True:
                    dice = diceset(user_dice[index])
                    await channel.send(dice)
                    if turn < 2:
                        await channel.send(
                            "고정시킬 칸의 번호를 , 로 나눠서 입력해 주거라. 고정시킬게 없으면 0을 보내고 점수를 고를거면 결정을 보내거라! 예)1,3,4 or 1,2 or 3\n한번더 입력시 고정 해제"
                        )
                        try:
                            team = await client.wait_for(
                                "message", timeout=30.0, check=check
                            )
                        except:
                            del users[index]
                            del user_dice[index]
                            return await channel.send("게임이 종료 됬느니라....")
                    if team.content == "결정" or turn == 2:
                        board = dice_check(user_dice[index])
                        embed = discord.Embed(title="점수 목록", color=0xF7CAC9)
                        for i in board.keys():
                            if users[index][u][0][i] == False:
                                if (
                                    i == "Choice"
                                    or i == "4 of a Kind"
                                    or i == "Full House"
                                ):
                                    scorelist.append(i)
                                    if board[i] == 0 and i != "Choice":
                                        embed.add_field(name=i, value=0)
                                    else:
                                        embed.add_field(
                                            name=i, value=plus_all(user_dice[index])
                                        )
                                elif i == "Small Straight":
                                    scorelist.append(i)
                                    if board[i] == 0:
                                        embed.add_field(name=i, value=0)
                                    else:
                                        embed.add_field(name=i, value="15")
                                elif i == "Large Straight":
                                    scorelist.append(i)
                                    if board[i] == 0:
                                        embed.add_field(name=i, value=0)
                                    else:
                                        embed.add_field(name=i, value="30")
                                elif i == "Yacht":
                                    scorelist.append(i)
                                    if board[i] == 0:
                                        embed.add_field(name=i, value=0)
                                    else:
                                        embed.add_field(name=i, value="50")
                                else:
                                    scorelist.append(i)
                                    num = get_num(user_dice[index])
                                    for h in enum.keys():
                                        if enum[h] == i:
                                            if board[i] == 0:
                                                embed.add_field(name=i, value=0)
                                            else:
                                                embed.add_field(
                                                    name=i, value=str(int(h) * num[h])
                                                )

                        def reaction_check(reaction, user):
                            return (
                                user == team.author
                                and str(reaction.emoji) == "1️⃣"
                                or str(reaction.emoji) == "2️⃣"
                                or str(reaction.emoji) == "3️⃣"
                                or str(reaction.emoji) == "4️⃣"
                                or str(reaction.emoji) == "5️⃣"
                                or str(reaction.emoji) == "6️⃣"
                                or str(reaction.emoji) == "✅"
                                or str(reaction.emoji) == "💳"
                                or str(reaction.emoji) == "🏠"
                                or str(reaction.emoji) == "▶"
                                or str(reaction.emoji) == "⏩"
                                or str(reaction.emoji) == "🎰"
                            )

                        a = await channel.send(embed=embed)
                        if scorelist == []:
                            scorelist = emoji.keys()
                        for i in scorelist:
                            if i == "Bonus":
                                continue
                            await a.add_reaction(emoji[i])
                        await asyncio.sleep(1)
                        try:
                            reaction, reactuser = await client.wait_for(
                                "reaction_add", timeout=30.0, check=reaction_check
                            )
                        except:
                            del users[index]
                            del user_dice[index]
                            return await channel.send("게임이 종료 됬느니라....")

                        def change_sheet(reaction, users, board, index, u):
                            for i in emoji.keys():
                                if emoji[i] == reaction.emoji:
                                    for j in enum.keys():
                                        if enum[j] == i:
                                            if board[i] == 0:
                                                users[index][u][0][i] = "[0]"
                                                users[index][u][1]["score"] += 0
                                                users[index][u][1][int(j)] += 0
                                                break
                                            else:
                                                users[index][u][0][i] = int(j) * num[j]
                                                users[index][u][1]["score"] += (
                                                    int(j) * num[j]
                                                )
                                                users[index][u][1][int(j)] += (
                                                    int(j) * num[j]
                                                )
                                                break
                                    if (
                                        emoji[i] == "✅"
                                        or emoji[i] == "💳"
                                        or emoji[i] == "🏠"
                                    ):
                                        if board[i] == 0 and emoji[i] != "✅":
                                            users[index][u][0][i] = "[0]"
                                            users[index][u][1]["score"] += 0
                                            break
                                        else:
                                            users[index][u][0][i] = plus_all(user_dice[index])
                                            users[index][u][1]["score"] += plus_all(
                                                user_dice[index]
                                            )
                                            break

                                    if emoji[i] == "▶":
                                        if board[i] == 0:
                                            users[index][u][0][i] = "[0]"
                                            users[index][u][1]["score"] += 0
                                            break
                                        else:
                                            users[index][u][0][i] = 15
                                            users[index][u][1]["score"] += 15
                                            break

                                    if emoji[i] == "⏩":
                                        if board[i] == 0:
                                            users[index][u][0][i] = "[0]"
                                            users[index][u]["score"] += 0
                                            break
                                        else:
                                            users[index][u][0][i] = 30
                                            users[index][u][1]["score"] += 30
                                            break

                                    if emoji[i] == "🎰":
                                        if board[i] == 0:
                                            users[index][u][0][i] = "[0]"
                                            users[index][u][1]["score"] += 0
                                            break
                                        else:
                                            users[index][u][0][i] = 50
                                            users[index][u][1]["score"] += 50
                                            break
                            return users

                        await a.delete()
                        users = change_sheet(reaction, users, board, index, u)
                        if homework(users[index][u][1]):
                            users[index][u]["Bonus"] = 35
                            users[index][u][1]["score"] += 35
                            await channel.send(user[u] + "숙제 다 마쳤느니라!")

                        for asdf in range(len(user)):
                            embed = discord.Embed(
                                title=user[asdf] + "님의 점수판", color=0xF7CAC9
                            )
                            for i in users[index][asdf][0].keys():
                                if users[index][asdf][0][i] == False:
                                    embed.add_field(name=i, value=0)
                                else:
                                    embed.add_field(
                                        name=i, value=users[index][asdf][0][i]
                                    )
                            embed.add_field(
                                name="score",
                                value=users[index][asdf][1]["score"],
                                inline=False,
                            )
                            await channel.send(embed=embed)
                        endFlag = True
                        break

                    elif team.content == "종료":
                        del users[index]
                        del user_dice[index]
                        return await channel.send("게임이 종료 됬느니라....")

                    else:
                        msg = list(reversed(team.content.split(",")))
                        if "0" in msg:
                            break
                        for i in msg:
                            try:
                                if int(i) > 5:
                                    break
                            except:
                                break
                            try:
                                user_dice[index][i] = user_dice[index][i]
                                user_dice[index] = rename(
                                    user_dice[index], i, int(i)
                                )
                            except:
                                user_dice[index] = rename(
                                    user_dice[index], int(i), i
                                )
                        continue

        if check_score(users[index]):
            del users[index]
            del user_dice[index]
            await channel.send("게임이 모두 마쳐졌느니라!")
            if len(users[index]) == 2:
                await channel.send(user[check_winner(users[index])])


async def checkcoin():
    await asyncio.sleep(0.01)
    now = datetime.datetime.now()
    t = datetime.time(now.hour, now.minute, now.second)
    recentTimeStamp = (t.hour * 60 + t.minute) * 60 + t.second
    timeToWait = 3600 - (recentTimeStamp % 3600)
    while True:
        await asyncio.sleep(timeToWait)
        dogechannel = client.get_channel("원하는 채팅방 ID")
        try:
            won, percent = doge.get_api_json()
            await dogechannel.send(
                "지금 도지는 {}원이고 전날 대비 {:.2f}퍼센트 이니라".format(won, percent)
            )
        except:
            await dogechannel.send("정보를 불러올 수 없느니라....")
        timeToWait = 3600

client.run(token)
