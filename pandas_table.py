
# coding: utf-8

# In[ ]:

# この表をとってきます。
import pandas as pd
_data = pd.read_html('https://ja.wikipedia.org/wiki/%E7%B5%8C%E6%B8%88%E5%8D%94%E5%8A%9B%E9%96%8B%E7%99%BA%E6%A9%9F%E6%A7%8B')
print('_dataは {}\n要素は {}\n長さは{}'.format( type(_data), type(_data[0]), len(_data) ))
# 戻り値のリストの2つ目に目的の表が入っています。
print(type(_data[1]))
_data[1]# 整形しましょう。
# 表の本体(数値データ部分）のDataFrameを切り出す
data = _data[1].loc[1:,1:] 

# 列名（最初の1行）を付ける
data.columns = _data[1].loc[0,1:] 

# 行の名前（index）を付ける（valuesにしなくてもOK）
data.index = _data[1].loc[1:,0].values 
print(data)

