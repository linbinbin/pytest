#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
#@profile
def merge():
    dfs = pd.read_csv('bbig.csv', names=['A','B','C','D','E'])
    dfss = pd.read_csv('small.csv', names=['A','B','C','D','E'])
    result = dfs.append(dfss).drop_duplicates(subset=['A'], keep='last').sort_values(by='A')
    result.to_csv('bbig_op.csv',index=False, header=False)
#print(dfss)
#print(dfs)
#dfs.columns=['A','B','C','D','E']
#dfss.columns=['A','B','C','D','E']
#result = pd.concat([dfs, dfss], axis=0, ignore_index=True).drop_duplicates(subset=['A'], keep='last')
#print(result)
#dfs.append(dfss).drop_duplicates(subset=['A'], keep='last').to_csv('bbig_op.csv',index=False, header=False)
if __name__ == "__main__":
    merge()
