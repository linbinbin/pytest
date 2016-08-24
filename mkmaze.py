
# coding: utf-8

# In[ ]:


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
    return random.randint(0, 3), random.randint(0, 1)*2

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
    mv, dis = get_dir_dis()
    counter = 1
    directions = [(-1, 0),(0, 1),(1, 0),(0, -1)]
    while True:
        # check erea
        if current.x+directions[mv][0]*2 > 0 and  current.x+directions[mv][0]*2 < len(matrix[0])-1            and current.y+directions[mv][1]*2 > 0 and  current.y+directions[mv][1]*2 < len(matrix)-1:
                if matrix[current.y+directions[mv][1]*2][current.x+directions[mv][0]*2].val == 't':
                    matrix[current.y+directions[mv][1]][current.x+directions[mv][0]].val = ' '
                    break
                elif matrix[current.y+directions[mv][1]*2][current.x+directions[mv][0]*2].val != '*':
                    current = path[random.randint(0, len(path)-1)]
                    mv, dis = get_dir_dis()
                else:
                    matrix[current.y+directions[mv][1]][current.x+directions[mv][0]].val = ' '
                    matrix[current.y+directions[mv][1]*2][current.x+directions[mv][0]*2].val = ' '
                    current = matrix[current.y+directions[mv][1]*2][current.x+directions[mv][0]*2]
                    path.append(current)
                    counter += 1
                    mv, dis = get_dir_dis()
        else:
            current = path[random.randint(0, len(path)-1)]
            mv, dis = get_dir_dis()
                            
    enstr = ""
    for line in matrix:
        for w in line:
            enstr += w.val
    print(enstr)
  
if __name__ == '__main__':
    mat = []
    meiro = []
    readmap("map_b.txt", mat, meiro)
    mkmeiro(mat, meiro)


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



