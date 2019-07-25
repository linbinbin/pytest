import gzip
import hashlib
import os, os.path
import sys
import re
import shutil
import time
import pandas as pd
import fileinput
import time

inpth = r"D:\talend\data\out_put_csv"
outpth = r"D:\tmp"

now = time.ctime()
cnvtime = time.strptime(now)
print(time.strftime("%Y/%m/%d %H:%M", cnvtime))
files = os.listdir(inpth)
for file in files:
    #print(file)
    if re.match('.*gz$', file):
        filename=file[0:18]
        print(filename)
        with gzip.open(os.path.join(inpth, file), mode='rt') as f:
            d = f.readlines()
            print(len(d))
            print(d[4])
            d1=d[5:len(d)]
            print(len(d1))
            with open(os.path.join(outpth, filename+'.csv'), "w") as f1:
                for ln in d1:
                    f1.write(ln)
            with open(os.path.join(outpth, filename+'.csv'), 'rb') as f_in:
                with gzip.open(os.path.join(outpth, filename+'.csv.gz'), 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            os.remove(os.path.join(outpth, filename+'.csv'))
end = time.ctime()
endtime = time.strptime(end)
print(time.strftime("%Y/%m/%d %H:%M", endtime))