#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import shutil
import sys
import time
import mktest

chk=lambda x: True if len([num[0] for num in x[1:] if num[-1]!='1'])>0 else False
if __name__ == "__main__":
    argv = sys.argv
    argc = len(argv)
    if argc<1:
        print "In put the id list"
        exit(1)
    no_auth = False
    case_num = 0
    for id in argv[1].split(','):
        print id, ': V301_IT_0167_{0:03d}'.format(case_num)
        ret = mktest.cmd(id, 'doc_user1', chk(id.split('_')), 'V301_IT_0167_{0:03d}'.format(case_num))
        case_num += 1
        if (not chk(id.split('_'))) and (not no_auth):
            ret += mktest.cmd(id, 'doc_user1_noauth', True, 'V301_IT_0167_{0:03d}'.format(case_num))
            no_auth = True
            case_num += 1
        if ret!= 0:
            print id + " mkshell error " + ret
            exit(1)
    print "Game over."
    exit(0)
