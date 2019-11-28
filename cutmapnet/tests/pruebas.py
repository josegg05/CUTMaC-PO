import numpy as np
import pandas as pd

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

pepe = "1234"
print(pepe[0])

# ******************************************************
# Pruebas TPN with SNAKE
# ******************************************************
from cutmapnet.petri_nets import tpn
import snakes.plugins
snakes.plugins.load(tpn, "snakes.nets", "snk")
from snk import *

n = PetriNet("stepper")

for i in range(3) :
    n.add_place(Place("p%s" % i, [dot]))
    n.add_transition(Transition("t%s" % i, min_time=i+1, max_time=i*2+1))
    n.add_input("p%s" % i, "t%s" % i, Value(dot))
init = n.get_marking()
print(init)
n.reset()
clock = 0.0
for i in range(3):
    print(" , ".join("%s[%s,%s]=%s"
                     % (t, t.min_time, t.max_time,
                        "#" if t.time is None else t.time)
                     for t in n.transition()))
    delay = n.time()
    print("[%s]" % clock, "delay:", delay)
    clock += delay
    print("[%s] fire: t%s" % (clock, i))
    n.transition("t%d" % i).fire(Substitution())

print("\n")
n.set_marking(init) # Acts like n.reset(), because each transition has a place in its pre-set whose marking is reset, just like for method reset
clock = 0.0
for i in range(3) :
    print(" , ".join("%s[%s,%s]=%s" % (t, t.min_time, t.max_time,
                                       "#" if t.time is None else t.time)
                     for t in n.transition()))
    for j in range(3) :
        delay = n.time()
        print("[%s]" % clock, "delay:", delay)
        clock += delay
    print("[%s] fire: t%s" % (clock, i))
    n.transition("t%s" % i).fire(Substitution())

# ******************************************************
# Pruebas graph with SNAKE
# ******************************************************

#from snakes.nets import *
import snakes.plugins
snakes.plugins.load("gv", "snakes.nets", "nets")
from nets import *

n = PetriNet('First net')
n.add_place(Place('p', [0]))
n.add_transition(Transition('t', Expression('x<5')))
n.add_input('p', 't', Variable('x'))
n.add_output('p', 't', Expression('x+1'))

modes = n.transition('t').modes()
print(modes)
#n.draw("value-0.png")

n.transition('t').fire(Substitution(x=0))
state = n.get_marking()
print(state)

#for engine in ('neato', 'dot', 'circo', 'twopi', 'fdp'):
#    n.draw(',test-gv-%s.png' % engine, engine=engine)

# Draw the PN and the state graph
n.draw("value-1.png")
s = StateGraph(n)
s.build()
s.draw('test-gv-graph.png')


# ******************************************************
# Pruebas time
# ******************************************************
import time

def procedure():
   time.sleep(2.5)

# measure process time
t0 = time.perf_counter()
procedure()
print(time.perf_counter()), "seconds process time"

# measure wall time
t0 = time.perf_counter()
procedure()
print(time.perf_counter() - t0), "seconds wall time"

# pruebas listas
lista = [["name", "color", "x_pos", "y_pos", "M0", "id"]]
print(lista)
lista.append([1, 2, 3, 4, 5, 6])
lista.append([1, 2, 3, 4, ["soy", "yo"], 6])
lista.append([1, 2, 3, 4, 5, 6])
print(lista)
print(lista[2][4])
print(len(lista))


# prueba 2 listas con los mismos elementos
pepe = [1, 2]
if set(pepe) == set([2, 1]):
    print("hola pepe")
else:
    pepe.append(5)


# List of list of lists
m_lights = [[[], [2], [], [], [5], [], [], [0, 1]],
            [[], [3], [], [], [5], [], [], [0, 1]],
            [[], [4], [], [], [5], [], [], [0, 1]],
            [[], [5], [], [], [5], [], [], [0, 1]]]
print(m_lights[3][1][0])

# Dictionary of dictionaries of dictionaries
dic = {
    1: {
        "neighbors": {
            "NORTH": "0005"
        }
    }
}

print(dic[1]["neighbors"]["NORTH"])


# If x is not None
variable = "hi"
if variable is not "":
    print("Is not ''. It : " + variable)
else:
    print("It is ''")


# String in a string
string = "hola/soy/Jose"
if "Jose" in string:
    print(f"Jose is in string {string}")


# 'f"{}"' string format
direction = "n"
print(f"Acc{direction.capitalize()}I_to_Normal")


# prueba np.sum
import numpy as np
vehicleNumber = []
vehicleNumber.append(2)
vehicleNumber.append(5)
vehicleNumber.append(3)
vehiNum = np.sum(vehicleNumber)
print(vehicleNumber)
print(vehiNum)

# del from list
moves = []
moves.append(1)
moves. append(5)
moves. append(7)
print(moves)
moves.remove(5)
print(moves)

# IF with OR, AND and IN:
hola = "tn_AccSI"
if (("tNormal" in hola) or ("tAcc" in hola)) and (hola[-1] not in ["n", "I", "O"]):
    print(hola)
hola = "tAccSI_n"
if (("tNormal" in hola) or ("tAcc" in hola)) and (hola[-1] not in ["n", "I", "O"]):
    print(hola)
hola = "tNormal012"
if (("tNormal" in hola) or ("tAcc" in hola)) and (hola[-1] not in ["n", "I", "O"]):
    print(hola)
hola = "tAccSI101"
if (("tNormal" in hola) or ("tAcc" in hola)) and (hola[-1] not in ["n", "I", "O"]):
    print(hola)

# copy()
moves_green = [1, 2]
MG = moves_green.copy()
MG.remove(1)
print(moves_green, MG)

# index
idx_list = ["Jose", "Jesi", "Mari"]
print(idx_list.index("Mar"))

# indexing dictionaries keys
ages = {"Jose": 29,
        "Jesi": 27,
        "Mari": 13}
print(list(ages.keys())[1])


for i in range(1,6):
    print(i)
