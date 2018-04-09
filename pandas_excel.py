import pandas as pd
import math
df_gen1 = pd.read_excel("プローブラベル変換形式_20180403.xlsx", sheet_name="Gen1（GDC1.0向け）", skiprows=3)
df_sxm = pd.read_excel("プローブラベル変換形式_20180403.xlsx", sheet_name="CARWINGS向け", skiprows=3)
#print(df)
lab_val = "0x"
lab_name = ""
lab_size = ""
df_gen1 = df_gen1.fillna({"ラベル値": 'no_lab_val', 'ラベル名': 'no_lab_name'})
df_sxm = df_sxm.fillna({"ラベル値": 'no_lab_val', 'ラベル名': 'no_lab_name'})
new_row = None
row_listg1 = []
row_listx = []
for index, row in df_gen1.iterrows():
    if row["ラベル値"] != "no_lab_val":
        if new_row is not None:
            row_listg1.append(new_row)
            #print(new_row)
        new_row = [row["ラベル値"], row["ラベル名"], row["Byte"]]
        #print(index, row["ラベル値"])
    else:
        new_row[2] += ";"+row["Byte"]
        #print(index, row["ラベル値"], row["Byte"])
row_listg1.append(new_row)
new_row = None
for index, row in df_sxm.iterrows():
    if row["ラベル値"] != "no_lab_val":
        if new_row is not None:
            row_listx.append(new_row)
            #print(new_row)
        new_row = [row["ラベル値"], row["ラベル名"], row["Byte"]]
        #print(index, row["ラベル値"])
    else:
        new_row[2] += ";"+row["Byte"]
        #print(index, row["ラベル値"], row["Byte"])
row_listx.append(new_row)
#print(row_listg1)
#print(row_listx)
for g1 in row_listg1:
    for x in row_listx:
        if g1[1] == x[1] and g1[1] != '未使用':
            print(g1)
            print(x)
