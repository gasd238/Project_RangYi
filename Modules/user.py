import pymongo
import json
import math
import random
import datetime
import discord
import certifi

from Modules.setting import *  # Import Settings

client = pymongo.MongoClient(database, tlsCAFile=certifi.where())
db = client.rangyibot
collection = db.user
bancol = db.ban

class Ban:
    def banUser(self, user):
        userid = user.id
        result = bancol.find_one({"userid": user.id})
        if not result:
            result = {"userid": user.id, "time": datetime.datetime.now()}
            bancol.insert_one(result)
            return "밴 됨"
        return "이미 밴 됨"


class UserLevel:
    def levelIncrease(self, user, message):
        userid = user.id
        isLevelup = False
        result = collection.find_one({"userid": user.id})
        if not result:
            result = {
                "userid": user.id,
                "level": 1,
                "currentxp": random.randint(3, 15),
                "time": datetime.datetime.now(),
            }
            collection.insert_one(result)
        update_time = datetime.datetime.now()
        if (update_time - result["time"]).seconds / 60 > 2:
            result["currentxp"] += random.randint(3, 15)
            result["time"] = update_time
            targetExp = self.LevelExpGetter(result["level"])

            while result["currentxp"] > targetExp:
                result["level"] += 1
                targetExp = self.LevelExpGetter(result["level"])
                isLevelup = True
            collection.update_one({"userid": userid}, {"$set": result})
            return isLevelup

    def showLevel(self, user, profileurl, isLevelUp=False):
        result = collection.find_one({"userid": user.id})
        if isLevelUp:
            embed = discord.Embed(
                title=":fireworks: 레벨 업!!",
                description="**{}가 {} 레벨**이 되었느니라!!\n다음 레벨까지 **{} XP** 남았느니라~~".format(
                    user.name,
                    result["level"],
                    self.LevelExpGetter(result["level"]) - result["currentxp"],
                ),
            )
            embed.set_thumbnail(url=profileurl)
        else:
            embed = discord.Embed(
                title="{}의 레벨이니라!".format(user.name),
                description="**현재{} 레벨**이니라!!\n다음 레벨까지 **{} XP** 남았느니라~~".format(
                    result["level"],
                    self.LevelExpGetter(result["level"]) - result["currentxp"],
                ),
            )
            embed.set_thumbnail(url=profileurl)
        return embed

    def showRanking(self, server):
        members = [x.id for x in server.members]
        output = collection.find({"userid": {"$in": members}}).sort('currentxp', pymongo.DESCENDING)
        return list(output)

    def LevelExpGetter(self, currentLevel):
        currentLevel += 1
        nextLevel = currentLevel**4
        nextLevel //= math.log2(nextLevel) / 2

        return int((nextLevel + 100) * math.sqrt(nextLevel))
