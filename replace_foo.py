#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import codecs

for path, sub_dirs, files in os.walk('.'):
    for f in files:
        #print(list(os.path.splitext(f)))
        if os.path.splitext(f)[1] == '.sh':
            name = ''.join([path, '/', f])
            #print(name)
            indata = ''
            outdata = ''
            with codecs.open(name, 'r' ,encoding='utf8') as rf:
                try:
                    indata = rf.read()
                except:
                    pass
            if indata.find('>Ntype ') != -1:
                print(name)
                with codecs.open(name, 'w' ,encoding='utf8') as wf:
                    outdata = indata.replace('>Ntype ', '>Nタイプ')
                    wf.write(outdata)
