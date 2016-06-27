#!/usr/bin/env python
# -*- coding: utf-8 -*-
from optparse import OptionParser
import sqlite3
import numpy as np
import matplotlib.pyplot as plt

def plotout(filename, nmap, scal):
    mapcount = 0
    updatecount = 0
    registcount = 0
    update_array_np = []
    regist_array_np = []
    update_array_plot = []
    regist_array_plot = []
    # データベースへ接続
    conn = sqlite3.connect(filename)
    # カーソルの作成
    cur = conn.cursor()    
    cur.execute("""SELECT process,sec,usec,nrec FROM xmlprotime WHERE process='xml_element_regist' OR process='xml_db_update-all' ORDER BY nrec;""")
    for process, sec, usec, nrec in cur.fetchall():
        if process == "xml_element_regist":
            regist_array_np.append(sec*1000000+usec)
            if registcount%(nmap*scal) == 0:
                regist_array_plot.append(np.mean(np.array(regist_array_np)))
                del regist_array_np[:]
            registcount = registcount + 1
        elif process == "xml_db_update-all":
            update_array_np.append(sec*1000000+usec)
            if updatecount%(scal) == 0:
                update_array_plot.append(np.mean(np.array(update_array_np)))
                #print(np.mean(np.array(update_array_np)))
                del update_array_np[:]
            updatecount = updatecount + 1
        else:
            continue

    print("regist = " + str(len(regist_array_plot)) + " update = " + str(len(update_array_plot)))
    x = range(0, len(regist_array_plot), 1)
    plt.plot(x, regist_array_plot, label='regist '+ str(np.mean(np.array(regist_array_plot))) + '/rec')
    plt.plot(x, update_array_plot, label='update '+ str(np.mean(np.array(update_array_plot))) + '/rec')
    plt.title('Process Time')
    plt.xlabel('record * '+str(scal))
    plt.ylabel('time(usec) label')
    plt.legend()
    plt.savefig(filename.split('.')[0]+'_'+str(scal)+".png")
    plt.show()

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename", default='xmloutdb_0000.db')
    parser.add_option("-n", "--nmap", type="int", dest="nmap", default=3)
    parser.add_option("-s", "--scal", type="int", dest="scal", default=100)
    (options, args) = parser.parse_args()
    plotout(options.filename, options.nmap, options.scal)

