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

class Hola:
    def __init__(self):
        self.hi = 0
hola = Hola()
print(hola.hi)
hola.hi = [1, 2, 3]
print(hola.hi)

# creating a series
data = pd.Series([5, 2, 3, 7], index=['a', 'b', 'c', 'd'])
print(data['a'])

#Pandas series
data2 = pd.Series()
data2 = data2.append(pd.Series([5], index=['jose']))
data2 = data2.append(pd.Series([6], index=['jesi']))
print(data2)

#Lists
data3 = []
data3.append("jeje")
data3.append("jojo")
print(data3)

#Dictionaries
data4 = {}
data4["jaja"] = 5
data4["fomo"] = 6
print(data4)
print(data4["fomo"])

#Pandas dataframe
data5 = pd.DataFrame(columns=["name", "color", "x_pos", "y_pos", "id"])
data5 = data5.append({'name': 'Sahil', 'color': 2, "x_pos": 70, "y_pos": 0, "id": 1}, ignore_index=True)
data5 = data5.append({'name': 'Jose', 'color': 2, "x_pos": 75, "y_pos": 0, "id": 1}, ignore_index=True)
data5 = data5.append({'name': 'Jesi', 'color': 2, "x_pos": 80, "y_pos": 0, "id": 1}, ignore_index=True)
print(data5)
data5.set_index("name", inplace=True)
print(data5)
print(data5.loc["Jose"]["x_pos"])
print(list(data5.index.values))
data5.iloc[1]["x_pos"] = 1000
print(data5.iloc[1]["x_pos"])

hola = "*hola"
print(hola)
if "*" in hola:
    hola = hola.replace("*", "")
    print(hola)