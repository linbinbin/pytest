#!/usr/bin/env python
# -*- coding: utf-8 -*-
from optparse import OptionParser
import os
import sys

def fild_all_files(directory):
    for root, dirs, files in os.walk(directory):
        yield root
        for file in files:
            yield os.path.join(root, file)

def chk_rsc_list(pathname, outname):
    # read list file
    infile = open(outname)
    inlines = infile.readlines()
    infile.close()
    outlines = []
    count = 0
    for inline in inlines:
        drop = 1
        count += 1
        print count, " find  ", inline 
        for file in fild_all_files(pathname):
            if os.path.isdir(file):
                continue
            srcfile = open(file)
            srclines = srcfile.readlines()
            srcfile.close()
            for srcline in srclines:
                if srcline.find(inline[:-1]) >= 0 and srcline[0:2] != '//':
                    drop = 0
                    break
            if drop == 0:
                break
        if drop == 1:
            print "add ", inline
            outlines.append(inline)
    os.remove(outname)
    outfile = open(outname, 'w')
    for outline in outlines:
        outfile.writelines(outline)
    outfile.close()

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-p", "--path", dest="pathname", default="./")
    parser.add_option("-o", "--outname", dest="outname", default='out.txt')
    (options, args) = parser.parse_args()
    chk_rsc_list(options.pathname, options.outname)
