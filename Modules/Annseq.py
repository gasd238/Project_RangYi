from random import randint

def rand():
    sequence = ''
    man = ['재홍', '정현', '호승', '상현', '서빈', '영빈', '종효', '선우', '현주']
    num = ['1','2','3','4','5','6','7','8','9']
    for j in range(0, 9):
        if j % 2 == 1:
            sequence = sequence + num[j] +' '+ man.pop(int(randint(0, len(man)-1))) + '\n'
        else:
            sequence = sequence + num[j] +' '+ man.pop(int(randint(0, len(man)-1))) + ' '
    return sequence


