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
            if indata.find('cmp  $WORKDIR/out.xml $WORKDIR/valid\nif [ $? -ne 0 ] ; then') != -1:
                print(name)
                with codecs.open(name, 'w' ,encoding='utf8') as wf:
                    outdata = indata.replace('cmp  $WORKDIR/out.xml $WORKDIR/valid\nif [ $? -ne 0 ] ; then', 
                                             'rm -f tmp.txt\ndiff $WORKDIR/out.xml $WORKDIR/valid > tmp.txt\n\
if [ -f "tmp.txt" ] ; then\n\
    l1=`grep -e ^"[<|>]" tmp.txt | wc -l`\n\
    l2=`grep -e ">20[0-9][0-9]/[0-9][0-9]/[0-9][0-9]" tmp.txt | wc -l`\n\
fi\n\
if [ $l1 -ne $l2 ] ; then')
                    wf.write(outdata)
