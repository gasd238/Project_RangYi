from random import randint


class Annseq:
    def rand(self, mlist):
        sequence = ''
        man = [] # 고정적으로 순서를 뽑는 목록이 있다면 넣어주세요.
        if mlist != []:
            man = mlist
        for _ in range(random.randint(0, 21)):
            random.shuffle(man)
        for j in range(len(man)):
            sequence = sequence + str(j+1) +' '+ str(man[j])
            if j % 2 == 1:
                sequence += '\n'
            else:
                sequence += ' '

        return sequence


