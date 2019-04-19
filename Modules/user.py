import json
import math


def levelIncrease(user, message):
    userid = user.id
    isLevelup = False
    with open('Data/userdata.json', 'r', encoding='utf-8') as userdata:
        data = userdata.read()
    data = json.loads(data)
    if str(userid) not in data['users']:
        data['users'][str(userid)] = {
            "level": 1,
            "currentxp": 0,
            "targetxp": LevelExpGetter(2)
        }
    data['users'][str(userid)]['currentxp'] += len(message) // 4 + 1
    while data['users'][str(userid)]['currentxp'] > data['users'][str(userid)]['targetxp']:
        data['users'][str(userid)]['level'] += 1
        data['users'][str(userid)]['targetxp'] += LevelExpGetter(data['users'][str(userid)]['level'])
        isLevelup = True
    with open('Data/userdata.json', 'w', encoding='utf-8') as userdata:
        json.dump(data, userdata, ensure_ascii=False, indent="\t")
    return isLevelup


def showLevel(user, isLevelUp=False):
    userid = user.id
    with open('Data/userdata.json', 'r', encoding='utf-8') as userdata:
        data = userdata.read()
    data = json.loads(data)
    if isLevelUp:
        strings = ":fireworks: **{}**가 **{} 레벨**이 되었느니라!!.\n다음 레벨까지 **{} XP** 남았느니라~~".format(user.name, data['users'][str(userid)]['level'],
                                                                data['users'][str(userid)]['targetxp'] -
                                                                data['users'][str(userid)]['currentxp'])
    else:
        strings = "**{}**는 **{} 레벨**이니라~\n다음 레벨까지 **{} XP** 남았느니라~~".format(user.name, data['users'][str(userid)]['level'],
                                                                data['users'][str(userid)]['targetxp'] -
                                                                data['users'][str(userid)]['currentxp'])
    return strings


def LevelExpGetter(currentLevel):
    nextLevel = currentLevel ** 2
    nextLevel //= math.log2(nextLevel) / 2
    return int((currentLevel + 100) * math.sqrt(currentLevel))
