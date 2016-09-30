#!/usr/bin/env python
# -*- coding: utf-8 -*-
from optparse import OptionParser
import os
import os.path
import shutil
import getpass
import sys
import codecs

def conv_encoding(fp):
    lookup = ('utf_8', 'euc_jp', 'euc_jis_2004', 'euc_jisx0213',
              'shift_jis', 'shift_jis_2004','shift_jisx0213',
              'iso2022jp', 'iso2022_jp_1', 'iso2022_jp_2', 'iso2022_jp_3',
              'iso2022_jp_ext','latin_1', 'iso_8859_1', 'ascii')
    encode = None
    data = None
    for encoding in lookup:
      try:
        print(str(encoding), "1")
        data = codecs.open(fp, 'r', encoding).read()
        print(str(encoding), "2")
        data = data.decode(encoding)
        print(str(encoding), "3")
        encode = encoding
        print(str(encoding))
        break
      except:
        pass
    if isinstance(data, str):
        return data,encode
    else:
        raise LookupError

def encode(enfile):
    data,encoding = None,None
    try:
        data,encoding = conv_encoding(enfile)
    finally:  
        pass
    enstr = '$data.="'
    count = 0
    for c in data:
        enstr += "".join("{0:02x}".format(ord(c)))
        count += 1
        if count % 40 == 0:
            enstr += '";'
            print(enstr)
            enstr = '$data.="'
    print(enstr,'";')
"""
    with codecs.open(enfile, 'r', 'euc-jp') as f:
        count = 0
        enstr = '$data.="'
        for line in f.readlines():
            for c in line:
                enstr += "".join("{0:02x}".format(ord(c)))
                count += 1
                if count % 40 == 0:
                    enstr += '";'
                    print(enstr)
                    enstr = '$data.="'
"""
def decode(defile):
    with open(defile) as f:
        for line in f.readlines():
            print(codecs.decode(line, "hex"))



if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-e", "--encode", dest="en", default='')
    parser.add_option("-d", "--decode", dest="de", default='')
    (options, args) = parser.parse_args();

    if (options.en != ''):
        encode(options.en)
        exit(0)
    if (options.de != ''):
        decode(options.de)
        exit(0)
    
