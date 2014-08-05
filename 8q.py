# *_utf-8_ *
import os
import math

def putNext(y,pos):
    putflg = 0
    if y==8:
        print "Ping Pong !!!!", pos
        return
    for x in range(0,8):
        hasflg = 0;
        for jugd in pos:
            if x == jugd[0] or y == jugd[1] or math.fabs(x-jugd[0]) == math.fabs(y-jugd[1]):
                hasflg = 1
        if hasflg == 0:
            print "Put the (%d, %d)" %(x, y)
            pos.append((x, y))
            t = y + 1
            print "Next t", 0, t, pos
            putNext(t, pos)
    if y > 1:
#        y -= 1
        pos.pop()
        print "back to ", y, pos


def main():
    print "Start 8 Queens!"
    for i in range(8):
        t = (i, 0)
        pos = [t]
        print "the first pos ", pos
        putNext(1, pos)
    print "End 8 Queens!"


if __name__=='__main__':
    main()
