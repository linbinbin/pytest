#!/usr/bin/env python
#-*- coding: euc-jp -*-
import csv
import os
import sys
import random
from datetime import datetime as dt
from optparse import OptionParser
from argparse import ArgumentParser

def mkout(name, num, head):
	with open(name, 'w', encoding='euc-jp', newline='') as f:
		row=[]
		writer=csv.writer(f, lineterminator='\n')
		for i in range(num):
			tdatetime = dt.now()
			tstr = tdatetime.strftime('%Y/%m/%d')
			row.append(('col1_'+str(head+i), 'col2_'+str(head+i), 'col3_'+str(head+i), tstr))
			if (i+1)%1000==0:
				writer.writerows(row)
				row=[]
		writer.writerows(row)
		f.close()

if __name__ == "__main__":
	""" コマンドエラー時に表示する文字列 """
	desc = '{0} [Args] [Options]\nDetailed options -h or --help'.format(__file__)
	# %progは出力できない
	# usage = u'%prog [Args] [Options]\nDetailed options -h or --help'

	parser = ArgumentParser(description=desc)
	# _parser = OptionParser(usage=usage, version=1.0)
	
	# 文字列
	parser.add_argument(
		'-f', '--file',
		type = str,
		dest = 'filename',
		required = False,
		default='xmlinput.csv',
		help = 'The output file name'
		)	

	parser.add_argument(
		'-n', '--nrec',
		type = int,
		dest = 'nrec',
		required = False,
		default=1000,
		help = 'The output file recode number'
		)	

	parser.add_argument(
		'-s', '--start',
		type = int,
		dest = 'start',
		required = False,
		default=0,
		help = 'The output file start recode number'
		)	

	args = parser.parse_args()
	mkout('csv/'+args.filename, args.nrec, args.start)
