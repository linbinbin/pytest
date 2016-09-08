#!/usr/bin/env python
#import sys
import heapq
import itertools as it
import argparse
import csv
from logging import getLogger,StreamHandler,FileHandler,DEBUG,ERROR
logger = getLogger(__name__)
handler = StreamHandler()

def print_matrix(m):
	for row in m:
		print(row)

def sudoku(matrix):
	vs = {"r1":[[1,2,3,4,5,6,7,8,9],[]], "r2":[[1,2,3,4,5,6,7,8,9],[]], "r3":[[1,2,3,4,5,6,7,8,9],[]],\
		"r4":[[1,2,3,4,5,6,7,8,9],[]], "r5":[[1,2,3,4,5,6,7,8,9],[]], "r6":[[1,2,3,4,5,6,7,8,9],[]],\
		"r7":[[1,2,3,4,5,6,7,8,9],[]], "r8":[[1,2,3,4,5,6,7,8,9],[]], "r9":[[1,2,3,4,5,6,7,8,9],[]],\
		"c1":[[1,2,3,4,5,6,7,8,9],[]], "c2":[[1,2,3,4,5,6,7,8,9],[]], "c3":[[1,2,3,4,5,6,7,8,9],[]],\
		"c4":[[1,2,3,4,5,6,7,8,9],[]], "c5":[[1,2,3,4,5,6,7,8,9],[]], "c6":[[1,2,3,4,5,6,7,8,9],[]],\
		"c7":[[1,2,3,4,5,6,7,8,9],[]], "c8":[[1,2,3,4,5,6,7,8,9],[]], "c9":[[1,2,3,4,5,6,7,8,9],[]],\
		"m11":[[1,2,3,4,5,6,7,8,9],[]], "m12":[[1,2,3,4,5,6,7,8,9],[]], "m13":[[1,2,3,4,5,6,7,8,9],[]],\
		"m21":[[1,2,3,4,5,6,7,8,9],[]], "m22":[[1,2,3,4,5,6,7,8,9],[]], "m23":[[1,2,3,4,5,6,7,8,9],[]],\
		"m31":[[1,2,3,4,5,6,7,8,9],[]], "m32":[[1,2,3,4,5,6,7,8,9],[]], "m33":[[1,2,3,4,5,6,7,8,9],[]]}
	hp = list()
	#create unset posetion and value list set
	for i, row in enumerate(matrix):
		for j, col in enumerate(row):
			try:
				if col != 0:
					vs['r'+str(i+1)][0].remove(col)
					vs['c'+str(j+1)][0].remove(col)
					vs['m'+str(int(i/3+1))+str(int(j/3+1))][0].remove(col)
				else:
					vs['r'+str(i+1)][1].append((i,j))
					vs['c'+str(j+1)][1].append((i,j))
					vs['m'+str(int(i/3+1))+str(int(j/3+1))][1].append((i,j))
			except:
				print(col, i, j)
	for key, item in vs.items():
		if len(item[0])>0:
			heapq.heappush(hp, [len(item[0]), key])
	if len(hp) == 0:
		print(matrix)
		exit(0)

	length, key = heapq.heappop(hp)
	v = vs[key]
	#print(length, key)
	#print(v)
	#print_matrix(matrix)
	for val in v[0]:
		for pos in v[1]:
			if val in vs['r'+str(pos[0]+1)][0] and val in vs['c'+str(pos[1]+1)][0] and val in vs['m'+str(int(pos[0]/3+1))+str(int(pos[1]/3+1))][0]:
				if matrix[pos[0]][pos[1]] != 0:
					print(pos[0], pos[1], matrix[pos[0]][pos[1]])
					print_matrix(matrix)
					exit(1)
				matrix[pos[0]][pos[1]] = val
				#print('set ({0},{1}):{2}'.format(pos[0],pos[1],matrix[pos[0]][pos[1]]))
				if not sudoku(matrix):
					matrix[pos[0]][pos[1]] = 0
	return False

if __name__ == "__main__":
	handler = FileHandler('log.txt', 'w')
	handler.setLevel(DEBUG)
	logger.setLevel(DEBUG)
	parser = argparse.ArgumentParser()
	parser.add_argument('input', help='in put file name')
	parser.add_argument('out', help='out put file name')
	parser.add_argument('-c', '--chk', action='store_true', help='check the out file')
	parser.add_argument('-d', '--dbg', action='store_true', help='show the debug log')
	parser.add_argument('-f', '--logf', action='store_true', help='debug log to log.txt')
    #parser.parse_args(args=sys.argv, namespace=cmd)
	cmd = parser.parse_args()

    #read input
	with open(cmd.input, "r") as f:
		matrix = list()
		for row in csv.reader(f, delimiter=","):
			lrow = list()
			for val in row:
				data = int(val) if val in '123456789' else 0
				lrow.append(data)
			matrix.append(lrow)
	sudoku(matrix)