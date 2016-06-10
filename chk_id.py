#!/usr/bin/env python
# -*- coding: utf-8 -*-
from optparse import OptionParser
import os

def fild_all_files(directory):
    for root, dirs, files in os.walk(directory):
        yield root
        for file in files:
            yield os.path.join(root, file)

def chk_rsc_list(inname, outname):
    # read list file
    infile = open(inname, encoding="utf-8")
    inlines = infile.readlines()
    infile.close()
    outlines = []
    newh = []
    count = 0
    drop = 1
    for inline in inlines:
        items = inline.split(sep=" ")
        if items.__len__() > 2 and items[0] == "#define":
            drop = 1
            print(" find  ", items[1])
            srcfile = open("utlprm2docxml.c", encoding="utf-8")
            srclines = srcfile.readlines()
            srcfile.close()
            for srcline in srclines:
                if srcline.find(items[1]) >= 0:
                    drop = 0
                    break
            if drop == 1:
                print( "not use ", items[1])
                outlines.append(items[1]+"\n")
                newh.append('#defind '+items[1] +' \\\n\t\t\t"未使用\\0" \\\n')
            else:
                newh.append(inline)
        else:
            if drop == 1:
                count += 1
                if count < 2:
                    newh.append('\t\t\t"not used\\0" \n')
                else:
                    count = 0
                    drop = 0
            else:
                newh.append(inline)

    outfile = open(outname, 'w')
    for outline in outlines:
        outfile.writelines(outline)
    outfile.close()
    newfile = open("newfile.c", 'w', encoding="utf-8")
    for newline in newh:
        newfile.writelines(newline)
    newfile.close()

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-p", "--inname", dest="inname", default="prm2docxml.h")
    parser.add_option("-o", "--outname", dest="outname", default='out.txt')
    (options, args) = parser.parse_args()
    chk_rsc_list(options.inname, options.outname)
