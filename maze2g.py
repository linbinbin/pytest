#!/usr/bin/env python
#import sys
#import random
import heapq
import networkx as nx
import matplotlib.pyplot as plt
import math
import itertools as it
import csv
import argparse
from logging import getLogger,StreamHandler,FileHandler,DEBUG,ERROR
logger = getLogger(__name__)
handler = StreamHandler()

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
        logger.error('x:{0}, y:{1}'.format(i,j))
        
def read_maze(file_name, arr, vertices):
    vs = 0
    global pok
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
                val = arr[i][j]
                vertices[arr[i][j]] = Vertice(i, j, arr[i][j], arr[i][j])        
                arr[i][j] = (val, val)
            elif arr[i][j] == 'P':
                vs += 1
                pok += 1
                val = arr[i][j]
                arr[i][j] = (vs, arr[i][j])
                vertices[str(vs)] = Vertice(i, j, str(vs), val)
                #logger.debug('p', str(vs), i, j)
            elif getWalls(arr, i, j) == 2 and arr[i][j] == ' ':
                arr[i][j] = 0
            else:
                vs += 1
                val = arr[i][j]
                arr[i][j] = (vs, val)
                vertices[str(vs)] = Vertice(i, j, str(vs), val)
        except:
            logger.error("over: x:{0}, y:{1}".format(i, j))

def getEdge(arr, lv, i, j, vertices, edges, c, lr):
    lv[0].used = 1
    for (a,b) in zip([1,-1,0,0], [0,0,1,-1]):
        rn = list(lr)
        if isWall(arr[i+a][j+b]) == 0 and isWall(arr[i+a*2][j+b*2]) == 0:
            arr[i+a][j+b] = '*'
            if arr[i+2*a][j+2*b] == 0:
                cn = c + 1
                rn.append((i+a, j+b))
                rn.append((i+a*2, j+b*2))
                getEdge(arr, lv, i+2*a, j+2*b, vertices, edges, cn, rn)                                   
            else:
                rn.append((i+a, j+b))           
                vn = arr[i+2*a][j+2*b][0]
                rrn = list(rn)
                rrn.reverse()
                cp = 0 if lv[0].pok == 'P' else 0
                p = 0 if vertices[str(vn)].pok == 'P' else 0
                edges.append((lv[0].name, str(vn), c, p, rn))
                edges.append((str(vn), lv[0].name, c, cp, rrn))               
                lv[0].edges.append((lv[0].name, str(vn), c, p))
                vertices[str(vn)].edges.append((str(vn), lv[0].name, c, cp))
                lv.append(vertices[str(vn)])
    del lr


# ダイクストラ法でｓ->t,Pの最小ルートを探索（P最大）
def mkrout(main_rout, vertices, edges, edgess):
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

    for u,v,d,p,r in edges:       
        edgess[(str(u),str(v))]=[d, p, 0, r]

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
    logger.debug(rp)
    main_rout.reverse()
    # main_routのverticesのegdesから'P'をBFS
    for v in main_rout:
        search_p(edgess, vertices[v])

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

def mkgraph(vertices, edges):
    edge_labels=dict([((u,v),(d, p))
                 for u,v,d,p,r in edges])
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

def search_p(edgess,vertice):
    vertice.used = 2
    for e in vertice.edges:
        if (e[3] > 0 or vertices[e[1]].pok == 'P') and vertices[e[1]].used != 2:
            vertice.branch.append(e[1])
            edgess[(e[0], e[1])][2] = 1
            edgess[(e[1], e[0])][2] = 1
    vertice.edges.clear()
    for v in vertice.branch:
        search_p(edgess, vertices[v])
            
def pbr(wf, vn, vertices, edgess):
    v = vertices[vn]
    logger.debug("{0},{1}".format(v.x, v.y))
    wf.write("{0},{1}\n".format(v.x, v.y))
    for n in v.branch:
        for x, y in edgess[(v.name, n)][3]:
            logger.debug("{0},{1}".format(x, y))
            wf.write("{0},{1}\n".format(x, y))
        pbr(wf, n, vertices, edgess)
        for x, y in edgess[(n,v.name)][3]:
            logger.debug("{0},{1}".format(x, y))
            wf.write("{0},{1}\n".format(x, y))
        logger.debug("{0},{1}".format(v.x, v.y))
        wf.write("{0},{1}\n".format(v.x, v.y))

