#!/usr/bin/env python
'''# -*- coding: utf-8 -*-'''
#-*- coding: euc-jp -*-
import csv
import os
import sys
import random
from datetime import datetime as dt

def mkout(name, num, head):
	with open(name, 'w', encoding='euc-jp', newline='') as f:
		row=[]
		#row.append(("ID", "name", "address", "contents", "date"))
		names = ["12","13","14","15","16"]
		addresses=["22","23","24","25","26"]
		writer=csv.writer(f, lineterminator='\n')
		#for i in range(int(num)/2):
		size=int(num/2)
		for i in range(size):
			tdatetime = dt.now()
			tstr = tdatetime.strftime('%Y/%m/%d')
			row.append(("{0}".format(head+i), names[i%5], addresses[i%4], random.randint(0,num), tstr))
			row.append(("{0}".format(head+num-i), names[i%5], addresses[i%4], random.randint(0,num), tstr))
			if (i+1)%1000==0:
				writer.writerows(row)
				row=[]
		writer.writerows(row)
		f.close()

if __name__ == "__main__":
	param = sys.argv
	start = 0
	if len(param)<2:
		raise Exception('parameter', param)
	print("The file name of output:" + param[1])
	print("Record Number:" + param[2])
	if len(param)>3:
		start = int(param[3])
	mkout(param[1], int(param[2]), start)
