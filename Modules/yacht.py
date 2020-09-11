from random import randint

dice = {1: 1, 2:1, 3: 1, 4: 1, 5: 1}
enum = {1:'ace', 2:'Deuces', 3:'Threes', 4:'Fours', 5:'Fives', 6:'Sixes'}
numline = {1:0, 2:0, 3:0, 4:0,5:0, 6:0, 'score':0}
scoreboard = {'ace':False, 'Deuces':False, 'Threes':False, 'Fours':False, 'Fives':False, 'Sixes':False, 'Bonus':False, 'Choice':False, '4 of a Kind':False, 'Full House':False, 'Small Straight':False, 'Large Straight':False, 'Yacht':False}
users = {}
user_dice = {}

def game_start(users, user):
    index = len(users.keys())+1
    if len(user) == 2:
        users[index] = [[scoreboard, numline], [scoreboard, numline]]
    elif len(user) == 1:
        users[index] = [[scoreboard, numline]]
    user_dice[index] = dice
    return users, user_dice, index

def roll_dice(dice):
    for i in dice.keys():
        if type(i) == str:
            continue
        else:
            dice[i] = int(randint(1, 6))
    return dice

def plus_all(dice):
    sum = 0
    for i in dice.values():
        sum+=i
    return sum

def homework(numline):
    sum = 0
    for i in numline.keys():
        if i == 'score':
            continue
        else:
            sum+=numline[i]
    if sum > 63:
        return True
    else:
        return False

def check_yacht(num):
    if 5 in num.values():
        return True
    else:
        return False

def check_numpart(num):
    board = {'ace':False, 'Deuces':False, 'Threes':False, 'Fours':False, 'Fives':False, 'Sixes':False, 'Bonus':False}
    for i in num.keys():
        if num[i] >0:
            board[enum[i]] = True
    return board

def check_straight(num):
    chk = 0
    for i in num.values():
        if i > 0:
            chk+=1
        elif i == 0 and chk == 0:
            continue
        else:
            break
    return chk

def check_full_house(num):
    if 3 in num.values() and 2 in num.values():
        return True
    else:
        return False

def check_four_cards(num):
    for i in num.values():
        if i>3:
            return True
    return False

def mod_scoreboard(board, scoreboard):
    for i in board.keys():
        if board[i] == True:
            scoreboard[i] = True
    return scoreboard

def get_num(dice):
    num = {1:0, 2:0, 3:0, 4:0,5:0, 6:0}
    for i in dice.values():
        for j in num.keys():
            if i == j:
                num[j] +=1
    return num

def dice_check(dice):
    scoreboard = {'ace':False, 'Deuces':False, 'Threes':False, 'Fours':False, 'Fives':False, 'Sixes':False, 'Bonus':False, 'Choice':True, '4 of a Kind':False, 'Full House':False, 'Small Straight':False, 'Large Straight':False, 'Yacht':False}
    
    num = get_num(dice)

    if check_yacht(num):
        scoreboard['Yacht'] = 50
    else:
        scoreboard['Yacht'] = 0
    
    if check_full_house(num):
        scoreboard['Full House'] = True
    else:
        scoreboard['Full House'] = 0


    if check_four_cards(num):
        scoreboard['4 of a Kind'] = True
    else:
        scoreboard['4 of a Kind'] = 0

    scoreboard = mod_scoreboard(check_numpart(num), scoreboard)

    if check_straight(num) == 5:
        scoreboard['Large Straight'] = True
    else:
        scoreboard['Large Straight'] = 0

    if check_straight(num) > 3:
        scoreboard['Small Straight'] = True 
    else:
        scoreboard['Small Straight'] = 0 

    return scoreboard

def check_score(scoreboards):
    for i in scoreboards:
        for j in i[0].keys():
            if i[0][j] == False:
                return False
    return True

def check_winner(users):
    if users[0][1]['score'] > users[1][1]['score']:
        return 0
    else:
        return 1

             