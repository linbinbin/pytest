import pandas as pd
df = pd.read_csv('big.csv', index_col=None, encoding='utf-8')
df.columns = ['no', 'name', 'add', 'ran', 'date']
df.sort_values('no')
df.to_csv('big_o.csv')
