import json
class Save:
    def save(self, ulev, uid, favper, choice):
        #json 파일을 불러와 저장되있는 단계(level), 호감도(Favorability), 선택지 대비(choice)를 변경
        with open('Data/game_save.json', 'r', encoding='utf-8') as game_save:
            data = game_save.read()
        data = json.loads(data)
        try:
            data["played_users"][str(uid)]["favper"] = int(favper)
            data["played_users"][str(uid)]["level"] = int(ulev)
            data["played_users"][str(uid)]["choice"] = int(choice)
            data["played_users"][str(uid)]["save_at_choice"] = int(save_at_choice)
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
            favper = data["played_users"][str(uid)]["favper"]
            lev = data["played_users"][str(uid)]["level"]
            choice = data["played_users"][str(uid)]["choice"]
            save_at_choice = data["played_users"][str(uid)]["save_at_choice"]
            return favper, lev, choice, save_at_choice
        except:
            data["played_users"][str(uid)]={
                "favper" : 50,
                "level" : 0,
                "choice" : 0,
                "save_at_choice" : 0
            }
            with open('Data/game_save.json', 'w', encoding='utf-8') as game_save:
                json.dump(data, game_save, ensure_ascii=False, indent="\t")
            return 50, 0, 0, 0
            
