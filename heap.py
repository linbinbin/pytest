#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This file for tree and heap"""

buff=[8,1,2,10,3,4,5,9,6,7]

def upheap(buff, n):
    while True:
        p = (n - 1) // 2
        if p < 0 or buff[p] <= buff[n]: break
        temp = buff[n]
        buff[n] = buff[p]
        buff[p] = temp
        n = p
        
def createheap(buff):
    for x in range(1, len(buff)):
        upheap(buff, x)

def downheap(buff, n):
    size = len(buff)
    while True:
        c = 2 * n + 1
        if c >= size: break
        if c + 1 < size:
            if buff[c] > buff[c + 1]: c += 1
        if buff[n] <= buff[c]: break
        temp = buff[n]
        buff[n] = buff[c]
        buff[c] = temp
        n = c
        
createheap(buff)
    
print(buff)

downheap(buff, 5)
print(buff)        