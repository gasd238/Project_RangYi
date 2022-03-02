from random import randint

dice = {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}
enum = {1: "ace", 2: "Deuces", 3: "Threes", 4: "Fours", 5: "Fives", 6: "Sixes"}
users = {}
user_dice = {}
board = {}


def game_start(users, user):
    index = len(users.keys()) + 1
    if len(user) == 2:
        users[index] = [
            [
                {
                    "ace": False,
                    "Deuces": False,
                    "Threes": False,
                    "Fours": False,
                    "Fives": False,
                    "Sixes": False,
                    "Bonus": False,
                    "Choice": False,
                    "4 of a Kind": False,
                    "Full House": False,
                    "Small Straight": False,
                    "Large Straight": False,
                    "Yacht": False,
                },
                {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, "score": 0},
            ],
            [
                {
                    "ace": False,
                    "Deuces": False,
                    "Threes": False,
                    "Fours": False,
                    "Fives": False,
                    "Sixes": False,
                    "Bonus": False,
                    "Choice": False,
                    "4 of a Kind": False,
                    "Full House": False,
                    "Small Straight": False,
                    "Large Straight": False,
                    "Yacht": False,
                },
                {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, "score": 0},
            ],
        ]
    elif len(user) == 1:
        users[index] = [
            [
                {
                    "ace": False,
                    "Deuces": False,
                    "Threes": False,
                    "Fours": False,
                    "Fives": False,
                    "Sixes": False,
                    "Bonus": False,
                    "Choice": False,
                    "4 of a Kind": False,
                    "Full House": False,
                    "Small Straight": False,
                    "Large Straight": False,
                    "Yacht": False,
                },
                {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, "score": 0},
            ]
        ]
    user_dice[index] = dice
    return users, user_dice, index


def roll_dice(dice):
    for i in dice.keys():
        if type(i) == str:
            continue
        else:
            for _ in range(int(randint(1, 6))):
                dice[i] = int(randint(1, 6))
    return dice


def plus_all(dice):
    sum = 0
    for i in dice.values():
        sum += i
    return sum


def homework(userboard):
    sum = 0
    for i in userboard.keys():
        if i == "score":
            continue
        else:
            sum += userboard[i]
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
    for i in num.keys():
        if num[i] > 0:
            board[enum[i]] = True
    return board


def check_straight(num):
    chk = 0
    for i in num.values():
        if i > 0:
            chk += 1
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
        if i > 3:
            return True
    return False


def mod_board(numpart, board):
    chkboard = {
        "ace": False,
        "Deuces": False,
        "Threes": False,
        "Fours": False,
        "Fives": False,
        "Sixes": False,
        "Bonus": False,
    }
    for i in numpart.keys():
        if numpart[i] == True:
            board[i] = True
    return board


def get_num(dice):
    num = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
    for i in dice.values():
        for j in num.keys():
            if i == j:
                num[j] += 1
    return num


def dice_check(dice):
    board = {
        "ace": False,
        "Deuces": False,
        "Threes": False,
        "Fours": False,
        "Fives": False,
        "Sixes": False,
        "Bonus": False,
        "Choice": False,
        "4 of a Kind": False,
        "Full House": False,
        "Small Straight": False,
        "Large Straight": False,
        "Yacht": False,
    }
    num = get_num(dice)

    board = mod_board(check_numpart(num), board)

    if check_yacht(num):
        board["Yacht"] = 50
    else:
        board["Yacht"] = 0

    if check_full_house(num):
        board["Full House"] = True
    else:
        board["Full House"] = 0

    if check_four_cards(num):
        board["4 of a Kind"] = True
    else:
        board["4 of a Kind"] = 0

    if check_straight(num) == 5:
        board["Large Straight"] = True
    else:
        board["Large Straight"] = 0

    if check_straight(num) > 3:
        board["Small Straight"] = True
    else:
        board["Small Straight"] = 0

    return board


def check_score(boards):
    for i in boards:
        for j in i[0].keys():
            if i[0][j] == False:
                return False
    return True


def check_winner(users):
    if users[0][1]["score"] > users[1][1]["score"]:
        return 0
    else:
        return 1
