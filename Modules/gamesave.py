import json

def save(ulev, ufav, uid):
    #json 파일을 불러와 저장되있는 단계(level), 호감도(Favorability)를 변경
    with open('Data/game_save.json', 'r', encoding='utf-8') as game_save:
        data = game_save.read()
    data = json.loads(data)
    try:
        data['played_users'][str(uid)]['level'] = ulev
        data['played_users'][str(uid)]['Favorability'] = ufav
    except:
        pass
    with open('Data/game_save.json', 'w', encoding='utf-8') as game_save:
            json.dump(data, game_save, ensure_ascii=False, indent="\t")


def load(uid):
    with open('Data/game_save.json', 'r', encoding='utf-8') as game_save:
        data = game_save.read()
    data = json.loads(data)
    try:
        lev = data['played_users'][str(uid)]['level']
        fav = data['played_users'][str(uid)]['Favorability']
        return lev, fav
    except:
        data['played_users'][str(uid)]={
            "level" : 1,
            "Favorability" : 50
        }
        with open('Data/game_save.json', 'w', encoding='utf-8') as game_save:
            json.dump(data, game_save, ensure_ascii=False, indent="\t")
        return 1, 50
