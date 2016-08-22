# coding: utf-8
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
        
def readmap(filename, matrix, start, end):
    with open(filename, 'r') as f:
        for row, line in enumerate(f.readlines()):
            r = []
            for col, w in enumerate(line):
                if w == ' ' or w == '*' or w == 's' or w == 'E' or w == 'P':
                    node = Node(row, col, w)
                    r.append(node)
                    if w == 's':
                        start.append(col)
                        start.append(row)
                        print("start:", start)
                    elif w == 'E':
                        end.append(col)
                        end.append(row)
                        print("end:", end)
            matrix.append(r)
            
def iswhite(node):
        return node.val != '*' and (not node.trace)
    
def getadjacent(n):
    x,y = n
    return [(x-1,y),(x,y-1),(x+1,y),(x,y+1)]
            
def bfs(start, end, matrix):
    queue = Queue()
    queue.put([start]) # Wrapping the start tuple in a list
    v = len(matrix[0])
    w = len(matrix)

    while not queue.empty():
        path = queue.get()
        pixel = path[-1]

        if pixel[0] == end[0] and pixel[1] == end[1]:
            return path
        try:
            for adjacent in getadjacent(pixel):
                x,y = adjacent
                if x > 0 and x <v and y > 0 and y < w:
                    if iswhite(matrix[y][x]):
                        #print("({0}, {1})is white".format(x, y))
                        matrix[y][x].trace = True # see note
                        new_path = list(path)
                        new_path.append(adjacent)
                        queue.put(new_path)
        except Exception as error:
            print("BFS err at (%d, %d)" % (x, y))

    print("Queue has been exhausted. No answer was found.")
            
if __name__ == '__main__':
    start = []
    end = []    
    mat = []
    
    readmap("meiro.txt", mat, start, end)
    path = bfs(start, end , mat)
    print(path)
    
    for x, y in path:
        if mat[y][x].val == ' ':
            mat[y][x].val = '+'
            
    enstr = ""
    for line in mat:
        for w in line:
            enstr += w.val
        enstr += '\n'
    print(enstr)    

