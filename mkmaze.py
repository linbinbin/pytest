#!/usr/bin/env python
import sys
import random
from queue import Queue

class Node:
    """Node info class"""
    def __init__(self, y, x, val):
        self.x = x
        self.y = y
        self.val = val
        self.trace = False
        
def get_dir_dis():
    return random.randint(0, 3), random.randint(0, 1)*2, random.randint(0,5)

def readmap(filename, matrix, path):
    with open(filename, 'r') as f:
        for row, line in enumerate(f.readlines()):
            r = []
            for col, w in enumerate(line):
                node = Node(row, col, w)
                r.append(node)
                if w == 's':
                    path.append(node)
                    print('add ', node.x, node.y)
            matrix.append(r)

def mkmeiro(matrix, path):
    current = path[0]
    mv, dis, p = get_dir_dis()
    counter = 0
    t = 0
    w = 0
    v = 0
    directions = [(-1, 0),(0, 1),(1, 0),(0, -1)]
    while True:
        # check erea
        if current.x+directions[mv][0]*2 > 0 and  current.x+directions[mv][0]*2 < len(matrix[0])-2 and current.y+directions[mv][1]*2 > 0 and  current.y+directions[mv][1]*2 < len(matrix)-1:
                if matrix[current.y+directions[mv][1]*2][current.x+directions[mv][0]*2].val == 't':
                    matrix[current.y+directions[mv][1]][current.x+directions[mv][0]].val = ' '
                    t = 1
                elif matrix[current.y+directions[mv][1]*2][current.x+directions[mv][0]*2].val == 'w':
                    matrix[current.y+directions[mv][1]][current.x+directions[mv][0]].val = ' '
                    w = 1
                elif matrix[current.y+directions[mv][1]*2][current.x+directions[mv][0]*2].val == 'v':
                    matrix[current.y+directions[mv][1]][current.x+directions[mv][0]].val = ' '
                    v = 1
                elif matrix[current.y+directions[mv][1]*2][current.x+directions[mv][0]*2].val != '*':
                    current = path[random.randint(0, len(path)-1)]
                    mv, dis, p = get_dir_dis()
                    #print('2')
                else:
                    matrix[current.y+directions[mv][1]][current.x+directions[mv][0]].val = 'p' if p>3 else ' '
                    matrix[current.y+directions[mv][1]*2][current.x+directions[mv][0]*2].val = 'p' if p>2 else ' '
                    current = matrix[current.y+directions[mv][1]*2][current.x+directions[mv][0]*2]
                    path.append(current)
                    counter += 1
                    mv, dis, p = get_dir_dis()
                    #print('3')
                if t and w and v:                  
                    break
                else:
                    mv, dis, p = get_dir_dis()
        else:
            if len(path)>2:
                current = path[random.randint(1, len(path)-1)]
            mv, dis, p = get_dir_dis()            
                            
    enstr = ""
    for line in matrix:
        for w in line:
            enstr += w.val
    print(enstr)
    print(counter)
  
if __name__ == '__main__':
    mat = []
    meiro = []
    readmap("map.txt", mat, meiro)
    mkmeiro(mat, meiro)




