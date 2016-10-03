#!/usr/bin/env python
# -*- coding: utf-8 -*-
from optparse import OptionParser, OptionValueError
from subprocess import call
from xml.etree.ElementTree import *
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
import re
import string

# string format 1: testbase no. 2: comment. 3: param ID
head = """
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
# huledenv.conf生成
# --------------------------------
mkhuledenv()
{{
perl -e '
$data.="6c6f675f6469723d7878780a776f726b5f6469723d7878780a706f72743d3130";
$data.="39380a6b6e6a636f64653d450a74726163655f6f75747075745f6d6f64653d30";
$data.="0a74726163655f7377697463685f6d6f64653d300a74726163655f7377697463";
$data.="685f73697a653d31300a74726163655f6b6565705f636e743d31300a7379736c";
$data.="6f675f6f75747075743d300a6f70656c6f675f6f75747075743d300a7365635f";
$data.="75736572706173735f73616d653d4e0a7365635f757365725f6e756d6f6e6c79";
$data.="3d4e0a7365635f706173735f6e756d6f6e6c793d4e0a7365635f757365725f61";
$data.="6c7068616f6e6c793d4e0a7365635f706173735f616c7068616f6e6c793d4e0a";
$data.="7365635f706173735f6d696e3d310a65645f6c6f675f6f75747075743d310a6c";
$data.="6f675f64656c5f626f726465723d31303030300a65645f6572725f6f75747075";
$data.="745f6c6576656c3d300a65645f6572725f7379736c6f675f666c61673d300a65";
$data.="645f6572725f6f75747075745f6d6f64653d520a65645f6572725f7377697463";
$data.="685f73697a653d300a6c6f63616c66696c655f6c6f636b6d6f64653d300a6875";
$data.="6c65646c616e673d4a504e0a64617465666d743d310a65645f7573655f746872";
$data.="6561643d310a65645f736f72745f6d657267655f7265636f7264636f756e743d";
$data.="353030303030300a63733466696c653d450a65645f6373765f6c696e65627265";
$data.="616b3d310a65645f6373765f656e636c6f73656669656c64733d310a65645f66";
$data.="6d745f6e756c6c5f666c61673d310a65645f66697876616c75655f6374726c63";
$data.="6861725f666c61673d310a636f6d706172655f646966666572656e745f747970";
$data.="655f646174613d310a74726561745f646f745f61735f736368656d613d310a";
@yy = pack("H*", $data); print "@yy";' > tmp.huledenv.conf
}}

mkhuledenv
mv $DMPATH/huledenv.conf $DMPATH/huledenv.conf.bak
#テスト用のテンポラリのhuledenv.confをコピー
mv tmp.huledenv.conf $DMPATH/huledenv.conf

# --------------------------------
# パラメータ作成
# --------------------------------
mkparam()
{{
	cat <<STRING >$WORKDIR/param\n"""


tail="""STRING\n}\n"""


data_head="""
# --------------------------------
# 比較データ生成
# --------------------------------
mkvalid()
{
        cat <<STRING >$WORKDIR/valid
"""
data_tail="""STRING
}}

#不要ファイル削除
rm -f $WORKDIR/valid* $WORKDIR/param $WORKDIR/err $WORKDIR/LOG $WORKDIR/out.*

#インポートファイル作成
mkparam

#管理情報を登録
utlediupdt -f $WORKDIR/param -r -k 8 >$WORKDIR/LOG
if [ $? -ne 0 ] ; then
	echo "utlediupdt failure"
	mv $DMPATH/huledenv.conf.bak $DMPATH/huledenv.conf 
	exit 1
fi

#仕様書出力を実行
utlprm2docxml -i {0} -lang {1} -o $WORKDIR/out.dat > $WORKDIR/err  2>&1
if [ $? -ne 0 ] ; then
	echo "utlprm2docxml is false"
	mv $DMPATH/huledenv.conf.bak $DMPATH/huledenv.conf 
	exit 1
fi

ID={0}
USER_ID=`whoami`
PRMDB="$DMPATH/edprm.db"
PRM_TIME=`sqlite3 "$PRMDB" "select substr(stime,1,19) from _edprm_master where id = '$ID';"`
PRM_DATE=`sqlite3 "$PRMDB" "select substr(stime,1,10) from _edprm_master where id = '$ID';"`
#Validファイル作成
mkvalid

mv $DMPATH/huledenv.conf.bak $DMPATH/huledenv.conf 

xmllint --format --output $WORKDIR/out.xml $WORKDIR/out.dat
if [ $? -ne 0 ] ; then
	echo "xmllint err"
	exit 1
fi

rm -f tmp.txt
diff $WORKDIR/out.xml $WORKDIR/valid > tmp.txt
if [ -f "tmp.txt" ] ; then
    l1=`grep -e ^"[<|>]" tmp.txt | wc -l`
    l2=`grep -e ">20[0-9][0-9]/[0-9][0-9]/[0-9][0-9]" tmp.txt | wc -l`
fi
if [ $l1 -ne $l2 ] ; then
    echo "cmp $WORKDIR/out.xml <=> $WORKDIR/valid failure"
    exit 1
fi

exit 0
"""

fnhex=lambda idx, x:"{0:02x}\n".format(ord(x)) if (idx+1)%40==0 else "{0:02x}".format(ord(x))
fn64=lambda idx, x:"{0}\n".format(x) if (idx+1)%80==0 else "{0}".format(x)

#get prm from db (not use)
def get_prm_str(wk_id, user_id, err, lang):
    try:
        retcode = call("cp $DMPATH/huledenv.conf $huledenv.conf.bak; cp  igen.cnf $DMPATH/huledenv.conf;", shell=True)
        retcode += call("utledigen -f {id}.igen -i ed -R -d {id} -k 8".format(id=wk_id), shell=True)
        if abs(retcode) > 0:
            print(wk_id, " utledigen error ", retcode)
            exit(3)
        retcode = call("utlprm2docxml -i {id} -lang {lang} -o out.dat > err 2>&1".format(id=wk_id, lang=lang), shell=True)
        retcode += call("xmllint --format --output out.xml out.dat", shell=True)
        retcode += call("cp  $huledenv.conf.bak $DMPATH/huledenv.conf;", shell=True)
        if abs(retcode) > 0:
            print(wk_id, " utlprm2docxml error ", retcode)
            exit(3)
    except OSError as e:
        print("err:", e, file=sys.stderr)
        exit(3)

    with codecs.open(wk_id+'.igen', 'r', 'utf_8') as rf:
        return rf.read().replace('\r\n','\n')+tail
    return None    

#get valid block
def get_val_str(id, err, userid, lang):
    ret = ''
    ret += data_head
    name = "out.xml"
    with codecs.open(name, 'r' ,encoding='utf8') as f:
        ret += f.read()
        ret += data_tail.format(id, lang)
        #ret = ret.encode("utf-8")
        ret = ret.replace('okada', '$USER_ID')
        ret = ret.replace('admin', '$USER_ID')
        ret = re.sub(r'201[0-9]/\d{2}/\d{2}</td>','$PRM_DATE</td>', ret)
        ret = re.sub(r'201[0-9]/\d{2}/\d{2}\s.*</td>','$PRM_TIME</td>', ret)
        #print ret.encode("utf-8")
        return ret

def cmd(wk_id, user_id, err, cmt, lang):
    prm = get_prm_str(wk_id, user_id, err, lang)
    if prm == None or len(prm) == 0:
        return 1

    valid = get_val_str(wk_id, err, user_id, lang)
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
        print("make shell false.")
        exit(5)

    exit(0)
