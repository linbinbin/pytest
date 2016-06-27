#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 16:39:18 2016

@author: H8324261
"""

import urllib.request
import sys
import codecs
import pandas as pd
import texttable as tt

# full width versions (SPACE is non-contiguous with ! through ~)
SPACE = '\N{IDEOGRAPHIC SPACE}'
EXCLA = '\N{FULLWIDTH EXCLAMATION MARK}'
TILDE = '\N{FULLWIDTH TILDE}'

# strings of ASCII and full-width characters (same order)
west = ''.join(chr(i) for i in range(ord(' '),ord('~')))
east = SPACE + ''.join(chr(i) for i in range(ord(EXCLA),ord(TILDE)))

# build the translation table
full = str.maketrans(west,east)

urllib.request.ProxyHandler({'https': 'https://Shinsei_Okada:shu09lin@192.168.236.23:8080'})
urllib.request.ProxyHandler({'http': 'http://Shinsei_Okada:shu09lin@192.168.236.23:8080'})
ret = urllib.request.urlopen("http://www.hi-ho.ne.jp/babaq/linux/gdb.html")
#sys.stdout = codecs.getwriter('shift_jis')(sys.stdout)
#print(ret.url, ret.status, ret.readlines().decode('shift_jis'))
html = ""
writer = pd.ExcelWriter("pandas.xlsx", engine='xlsxwriter')
for line in ret.readlines():
    html = html+line.decode('shift_jis')
_data = pd.read_html(html)
for idx, tbl in enumerate(_data):
	#print("item[{}]: type:{}\n{} \n".format(idx, type(tbl), tbl))
	tab = tt.Texttable()
	tab.set_cols_width([15,38])
	#tab.header(tbl[0])
	for i in range(len(tbl)):
		#print("len1:{0}, len2:{1}\n".format(len(tbl[0][i]), len(tbl[1][i])))
		#tab.add_row([tbl[0][i].translate(full).rstrip().split('\n'), tbl[1][i].translate(full).rstrip().split('\n')])
		tab.add_row([tbl[0][i], tbl[1][i]])
	print(tab.draw())
	tbl.to_excel(writer, "table"+str(idx), index=False)
writer.save()
	#print("tbl[0]:{}\ntbl[1]:{}\n".format(tbl[0], tbl[1]))

