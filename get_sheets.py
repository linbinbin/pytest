# -*- coding: utf-8 -*-
"""
Get Excel SheetNames。
"""
from pathlib import Path
import openpyxl as px
import pandas as pd
import argparse

def get_sheetNames(xlsx):
    #fx = mypath.joinpath(xlsx)
    book = px.load_workbook(xlsx)
    print("Name: {}".format(xlsx))
    print("Sheets: {}".format(list(book.get_sheet_names())))
    return {xlsx: book.get_sheet_names()}

def mk_list(src, out):
    mypath = Path(src)
    listc = filter(lambda x: x.name.find('.xlsx') > 0, [mypath.joinpath(path.name) for path in mypath.iterdir()])
    msheets = map(get_sheetNames, listc)
    dummy = list(msheets)

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('src_dir', default='.', help='Source file directory')
    parser.add_argument('out_ret', default='output_file.csv', help='out put file name')
    
    cmd = parser.parse_args()

    mk_list(cmd.src_dir, cmd.out_ret) 
