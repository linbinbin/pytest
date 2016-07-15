#!/usr/bin/env python
# -*- coding: utf-8 -*-
from optparse import OptionParser
import os
import os.path
import shutil
import getpass
import sys
import codecs

def encode(enfile):
    with open(enfile) as f:
        count = 0
        for line in f.read():
            if count == 0:
                enstr = '$data.="'
            enstr += "".join("{0:02x}".format(ord(c)) for c in line)
            enstr += '";'
            print enstr

def decode(defile):
    with open(defile) as f:
        for line in f.readlines():
            print codecs.decode(line, "hex")



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
    
