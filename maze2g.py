#!/usr/bin/env python
#import sys
#import random
#import pprint as pp
import heapq
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
        self.poks = 0
        self.pre = ''
        self.used = 0
        self.next = ''
        self.branch = []
    def __lt__(self, other):
        return self.name < other.name
    def __gt__(self, other):
        return self.name > other.name
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
            if arr[i+a][j+b] == 'p':
                cp = p - 1
                pok += 1
            arr[i+a][j+b] = '*'
            if arr[i+2*a][j+2*b] == 0 or arr[i+2*a][j+2*b] == 'p':
                vn = v
                cn = c + 1
                if arr[i+2*a][j+2*b] == 'p':
                    cp = p - 1
                    pok += 1                    
            else:
                vn = arr[i+2*a][j+2*b][0]
                if arr[i+2*a][j+2*b][1] == 'p':
                    cp = p - 1
                    if len(nodes[str(vn)].edges)==0:                    
                        pok += 1
                edges.append((v, vn, c, cp))
                #edges_d["{0},{1}".format(v,vn)] = (v, vn, c, cp)
                #edge_labels                
                nodes[str(v)].edges.append((v, vn, c, cp))
                nodes[str(vn)].edges.append((v, vn, c, cp))
                cn = 1
                cp = 0
            getEdge(arr, i+2*a, j+2*b, edges, vn, cn, cp)

for line in open('maze2.txt', 'r'):
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
#getEdge(arr, nodes['s'].x, nodes['s'].y, edges, 1, 1, 0)
getEdge(arr, 3, 7, edges, 1, 1, 0)
edge_labels=dict([((u,v),(d, p))
             for u,v,d,p in edges])
# Sort the Node's edge by p and d
for key in nodes:
    nodes[key].edges.sort(key=lambda x:(x[3], x[2]))
#    if len(nodes[key].edges)>2:
#        print([list(x) for x in nodes[key].edges])

print([x for x in edges])
print([(node[1].name, node[1].x, node[1].y) for node in nodes.items()])        
print("Node:{0}, Edge:{1}, Pokemon:{2}".format(vs+1, len(edges), pok))
#print([x for x in edges if x[0]=='s' or x[0]=='t' or x[1] == 's' or x[1] == 't'])

# ダイクストラ法でｓ->t,Pの最小ルートを探索（Pは負）
#rout = heapq()
rout = list()
outs = list()
pathes = dict()
nodes['s'].used = 1
for edge in nodes['s'].edges:
    nn = edge[0] if str(edge[0]) != 's' else edge[1]
    vn = nodes[str(nn)]
    vn.dis, vn.poks, vn.pre = edge[2], edge[3], 's'
    heapq.heappush(rout, ((vn.poks, vn.dis),vn))
while len(rout)>0:
    v = heapq.heappop(rout)[1]
    v.used = 1
    #print(len(rout))
    for edge in v.edges:
        nn = edge[0] if str(edge[0]) != v.name else edge[1]
        vn = nodes[str(nn)]
        if vn.used == 0:
            if vn.dis == 0:
                vn.poks = v.poks + edge[3]
                vn.dis = v.dis + edge[2]
                vn.pre = v.name
            else:
                if vn.poks > v.poks + edge[3]:
                    vn.poks = v.poks + edge[3]
                    vn.pre = v.name            
                elif vn.poks == v.poks + edge[3] and vn.dis > v.dis + edge[2]:
                    vn.dis = v.dis + edge[2]
                    vn.pre = v.name
            heapq.heappush(rout, ((vn.poks, vn.dis),vn))

G = nx.Graph()
srcs, dests = zip(* [(fr, to) for (fr, to, d, p) in edges])
G.add_nodes_from(srcs + dests)

for (s,r,d,p) in edges:
    G.add_edge(s, r, weight=10/math.sqrt(d))

pos = nx.spring_layout(G)

plt.figure(figsize=(10, 8))
nx.draw_networkx(G, pos, with_labels=True, edge_vmin=10)
nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels)

plt.axis('off')
plt.savefig('map.png', dpi=100)
#plt.show()

edgess=dict([((str(u),str(v)),(d, p))
             for u,v,d,p in edges])
rp = ""
v = nodes['t']
d = v.dis
p = 0
while v.pre != '':
    rp += "{0}({1},{2}) <- ".format(v.name, v.x+1, v.y+1)            
    vp = nodes[v.pre]
    vp.next = v.name
    if (v.name, vp.name) in edgess:
        p += edgess[(v.name, vp.name)][1]
        del edgess[(v.name, vp.name)]
    else:
        p += edgess[(vp.name, v.name)][1]
        del edgess[(vp.name, v.name)]
    v = vp
rp += "{0}({1},{2}) d:{3} p:{4}".format(v.name, v.x+1, v.y+1, d, -p)
print(rp)

# 残りのPを持つEdgeを探索
#　最小ルート点と直接,最小ルート点からのルート追加
out = dict()


#　共通点ないEdge、tからダイクストラ法で最短ルートを探索
#　既存ルートと共通点がある場合、共通点へのルート追加