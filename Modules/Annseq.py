from random import randint


class Annseq:
    def rand(self):
        sequence = ''
        man = ['재홍', '정현', '호승', '상현', '서빈', '영빈', '종효', '선우', '현주']
        for j in range(len(man)):
            if j % 2 == 1:
                sequence = sequence + str(j+1) +' '+ man.pop(int(randint(0, len(man)-1))) + '\n'
            else:
                sequence = sequence + str(j+1) +' '+ man.pop(int(randint(0, len(man)-1))) + ' '
        return sequence

    def rand_self(self, mlist):
        sequence = ''
        for j in range(len(mlist)):
            if j % 2 == 1:
                sequence = sequence + str(j+1) +' '+ mlist.pop(int(randint(0, len(mlist)-1))) + '\n'
            else:
                sequence = sequence + str(j+1) +' '+ mlist.pop(int(randint(0, len(mlist)-1))) + ' '
        return sequence


