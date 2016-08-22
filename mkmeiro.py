# coding: utf-8
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
    return random.randint(0, 3), random.randint(2, 7)

def readmap(filename, matrix, path):
    with open(filename, 'r') as f:
        for row, line in enumerate(f.readlines()):
            r = []
            for col, w in enumerate(line):
                node = Node(row, col, w)
                r.append(node)
                if w == ' ':
                    path.append(node)
            matrix.append(r)

def mkmeiro(matrix, path):
    current = path[0]
    mv, dis = get_dir_dis()
    counter = 1
    while current.val == 'E' or matrix[current.y+1][current.x].val != 'E':
        if mv == 0 and current.x-1>0 and matrix[current.y-1][current.x-1].val != ' ' and matrix[current.y+1][current.x-1].val != ' ' and matrix[current.y][current.x-2].val != ' ':
            if matrix[current.y][current.x-1].val != ' ':
                path.append(matrix[current.y][current.x-1])
                matrix[current.y][current.x-1].val = ' '
            current = matrix[current.y][current.x-1]
            counter += 1
        elif mv == 1 and current.y+1<len(matrix)-1 and matrix[current.y+1][current.x-1].val != ' ' and matrix[current.y+1][current.x+1].val != ' ' and matrix[current.y+2][current.x].val != ' ':
            if matrix[current.y+1][current.x].val != ' ':
                path.append(matrix[current.y+1][current.x])            
                matrix[current.y+1][current.x].val = ' '
            current = matrix[current.y+1][current.x]
            counter += 1
        elif mv == 2 and current.x+1<len(matrix[0])-2 and matrix[current.y-1][current.x+1].val != ' ' and matrix[current.y+1][current.x+1].val != ' ' and matrix[current.y][current.x+2].val != ' ':
            if matrix[current.y][current.x+1].val != ' ':
                path.append(matrix[current.y][current.x+1])
                matrix[current.y][current.x+1].val = ' '
            current = matrix[current.y][current.x+1] 
            counter += 1
        elif mv == 3 and current.y-1>0 and matrix[current.y-1][current.x-1].val != ' ' and matrix[current.y-1][current.x+1].val != ' ' and matrix[current.y-2][current.x].val != ' ':
            if matrix[current.y-1][current.x].val != ' ':
                path.append(matrix[current.y-1][current.x])
                matrix[current.y-1][current.x].val = ' '
            current = matrix[current.y-1][current.x]  
            counter += 1
        else:
            current = path[random.randint(0, len(path)-1)]
        if counter % dis == 0: 
            mv, dis = get_dir_dis()
            #print("conuter:{0} random.{1}".format(counter, mv))
        
    enstr = ""
    for line in matrix:
        for w in line:
            enstr += w.val
    print(enstr)
  
if __name__ == '__main__':
    mat = []
    meiro = []
    readmap("map.txt", mat, meiro)
    mkmeiro(mat, meiro)

