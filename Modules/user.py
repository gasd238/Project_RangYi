import pymongo
import json
import math

from Modules.setting import *  # Import Settings

client = pymongo.MongoClient(database)
db = client.rangyibot
collection = db.user


class UserLevel:
    def levelIncrease(self, user, message):
        userid = user.id
        isLevelup = False
        result = collection.find_one({"userid": user.id})
        if not result:
            result = {
                "userid": user.id,
                "level": 1,
                "currentxp": 0
            }
            collection.insert_one(result)
        result['currentxp'] += len(message) // 4 + 1
        targetExp = self.LevelExpGetter(result['level'])

        while result['currentxp'] > targetExp:
            result['level'] += 1
            isLevelup = True
        collection.update_one({"userid": userid}, {"$set": result})
        return isLevelup

    def showLevel(self, user, isLevelUp=False):
        result = collection.find_one({"userid": user.id})
        if isLevelUp:
            strings = ":fireworks: **{}**가 **{} 레벨**이 되었느니라!!.\n다음 레벨까지 **{} XP** 남았느니라~~".format(user.name,
                                                                                                  result['level'],
                                                                                                  self.LevelExpGetter(
                                                                                                      result['level']) -
                                                                                                  result['currentxp'])
        else:
            strings = "**{}**는 **{} 레벨**이니라~\n다음 레벨까지 **{} XP** 남았느니라~~".format(user.name, result['level'],
                                                                                self.LevelExpGetter(result['level']) -
                                                                                result['currentxp'])
        return strings

    def showRanking(self, server):
        members = [str(x.id) for x in list(server.members)]
        output = collection.find({"userid": {"$in": members}}).sort('currentxp', pymongo.DESCENDING)
        return output

    def LevelExpGetter(self, currentLevel):
        currentLevel += 1
        nextLevel = currentLevel ** 2
        nextLevel //= math.log2(nextLevel) / 2

        return int((currentLevel + 100) * math.sqrt(currentLevel))
