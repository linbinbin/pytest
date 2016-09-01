#!/usr/bin/env python
#import sys
#import random
#import pprint as pp
import heapq
import networkx as nx
import matplotlib.pyplot as plt
import math
import itertools as it
import csv

edges = list()
arr = list()
vertices = dict()
edges_d = dict()
pok = 0 

class Vertice:
    """vertice info class"""
    def __init__(self, x, y, name, p):
        self.x = x
        self.y = y
        self.name = name
        self.edges = []
        self.dis = 0
        self.poks = 0
        self.pre = ''
        self.used = 0 #1,2
        self.next = ''
        self.branch = []
        self.pok = p
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
        
def getEdge(arr, i, j, edges, v, c, p, lr):
    for (a,b) in zip([1,-1,0,0], [0,0,1,-1]):
        global pok
        cp = p
        rn = list(lr)
        if isWall(arr[i+a][j+b]) == 0:
            if arr[i+a][j+b] == 'P':
                cp -= 1
                pok += 1
            arr[i+a][j+b] = '*'
            if arr[i+2*a][j+2*b] == 0 or arr[i+2*a][j+2*b] == 'P':
                vn = v
                cn = c + 1
                if arr[i+2*a][j+2*b] == 'P':
                    cp -= 1
                    pok += 1
                rn.append((i+a, j+b))
                rn.append((i+a*2, j+b*2))                                   
            else:
                rn.append((i+a, j+b))           
                vn = arr[i+2*a][j+2*b][0]
                if arr[i+2*a][j+2*b][1] == 'P':
                    if len(vertices[str(vn)].edges)==0:                    
                        pok += 1
                rrn = list(rn)
                rrn.reverse()
                edges.append((str(v), str(vn), c, cp, rn))
                edges.append((str(vn), str(v), c, cp, rrn))               
                vertices[str(v)].edges.append((str(v), str(vn), c, cp))
                vertices[str(vn)].edges.append((str(vn), str(v), c, cp))
                cn = 1
                cp = 0
                rn = list()
            getEdge(arr, i+2*a, j+2*b, edges, vn, cn, cp, rn)
    del lr

def read_maze(file_name, arr, vertices):
    vs = 0
    for line in open(file_name, 'r'):
        arr.append(list(line))
    height = len(arr)
    width = len(arr[height - 1])
    cellidi = range(1,height,2)
    cellidj = range(1,width,2)
    # Make vertices
    for i,j in it.product(cellidi, cellidj):
        try:
            if arr[i][j] == '*':
                continue
            if arr[i][j] == 'S' or arr[i][j] == 'G':
                vertices[arr[i][j]] = Vertice(i, j, arr[i][j], arr[i][j])        
                arr[i][j] = (arr[i][j], arr[i][j])
            elif arr[i][j] == 'P':
                vs += 1
                val = arr[i][j]
                arr[i][j] = (vs, arr[i][j])
                vertices[str(vs)] = Vertice(i, j, str(vs), val)
                print('p', str(vs), i, j)
            elif getWalls(arr, i, j) == 2 and arr[i][j] == ' ':
                arr[i][j] = 0
            else:
                vs += 1
                val = arr[i][j]
                arr[i][j] = (vs, arr[i][j])
                vertices[str(vs)] = Vertice(i, j, str(vs), val)
        except:
            print("error: ", i, j)
#read_maze('input_file', arr, vertices) 
read_maze('maze2.txt', arr, vertices) 

lr = list()          
# Set Edge　for graph
getEdge(arr, vertices['G'].x, vertices['G'].y, edges, 'G', 1, 0, lr)
edge_labels=dict([((u,v),(d, p))
             for u,v,d,p,r in edges])
# Sort the vertice's edge by p and d
for key in vertices:
    vertices[key].edges.sort(key=lambda x:(x[3], x[2]))

print([(x[0], x[1])for x in edges])
print([(vertice[1].name, vertice[1].y+1, vertice[1].x+1, vertice[1].pok) for vertice in vertices.items()])        
print("vertice:{0}, Edge:{1}, Pokemon:{2}".format(len(vertices), len(edges), pok))

# ダイクストラ法でｓ->t,Pの最小ルートを探索（P最大）
rout = list()
vertices['S'].used = 1
for edge in vertices['S'].edges:
    nn = edge[1]
    vn = vertices[str(nn)]
    vnpoks = edge[3]
    if vn.pok == 'P':
        vnpoks -= 1 
    vn.dis, vn.poks, vn.pre = edge[2], vnpoks, 'S'
    heapq.heappush(rout, ((vn.poks, vn.dis),vn))
while len(rout)>0:
    v = heapq.heappop(rout)[1]
    v.used = 1
    for edge in v.edges:
        nn = edge[1]
        vn = vertices[str(nn)]
        if vn.used == 0:
            vnpoks = v.poks - edge[3] 
            if vn.pok == 'P':
                vnpoks -= 1
            if vn.dis == 0:
                vn.poks = vnpoks
                vn.dis = v.dis + edge[2]
                vn.pre = v.name
            else:
                if vn.poks > vnpoks:
                    vn.poks = vnpoks
                    vn.pre = v.name            
                elif vn.poks == vnpoks and vn.dis > v.dis + edge[2]:
                    vn.dis = v.dis + edge[2]
                    vn.pre = v.name
            heapq.heappush(rout, ((vn.poks, vn.dis),vn))
