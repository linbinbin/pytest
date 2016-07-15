#!/usr/bin/env python
# coding:utf-8
import re
from xml.etree.ElementTree import *
from optparse import OptionParser, OptionValueError

def find_intag(tagname, value):
    

def chk_value(**opt, *arg):
    tree = parse("out.xml") if len(arg)==0 else parse(grg[0])
    elem = tree.getroot()
    et = None
    for esh in elem.getiterator("sheet"):
        if opt["sheet"] ==None or esh.get("name")==opt["sheet"]:
            #print "find ", esh.get("name")
            for idx, etl in enumerate(esh):
                if rg and etl.tag == "range" and etl.get("name") == rg:
                    #print "find range ", eall.get("name")
                    et = esh[(idx+1)%len(esh)]
                    break
            if et:
                for ertl in list(et):
                    #print "{0}\n".format(ertl.tag)
                    for iidx, erdl in enumerate(ertl):
                        #print u"{0} {1}\n".format(erdl.tag, erdl.text)
                        if erdl.tag == "td" and erdl.text == first_td:
                            #print u"{0} {1}\n".format(erdl.tag, erdl.text)
                            erdln = ertl[(iidx+1)%len(ertl)]
                            #print u"{0} {1}\n".format(erdln.tag, erdln.text)
                            if erdln.tag == "td" and erdln.text == value:
                                return 0
                            else:
                                return -1
            return -1

if __name__=="__main__":
    usage = "usage: %prog [options] [xmlfile]"
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
    parser.add_option("-s", "--sheet", dest="sheet", help="sheet name")
    parser.add_option("-t", "--table", dest="table", help="table name")
    parser.add_option("-r", "--range", dest="range", help="range name")
    parser.add_option("-td1", "--td1", dest="td1", help="value of td1")
    parser.add_option("-td2", "--td2", dest="td2", help="value of td2")
    #for v3
    #parser.add_argument("tsn", nargs=".", help="testbase number")
    #parser.add_argument("vdf", nargs=".", help="valid file")
    #parser.add_argument("cmt", nargs="?", help="comment")

    (options, args) = parser.parse_args()
    if chk_value(options, args) != 0:
        print "not find value {0}".format(options["td2"])
        exit(1)
    else:
        print "find value {0}".format(options["td2"])
        exit(0)



