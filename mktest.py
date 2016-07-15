#!/usr/bin/env python
# -*- coding: utf-8 -*-
from optparse import OptionParser, OptionValueError
from subprocess import call
import os
import os.path
import shutil
import getpass
import sys
import codecs
import sqlite3
import base64
import time
import code


# string format 1: testbase no. 2: comment. 3: param ID
head = u"""
#! /bin/sh

###
### TESTBASE :{num}
### comment  :{com}
###
WORKDIR=`dirname $0`
mkfunc()
{{
	if [ -f $WORKDIR/functions ]; then
		return
	fi

	cat <<STRING >tmp$$
0a6765745f6b6e6a636f646528290a7b0a0967726570205e6b
6e6a636f6465202448554c504154482f68756c6564656e762e
636f6e66207c0a0909736564202d65202273236b6e6a636f64
655b205c745d2a3d5b205c745d2a2323220a7d0a0a66696c65
63726c6628290a7b0a097065726c202d7065202773235c725c
6e235c6e2327202431203e20746d7024242e7478740a096d76
20746d7024242e7478742024310a7d0a0a66696c65636f6465
636f6e7628290a7b0a096c6f63616c20636f64650a0a096966
205b202423202d65712030205d3b207468656e0a0909656368
6f202275736167653a2066696c65636f6465636f6e76206669
6c656e616d65220a090972657475726e20310a0966690a0a09
6361736520606765745f6b6e6a636f64656020696e0a094529
0a09096e6b66202d6578202431207c207065726c202d706520
2773235c725c6e235c6e2327203e20746d7024242e7478740a
09096d7620746d7024242e7478742024310a09093b3b0a0953
290a09096e6b66202d7378202431207c207065726c202d7065
202773235c725c6e235c6e2327203e20746d7024242e747874
0a09096d7620746d7024242e7478742024310a09093b3b0a09
38290a09096e6b66202d7778202431207c207065726c202d70
65202773235c725c6e235c6e2327203e20746d7024242e7478
740a09096d7620746d7024242e7478742024310a09093b3b0a
09657361630a0972657475726e20300a7d0a
STRING
	perl -e '
	my @data = <>;
	chomp(@data);
	my $data = join("", @data);
	my @file = pack("H*", $data);
	print "@file";
	' tmp$$ > $WORKDIR/functions
	rm -f tmp$$
}}

mkfunc

. $WORKDIR/functions

# --------------------------------
# パラメータ作成
# --------------------------------
mkparam()
{{
	cat <<STRING >param\n"""


tail=u"""STRING\n}\n"""


data_head=u"""
# --------------------------------
# 比較データ生成
# --------------------------------
mkvalid()
{
        cat <<STRING >tmp$$
"""
data_tail_err=u"""
STRING
	perl -e '
	my @data = <>;
	chomp(@data);
	my $data = join("", @data);
	my @file = pack("H*", $data);
	print "@file";
	' tmp$$ > valid
	rm -f tmp$$
}}

#不要ファイル削除
rm -f valid* param err LOG out.*

#インポートファイル作成
mkparam

#比較データ作成
mkvalid

#DB 更新
$WORKDIR/user_db

unset BS_USER

#管理情報を登録
utlediupdt -f param -r -k 8 >LOG
if [ $? -ne 0 ] ; then
	echo "utlediupdt failure"
	exit 1
fi
{1}
#仕様書出力を実行
utlprm2docxml -i {0} -o out.xml > err  2>&1
if [ $? -eq 0 ] ; then
	echo "utlprm2docxml sucess but the auth check is false"
	unset BS_USER
	exit 1
fi

grep -v TRNTIMEONERR err > tmp$$
mv tmp$$ err

cmp err valid
if [ $? -ne 0 ] ; then
	echo "cmp err <=> valid failure"
	unset BS_USER
	exit 1
fi
unset BS_USER
exit 0
"""
data_tail=u"""
STRING
	perl -e '
	my @data = <>;
	chomp(@data);
	my $data = join("", @data);
	my @file = pack("H*", $data);
	print "@file";
	' tmp$$ > valid
	rm -f tmp$$
}}

#不要ファイル削除
rm -f valid* param err LOG out.*

#インポートファイル作成
mkparam

#DB 更新
$WORKDIR/user_db

unset BS_USER

#管理情報を登録
utlediupdt -f param -r -k 8 >LOG
if [ $? -ne 0 ] ; then
	echo "utlediupdt failure"
	exit 1
fi
{1}
#仕様書出力を実行
utlprm2docxml -i {0} -o out.xml > err  2>&1
if [ $? -ne 0 ] ; then
	echo "utlprm2docxml is false"
        unset BS_USER
	exit 1
fi

xmllint out.xml > /dev/null
if [ $? -ne 0 ] ; then
	echo "xmllint err"
        unset BS_USER
	exit 1
fi
unset BS_USER
exit 0
"""

