#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 16:39:18 2016

@author: H8324261
"""

import urllib.request;
import sys;
import codecs;
import butyful
urllib.request.ProxyHandler({'https': 'https://Shinsei Okada:shu08lin@192.168.236.23:8080'})
urllib.request.ProxyHandler({'http': 'http://Shinsei Okada:shu08lin@192.168.236.23:8080'})
ret = urllib.request.urlopen("http://www.hi-ho.ne.jp/babaq/linux/gdb.html")
#sys.stdout = codecs.getwriter('shift_jis')(sys.stdout)
#print(ret.url, ret.status, ret.readlines().decode('shift_jis'))
html = ""
for line in ret.readlines():
    html = html+line.decode('shift_jis')
print(html)