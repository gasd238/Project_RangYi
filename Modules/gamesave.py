import json

def save():
    with open('Data/game_save.json', 'r', encoding='utf-8') as game_save:
        data = game_save.read()
    data = json.loads(data)