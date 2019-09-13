import pandas as pd
import numpy as np

colum = ['X', 'Y', 'Z']
df = pd.DataFrame(columns=colum)
a = np.zeros((len(colum),), dtype=np.int)
df2 = pd.DataFrame(data=[a], columns=colum)
print(df)
df = df.append(df2, ignore_index=True)
df = df.append(df2, ignore_index=True)
df = df.append(df2, ignore_index=True)
df.loc[2]['X'] = 10
df.loc[1]['X'] = 10
print(df)
print(a)
