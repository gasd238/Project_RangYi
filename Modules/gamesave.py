import json
class Save:
    def save(self, ulev, uid, uname):
        #json 파일을 불러와 저장되있는 단계(level), 호감도(Favorability)를 변경
        with open('Data/game_save.json', 'r', encoding='utf-8') as game_save:
            data = game_save.read()
        data = json.loads(data)
        try:
            data["played_users"][str(uid)]["name"] = str(uname)
            data["played_users"][str(uid)]["level"] = int(ulev)
            with open('Data/game_save.json', 'w', encoding='utf-8') as game_save:
                json.dump(data, game_save, ensure_ascii=False, indent="\t")
            return "저장 완료"
        except:
            return "저장 실패"
        


    def load(self, uid):
        with open('Data/game_save.json', 'r', encoding='utf-8') as game_save:
            data = game_save.read()
        data = json.loads(data)
        try:
            name = data["played_users"][str(uid)]["name"]
            lev = data["played_users"][str(uid)]["level"]
            return name, lev
        except:
            data["played_users"][str(uid)]={
                "name" : 'Null',
                "level" : 1
            }
            with open('Data/game_save.json', 'w', encoding='utf-8') as game_save:
                json.dump(data, game_save, ensure_ascii=False, indent="\t")
            return 'Null', 1
            