fnhex=lambda idx, x:"{0:02x}\n".format(ord(x)) if (idx+1)%40==0 else "{0:02x}".format(ord(x))
fn64=lambda idx, x:"{0}\n".format(x) if (idx+1)%80==0 else "{0}".format(x)

#get prm from db (not use)
def get_prm_str(wk_id, user_id, err):
    try:
        retcode = call("utledigen -f {id}.igen -i ed -R -d {id}".format(id=wk_id), shell=True)
        if abs(retcode) > 0:
            print  wk_id, " utledigen error ", retcode
            exit(3)
        if user_id:
            retcode = call("export BS_USER={user};utlprm2docxml -i {id} -o out.dat > err 2>&1;unset BS_USER".format(id=wk_id, user=user_id), shell=True)
        else:
            retcode = call("unset BS_USER;utlprm2docxml -i {id} -o out.dat > err 2>&1".format(id=wk_id), shell=True)
        if abs(retcode) > 0:
            print  wk_id, " utlprm2docxml error ", retcode
            exit(3)
    except OSError, e:
        print >>sys.stderr, "err:", e
        exit(3)

    with codecs.open(wk_id+'.igen', 'r', 'utf_8') as rf:
        return rf.read().replace('\r\n','\n')+tail
    return None    

#get valid block
def get_val_str(id, err, userid):
    ret = ''
    ret += data_head
    name = "err" if err else "out.dat"
    with open(name, 'r') as f:
        ret += ''.join(fnhex(idx, x) for idx, x in enumerate(f.read()))
        export = 'export BS_USER={0}'.format(userid) if userid != None else ''
        if err:
            ret += data_tail_err.format(id, export)
            return ret
        else:
            ret += data_tail.format(id, export)
            return ret

def cmd(wk_id, user_id, err, cmt):
    prm = get_prm_str(wk_id, user_id, err)
    if prm == None or len(prm) == 0:
        return 1

    valid = get_val_str(wk_id, err, user_id)
    if len(valid) < 0:
        return 1

    #open and write out file
    with codecs.open("{0}.sh".format(cmt), 'w', 'utf_8') as wf:
        wf.write(head.format(num=wk_id, com=cmt if cmt else ''))
        wf.write(prm)
        wf.write(valid)
        return 0
    return 1
    

# スクリプトの使用方法を表す文字列
# デフォルト値は"Usage: %prog [options]"
# "usage: "で始まらないと自動的に"usage :"が追加される
# %progはスクリプト名で置換

if __name__ == "__main__":
    usage = "usage: %prog [options] testbase_number[comment]"
    parser = OptionParser(usage)
# オプションの追加
# action オプションが見つかった場合に行う処理
# type   オプションの型
# dest   引数の保存先
#        省略時は長いオプション名を使用
#        それも省略なら短いオプション名
# default オプションのデフォルト値
#         省略した場合のデフォルト値はNone
# metavar ヘルプ表示で使われる仮引数
#         省略時は保存先の名前を大文字にして使用
    parser.add_option("-e", "--error", action="store_true",  default=False, dest="err", help="err case option")
    parser.add_option("-u", "--userid", dest="userid", help="bs_user")
    #for v3
    #parser.add_argument("tsn", nargs=".", help="testbase number")
    #parser.add_argument("vdf", nargs=".", help="valid file")
    #parser.add_argument("cmt", nargs="?", help="comment")

    (options, args) = parser.parse_args()
    if (not args) or len(args)<1:
        parser.error("requires parameters.")
        exit(1)

    if cmd(args[0], options.userid, options.err, args[1])!=0:
        print "make shell false."
        exit(5)

    exit(0)
