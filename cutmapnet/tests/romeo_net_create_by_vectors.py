# Program writes the Intersection html for ROMEO simulator
from cutmapnet.petri_nets import inter_tpn
from cutmapnet.petri_nets import intersections_classes
from cutmapnet.petri_nets import romeo_graph
import pandas as pd


fileName = "results/intersection5.xml"
file1 = open(fileName, "w")

InitHML = ['<?xml version="1.0" encoding="UTF-8" ?>\n',
           '<romeo version="Romeo v3.6.0"> </romeo>\n',
           '<TPN name="/home/jose/Desktop/UC/Investigación/PetriNets/romeo-3.6.0-linux/romeo-3.6.0/semaphore.xml">\n']
file1.writelines(InitHML)
file1.close()

# movements = [0, 1, 2, 3, 4, 5, 6, 7]
# phases = [[0, 4], [0, 5], [1, 4], [1, 5], [2, 6], [2, 7], [3, 6], [3, 7]]
# cycles = pd.Series(data=[[1, 2, 3, 4, 5, 6, 7, 0],
#                          [2, 2, 3, 4, 5, 2, 2, 2],
#                          [1, 5, 0, 0, 0, 7, 0, 0],
#                          [1, 3, 1, 4, 6, 1, 1, 1],
#                          [2, 0, 6, 0, 0, 0, 7, 0]],
#                    index=["Normal", "AccA", "AccB", "AccC", "AccD"])

# movements = [0, 1, 3, 4, 5, 7]
# phases = [[3, 7], [0, 5], [0, 4], [1, 5]]
# lights = [["rrrGGGG", "rrryyyy"], ["GGGrrrr", "yyyrrrr"], ["rrGrrrr", "rryrrrr"], ["GGrrrrr", "yyrrrrr"]]
# cycles = pd.Series(data=[[3, 0, 0, 0],
#                          [1, 0, 0, 0],
#                          [2, 0, 0, 0]],
#                    index=["Normal", "AccA", "AccB"])
#
# petri_net, place_id, transition_id = inter_tpn_pandas.net_create(movements, phases, cycles)
# romeo_graph.net_romeo_graph(fileName, petri_net)

inter_id = 2
inter_info = intersections_classes.Intersection(inter_id)
inter_info.config()
petri_net_inter, place_id, transition_id = inter_tpn.net_create(inter_info.movements, inter_info.phases,
                                                                    inter_info.cycles, inter_info.cycles_names)
romeo_graph.net_romeo_graph(fileName, petri_net_inter)


print("palceID = " + str(place_id) + "\ntransitionID = " + str(transition_id))
print(petri_net_inter.transitions)

file1 = open(fileName, "a")
FinalHTML = [' <timedCost></timedCost>\n\n',
             ' <declaration><![CDATA[// insert here your type definitions using C-like syntax\n\n\n',
             '// insert here your function definitions\n',
             '// using C-like syntax]]></declaration>\n\n'
             ' <initialization><![CDATA[// insert here the state variables declarations\n',
             '// and possibly some code to initialize them\n',
             '// using C-like syntax\n',
             ']]></initialization>\n\n',
             ' <preferences>\n',
             '   <colorPlace  c0="SkyBlue2"  c1="gray"  c2="cyan"  c3="green"  c4="yellow"  c5="brown" />\n\n',
             '   <colorTransition  c0="yellow"  c1="gray"  c2="cyan"  c3="green"  c4="SkyBlue2"  c5="brown" />\n\n',
             '   <colorArc  c0="black"  c1="gray"  c2="blue"  c3="#beb760"  c4="#be5c7e"  c5="#46be90" />\n\n',
             ' </preferences>\n',
             '</TPN>\n\n']
file1.writelines(FinalHTML)
file1.close()
