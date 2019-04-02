import json
import math


def levelIncrease(userid, message):
    with open('../Data/userdata.json', 'r', encoding='utf-8') as userdata:
        data = userdata.read()
    data = json.loads(data)
    if str(userid) not in data['users']:
        data['users'][str(userid)] = {
            "level": 1,
            "currentxp": 0,
            "targetxp": LevelExpGetter(1)
        }
    data['users'][str(userid)]['currentxp'] += len(message) // 4 + 1
    with open('../Data/userdata.json', 'w', encoding='utf-8') as userdata:
        json.dump(data, userdata, ensure_ascii=False, indent="\t")
    return data


def LevelExpGetter(currentLevel):
    currentLevel += 1
    currentLevel **= 2
    currentLevel //= math.log2(currentLevel) / 2
    return int(currentLevel + 100)
