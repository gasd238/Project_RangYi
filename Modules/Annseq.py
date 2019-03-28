from random import randint

def rand():
    sequence = ''
    man = ['재홍', '정현', '호승', '상현', '서빈', '영빈', '종효', '선우', '현주']
    num = ['1','2','3','4','5','6','7','8','9']
    for j in range(9):
        sequence = sequence + man[j] +' '+ num.pop(int(randint(0, len(num)-1))) + '\n'
    return sequence


