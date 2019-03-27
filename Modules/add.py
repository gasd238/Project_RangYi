#-*-coding: UTF-8-*-
def add(list):
    f = open('post.txt', 'a')
    lines = ''
    for i in range(0, len(list)): 
        lines = lines + list[i] + ' '
    f.write(lines+'\n')
    f.close()