#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import shutil
import sys
import time
import xmktest

chk=lambda x: True if len([num for num in x if num=='err'])>0 else False
if __name__ == "__main__":
    argv = sys.argv
    argc = len(argv)
    if argc<1:
        print("In put the id list")
        exit(1)
    no_auth = False
    case_num = 0
    print(argv[2])
    for id in argv[1].split(','):
        print(id, ': {1}_{0:02d}'.format(case_num+1, argv[2]))
        if len(argv)>3:
            ret = xmktest.cmd(id,  None, chk(id.split('_')), '{1}_{0:02d}'.format(case_num+1, argv[2]), argv[3])
        else:
            ret = xmktest.cmd(id,  None, chk(id.split('_')), '{1}_{0:02d}'.format(case_num+1, argv[2]), 0)
        case_num += 1
        if ret!= 0:
            print(id + " mkshell error " + ret)
            exit(1)
    print("Game over.")
    exit(0)
