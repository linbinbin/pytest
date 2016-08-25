#!/usr/bin/env python
#import sys
#import random
#import pprint as pp
from queue import Queue
import networkx as nx
import matplotlib.pyplot as plt
import math

# 迷路をグラフにする：本質的に深さ優先探索
import itertools as it
vs = 0
edges = list()
arr = list()
nodes = dict()
edges_d = dict()
pok = 0 

class Node:
    """Node info class"""
    def __init__(self, y, x, name):
        self.x = x
        self.y = y
        self.name = name
        self.edges = []
        self.dis = 0
class Edge:
    """Edge info class"""
    def __init__(self, start, end, ndis, npok):
        self.start = start
        self.end = end
        self.ndis = ndis
        self.npok = npok
        
def isWall(s):
    return 1 if s == '*' else 0

def getWalls(arr, i, j):
    try:
        return isWall(arr[i+1][j]) + isWall(arr[i-1][j]) + isWall(arr[i][j+1]) + isWall(arr[i][j-1])
    except:
        print(i,j)
        
def getEdge(arr, i, j, edges, v, c, p):
    for (a,b) in zip([1,-1,0,0], [0,0,1,-1]):
        global pok
        cp = p
        if isWall(arr[i+a][j+b]) == 0:
            arr[i+a][j+b] = '*'
            if arr[i+2*a][j+2*b] == 0 or arr[i+2*a][j+2*b] == 'p':
                vn = v
                cn = c + 1
                if arr[i+2*a][j+2*b] == 'p':
                    cp = p - 1
                    pok += 1
            else:
                if type(arr[i+2*a][j+2*b]) != tuple:
                    print(i+2*a, j+2*b, arr[i+2*a][j+2*b])
                if arr[i+a][j+b] == 'p':
                    cp = p - 1
                    pok += 1
                vn = arr[i+2*a][j+2*b][0]
                if arr[i+2*a][j+2*b][1] == 'p':
                    cp = p - 1
                    pok += 1
                edges.append((v, vn, c, cp))
                #edges_d["{0},{1}".format(v,vn)] = (v, vn, c, cp)
                #edge_labels                
                nodes[str(v)].edges.append((v, vn, c, cp))
                nodes[str(vn)].edges.append((v, vn, c, cp))
                cn = 1
                cp = 0
            getEdge(arr, i+2*a, j+2*b, edges, vn, cn, cp)

for line in open('maze.txt', 'r'):
    arr.append(list(line))
height = len(arr)
width = len(arr[height - 1])
if not height % 2:
    arr.append(['*' for x in range(width)])
if not width % 2:
    for i in range(height):
        arr[i].append('*')
cellidj = range(1,width,2)
cellidi = range(1,height,2)
# Make Nodes
for i,j in it.product(cellidi, cellidj):
    if arr[i][j] == 's' or arr[i][j] == 't':
        nodes[arr[i][j]] = Node(i, j, arr[i][j])        
        arr[i][j] = (arr[i][j], arr[i][j])
    elif getWalls(arr, i, j) == 2:
        arr[i][j] = 0 if arr[i][j] == ' ' else 'p'
    else:
        vs += 1
        arr[i][j] = (vs, arr[i][j])
        nodes[str(vs)] = Node(i, j, str(vs))
               
# Set Edge　for graph
getEdge(arr, 21, 1, edges, 1, 1, 0)
edge_labels=dict([((u,v,),(d, p))
             for u,v,d,p in edges])
# Sort the Node's edge by p and d
for key in nodes:
    nodes[key].edges.sort(key=lambda x:(x[3], x[2]))
#    if len(nodes[key].edges)>2:
#        print([list(x) for x in nodes[key].edges])

        
print("Node:{0}, Edge:{1}, Pokemon:{2}".format(vs+1, len(edges), pok))
print([x for x in edges if x[0]=='s' or x[0]=='t' or x[1] == 's' or x[1] == 't'])

rout = Queue()

G = nx.Graph()
srcs, dests = zip(* [(fr, to) for (fr, to, d, p) in edges])
G.add_nodes_from(srcs + dests)

for (s,r,d,p) in edges:
    G.add_edge(s, r, weight=10/math.sqrt(d))

pos = nx.spring_layout(G)

plt.figure(figsize=(100, 80))
nx.draw_networkx(G, pos, with_labels=True, edge_vmin=10)
nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels)

plt.axis('off')
plt.savefig('map.png', dpi=100)
#plt.show()
