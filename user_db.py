#!/usr/bin/env python
# -*- coding: utf-8 -*-
from optparse import OptionParser, OptionValueError
import os
import os.path
import shutil
import getpass
import sys
import sqlite3
import time


def update_users(path):
    # データベースへ接続
    tm = time.strftime("%Y/%m/%d %H:%M:%S.000000", time.localtime())
    user_update_sql="""REPLACE INTO _master VALUES('{userid}','{key}','','M70iHOBr+19YEQBZ2xJu2Q==','{userid}','','admin','{com}','{auth_type}','{user_type}','','{time}','','{time}','')"""
    auth_update_sql="""REPLACE INTO _auth VALUES('{grpid}','{userid}','admin','{def_auth}','{exec_auth}','{time}',NULL)"""
    ggrp_update_sql="""REPLACE INTO _ggrp VALUES('{grpid}','{com}','admin','{omit_auth}','{time}', NULL)"""

    user_list = [
        {'userid':'doc_user1', 'key':'DOC_USER1', 'com':'grp1_user com', 'auth_type':'P', 'user_type':'G', 'time':tm},
        {'userid':'doc_user1_noauth', 'key':'DOC_USER1_NOAUTH', 'com':'grp1_user no auth com', 'auth_type':'P', 'user_type':'G', 'time':tm},
        {'userid':'doc_user2', 'key':'DOC_USER2', 'com':'grp2_user com', 'auth_type':'P', 'user_type':'G', 'time':tm},
        {'userid':'doc_user2_noauth', 'key':'DOC_USER2_NOAUTH', 'com':'grp2_user no authcom', 'auth_type':'P', 'user_type':'G', 'time':tm},
        {'userid':'doc_user12', 'key':'DOC_USER12', 'com':'grp1_2_user com', 'auth_type':'P', 'user_type':'G', 'time':tm},
        {'userid':'doc_user3', 'key':'DOC_USER3', 'com':'grp3_user com', 'auth_type':'P', 'user_type':'G', 'time':tm},
    ]

    grp_list = [
        {'grpid':'DOC_GRP1', 'com':'doc_group1', 'omit_auth':0, 'time':tm},
        {'grpid':'DOC_GRP2', 'com':'doc_group2', 'omit_auth':0, 'time':tm},
        {'grpid':'DOC_GRP3', 'com':'doc_group3', 'omit_auth':0, 'time':tm},
    ]

    auth_list = [
        {'grpid':'DOC_GRP1', 'userid':'doc_user1', 'def_auth':'U', 'exec_auth':'X', 'time':tm},
        {'grpid':'DOC_GRP1', 'userid':'doc_user1_noauth', 'def_auth':'N', 'exec_auth':'N', 'time':tm},
        {'grpid':'DOC_GRP2', 'userid':'doc_user2', 'def_auth':'U', 'exec_auth':'X', 'time':tm},
        {'grpid':'DOC_GRP2', 'userid':'doc_user2_noauth', 'def_auth':'N', 'exec_auth':'N', 'time':tm},
        {'grpid':'DOC_GRP1', 'userid':'doc_user12', 'def_auth':'U', 'exec_auth':'X', 'time':tm},
        {'grpid':'DOC_GRP2', 'userid':'doc_user12', 'def_auth':'U', 'exec_auth':'X', 'time':tm},
        {'grpid':'DOC_GRP3', 'userid':'doc_user3', 'def_auth':'U', 'exec_auth':'X', 'time':tm},        
    ]
#    user_update_sql="""REPLACE INTO _master VALUES('{0}','{1}','','M70iHOBr+19YEQBZ2xJu2Q==','{2}','','admin','{3}','{4}','{5}','','{6}','','{7}','')"""
#    now = time.strftime("%Y/%m/%d %H:%M:%S.000000", time.localtime())
#    user_list = [
#        ('grp4_user', 'GRP4_USER','grp4_user',  'grp4_user com', 'P', 'G', now, now),
#        ('grp5_user', 'GRP5_USER','grp5_user',  'grp5_user com', 'P', 'G', now, now)
#    ]

    with sqlite3.connect(os.path.join(path,'user.db')) as db_user:
            with sqlite3.connect(os.path.join(path,'ggrp.db')) as db_ggrp:
                ucur = db_user.cursor()
                gcur = db_ggrp.cursor()
                try:
                    for user in user_list:
                        ucur.execute(user_update_sql.format(**user))
                    for grp in grp_list:
                        gcur.execute(ggrp_update_sql.format(**grp))
                    for au in auth_list:
                        gcur.execute(auth_update_sql.format(**au))
                    db_user.commit()
                    db_ggrp.commit()
                except sqlite3.Error, e:            
                    print "Error {0}".format(e.args[0])
                    db_user.rollback()
                    db_ggrp.rollback()
                    return -1
                return 0

if __name__ == "__main__":
    usage = "usage: %prog [options]"
    parser = OptionParser(usage)
    parser.add_option("-d", "--debug", action="store_true",  default=False, dest="debug", help="debug option")
    (options, args) = parser.parse_args()
    path=os.environ['DMPATH'] if not options.debug else ''
    #print "path:{0}\n".format(path)
    update_users(path)