"""
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
"""
edgess=dict([((str(u),str(v)),[d, p, 0, r])
             for u,v,d,p,r in edges])

main_rout = list()
rp = ""
v = vertices['G']
v.used = 2
d = v.dis
p = v.poks
main_rout.append('G')
while v.pre != '':
    rp += "{0}({1},{2}) <- ".format(v.name, v.y+1, v.x+1)            
    vp = vertices[v.pre]
    vp.next = v.name
    edgess[(v.name, vp.name)][2] = 1
    edgess[(vp.name, v.name)][2] = 1
    v.edges.remove((v.name, vp.name, edgess[(v.name, vp.name)][0], edgess[(v.name, vp.name)][1]))    
    vp.edges.remove((vp.name, v.name, edgess[(vp.name, v.name)][0], edgess[(vp.name, v.name)][1]))    
    v = vp
    v.used = 2
    main_rout.append(v.name)
rp += "{0}({1},{2}) d:{3} p:{4}".format(v.name, v.y+1, v.x+1, d, -p)
print(rp)

def search_p(vertice):
    vertice.use = 2
    for e in vertice.edges:
        if (e[3] > 0 or vertices[e[1]].pok == 'P') and vertices[e[1]].used != 2:
            vertice.branch.append(e[1])
            edgess[(e[0], e[1])][2] = 1
            edgess[(e[1], e[0])][2] = 1
    vertice.edges.clear()
    for v in vertice.branch:
        search_p(vertices[v])

main_rout.reverse()
# main_routのverticesのegdesから'P'をBFS
for v in main_rout:
    search_p(vertices[v])

#　残りのP verticeを追加
for vs in vertices.items():
    v = vs[1]
    if v.pok == 'P' and v.used != 2:
        v.used = 2
        vertices[v.pre].branch.append(v.name)
        while v.pre != '' and vertices[v.pre].used != 2:
             vertices[v.pre].used = 2
             v = vertices[v.pre]
             vertices[v.pre].branch.append(v.name)             
"""
#　残りのP edgessを追加
for e in edgess.items():
    if e[1][1] != 0 and e[1][2] == 0:
        if vertices[e[0][1]].used == 2:
            vertices[e[0][0]].used = 2
            vertices[e[0][1]].branch.append(e[0][0])
        elif vertices[e[0][0]].used == 2:
            vertices[e[0][1]].used = 2
            vertices[e[0][0]].branch.append(e[0][1])
        else:
            if vertices[e[0][0]].dis > vertices[e[0][1]].dis:
                v = vertices[e[0][0]]
                vp = vertices[e[0][1]]
            else:
                v = vertices[e[0][1]]
                vp = vertices[e[0][0]]
            v.used = 2
            vp.branch.append(v.name)
            v = vp
            v.used = 2
            while True:
                vertices[v.pre].used = 2
                vertices[v.pre].branch.append(v.name)
                edgess[(vertices[v.pre].name, v.name)][2] = 1
                edgess[(v.name, vertices[v.pre].name)][2] = 1
                if v.pre != '' or vertices[v.pre].used != 2:
                    break
                v = vertices[v.pre]
        e[1][2] = 1
        edgess[(e[0][1], e[0][0])][2] = 1
"""
def pbr(wf, vn, vertices, edgess):
    v = vertices[vn]
    print("{0},{1}".format(v.x, v.y))
    wf.write("{0},{1}\n".format(v.x, v.y))
    for n in v.branch:
        for x, y in edgess[(v.name, n)][3]:
            print("{0},{1}".format(x, y))
            wf.write("{0},{1}\n".format(x, y))
        pbr(wf, n, vertices, edgess)
        for x, y in edgess[(n,v.name)][3]:
            print("{0},{1}".format(x, y))
            wf.write("{0},{1}\n".format(x, y))
        print("{0},{1}".format(v.x, v.y))
        wf.write("{0},{1}\n".format(v.x, v.y))

def print_out(file_name, main_rout, edgess, vertices):
    vo = ""
    with open(file_name, 'w') as f:
        for v in main_rout:
            if vo != "":
                for x, y in edgess[(vo,v)][3]:
                    print("{0},{1}".format(x, y))
                    f.write("{0},{1}\n".format(x, y))
            vo = v 
            if len(vertices[v].branch) > 0:    
                pbr(f, v, vertices, edgess)   
            if len(vertices[v].branch) == 0:
                print("{0},{1}".format(vertices[v].x, vertices[v].y))
                f.write("{0},{1}\n".format(vertices[v].x, vertices[v].y))
print_out('output_file', main_rout, edgess, vertices)

def chk_rout():
    arr = list()
#    for line in open('input_file', 'r'):
    for line in open('maze2.txt', 'r'):
        arr.append(list(line))
    for line in arr:
        l = ""
        for txt in line[:-1]:
            l += str(txt)
        print(l) 
    csv_reader = csv.reader(open("output_file", "r"), delimiter=",")
    org = None
    for row in csv_reader:
        if org != None:
            if abs(int(row[0]) - int(org[0])) + abs(int(row[1])-int(org[1])) != 1 or arr[int(row[0])][int(row[1])] == '*' :
                print("err at ", row)
                break
        arr[int(row[0])][int(row[1])] = ' '
        org = row
    for line in arr:
        l = ""
        for txt in line[:-1]:
            l += str(txt)
        print(l)
chk_rout()    