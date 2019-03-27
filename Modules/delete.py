#-*-coding: UTF-8-*-
def delete(num):
    f = open('post.txt', 'r')
    text = f.readlines()
    f.close()
    f = open('post.txt', 'w')
    for i in range(0, len(text)):
        if text[i].startswith(str(num)):
            continue
        f.write(str(text[i]))
    f.close()