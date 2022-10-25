import numpy as np
import random

from pygame.threads import Thread

numList = np.arange(100000).tolist()
tl = []


def pick():
    cnt = 0
    while len(numList):
        try:
            numList.remove(random.choice(numList))
        except:
            assign = None
        else:
            cnt += 1
    return cnt


def p1():
    x = pick()
    print("p1: ", x)


def p2():
    x = pick()
    print("p2: ", x)


a = Thread(target=p1)
b = Thread(target=p2)
a.start()
b.start()