def print_out(file_name, main_rout, edgess, vertices):
    vo = ""
    with open(file_name, 'w') as f:
        for v in main_rout:
            if vo != "":
                for x, y in edgess[(vo,v)][3]:
                    logger.debug("{0},{1}".format(x, y))
                    f.write("{0},{1}\n".format(x, y))
            vo = v 
            if len(vertices[v].branch) > 0:    
                pbr(f, v, vertices, edgess)   
            if len(vertices[v].branch) == 0:
                logger.debug("{0},{1}".format(vertices[v].x, vertices[v].y))
                f.write("{0},{1}\n".format(vertices[v].x, vertices[v].y))

def chk_rout(input, output):
    arr = list()
    for line in open(input, 'r'):
        arr.append(list(line))
    for line in arr:
        l = ""
        for txt in line[:-1]:
            l += str(txt)
        logger.debug(l) 
    csv_reader = csv.reader(open(output, "r"), delimiter=",")
    org = None
    for row in csv_reader:
        if org != None:
            if abs(int(row[0]) - int(org[0])) + abs(int(row[1])-int(org[1])) != 1 or arr[int(row[0])][int(row[1])] == '*' :
                logger.error("err at csv:{0}".fomat(row))
                break
        arr[int(row[0])][int(row[1])] = ' '
        org = row
    for line in arr:
        l = ""
        for txt in line[:-1]:
            l += str(txt)
        logger.debug(l)

if __name__ == "__main__":
    edges = list()
    arr = list()
    vertices = dict()
    edges_d = dict()
    global pok
    pok = 0 
    
    parser = argparse.ArgumentParser()
    parser.add_argument('input', default='input_file', help='in put file name')
    parser.add_argument('out', default='output_file', help='out put file name')
    parser.add_argument('-g', '--grf', action='store_true', help='make the Node graph')
    parser.add_argument('-c', '--chk', action='store_true', help='check the out file')
    parser.add_argument('-d', '--dbg', action='store_true', help='show the debug log')
    parser.add_argument('-f', '--logf', action='store_true', help='debug log to log.txt')
    #parser.parse_args(args=sys.argv, namespace=cmd)
    cmd = parser.parse_args()
    # Logging
    if cmd.logf:
        handler = FileHandler('log.txt', 'w')
    if cmd.dbg:
        handler.setLevel(DEBUG)
        logger.setLevel(DEBUG)
    else:
        handler.setLevel(ERROR)
        logger.setLevel(ERROR)        
    logger.addHandler(handler)

    #read_maze('input_file', arr, vertices) 
    read_maze(cmd.input, arr, vertices) 
    #rout list
    lr = list()
    #vertice list
    lv = list()          
    # Set Edge　for graph
    lv.append(vertices['S'])
    while len(lv) > 0:
        if lv[0].used == 0:
            getEdge(arr, lv, lv[0].x, lv[0].y, vertices, edges, 1, lr)
        lv.remove(lv[0])
    for key, item in vertices.items():
        item.used = 0

    if cmd.grf:
        mkgraph(vertices, edges)
    # Sort the vertice's edge by p and d
    for key in vertices:
        vertices[key].edges.sort(key=lambda x:(x[3], x[2]))

    logger.debug([(x[0], x[1])for x in edges])
    logger.debug([(vertice[1].name, vertice[1].y+1, vertice[1].x+1, vertice[1].pok) for vertice in vertices.items()])        
    logger.debug("vertice:{0}, Edge:{1}, Pokemon:{2}".format(len(vertices), len(edges), pok))
    
    main_rout = list()
    edgess = dict()
    mkrout(main_rout, vertices, edges, edgess)
    print_out(cmd.out, main_rout, edgess, vertices)

    if cmd.chk:
        chk_rout(cmd.input, cmd.out)
