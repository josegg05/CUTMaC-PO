# Program writes the Intersection html for ROMEO simulator
from cutmapnet.petri_nets import inter_tpn_pandas
from cutmapnet.petri_nets import romeo_graph
import pandas as pd

# def net_romeo_graph(file_name, petri_net):
#     file = open(file_name, "a")
#     #petri_net.places.set_index("name", inplace=True)
#     #petri_net.transitions.set_index("name", inplace=True)
#     for i in list(petri_net.places.index.values):
#         place = [
#             ' <place id="%d" identifier="%s" label="%s" initialMarking="%d" eft="0" lft="inf">\n' % (
#                 petri_net.places.loc[i]["id"], i, i, petri_net.places.loc[i]["M0"]),
#             '    <graphics color="%d">\n' % petri_net.places.loc[i]["color"],
#             '       <position x="%d" y="%d"/>\n' % (
#                 petri_net.places.loc[i]["x_pos"], petri_net.places.loc[i]["y_pos"]),
#             '       <deltaLabel deltax="10" deltay="10"/>\n',
#             '    </graphics> \n',
#             '    <scheduling gamma="0" omega="0"/> \n',
#             ' </place> ]\n\n']
#         file.writelines(place)
#         # print(p_ids_array)
#
#     for i in list(petri_net.transitions.index.values):
#         transition = [
#             ' <transition id="%d" identifier="%s" label="%s"  eft="%d" lft="inf" speed="1" cost="0" unctrl="0" obs="1"  guard="">\n' % (
#                 petri_net.transitions.loc[i]["id"], i,
#                 i, petri_net.transitions.loc[i]["time"]),
#             '    <graphics color="%d">\n' % petri_net.transitions.loc[i]["color"],
#             '       <position x="%d" y="%d"/>\n' % (
#             petri_net.transitions.loc[i]["x_pos"], petri_net.transitions.loc[i]["y_pos"]),
#             '       <deltaLabel deltax="25" deltay="0"/>\n',
#             '       <deltaGuard deltax="20" deltay="-20"/>\n',
#             '       <deltaUpdate deltax="20" deltay="10"/>\n',
#             '       <deltaSpeed deltax="-20" deltay="5"/>\n',
#             '       <deltaCost deltax="-20" deltay="5"/>\n',
#             '    </graphics>\n',
#             '    <update><![CDATA[]]></update>\n',
#             ' </transition>\n\n']
#         file.writelines(transition)
#
#         if petri_net.transitions.loc[i]["arcs_in"] != "NaN":
#             a_transition = petri_net.transitions.loc[i]["id"]
#             arcs_in_t = list(petri_net.transitions.loc[i]["arcs_in"])
#             for j in range(len(arcs_in_t)):
#                 if "*" in arcs_in_t[j]:
#                     arcs_in_t[j] = arcs_in_t[j].replace("*", "")
#                     type = "logicalInhibitor"
#                 else:
#                     type = "PlaceTransition"
#                 a_place = petri_net.places.loc[arcs_in_t[j]]["id"]
#                 arc = [
#                     '<arc place="%d" transition="%d" type="%s" weight="1" inhibitingCondition ="">\n' % (
#                         a_place, a_transition, type),
#                     ' <nail xnail="0" ynail="0"/>\n',
#                     ' <graphics color="0">\n',
#                     ' </graphics>\n',
#                     '</arc>\n\n\n', ]
#                 file.writelines(arc)
#
#             arcs_out_t = list(petri_net.transitions.loc[i]["arcs_out"])
#             for j in range(len(arcs_out_t)):
#                 a_place = petri_net.places.loc[arcs_out_t[j]]["id"]
#                 arc = [
#                     '<arc place="%d" transition="%d" type="TransitionPlace" weight="1">\n' % (
#                         a_place, a_transition),
#                     ' <nail xnail="0" ynail="0"/>\n',
#                     ' <graphics color="0">\n',
#                     ' </graphics>\n',
#                     '</arc>\n\n\n', ]
#                 file.writelines(arc)
#
#     file.close()
#     return 0


fileName = "results/intersection4.xml"
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

movements = [0, 1, 3, 4, 5, 7]
phases = [[3, 7], [0, 5], [0, 4], [1, 5]]
lights = [["rrrGGGG", "rrryyyy"], ["GGGrrrr", "yyyrrrr"], ["rrGrrrr", "rryrrrr"], ["GGrrrrr", "yyrrrrr"]]
cycles = pd.Series(data=[[3, 0, 0, 0],
                         [1, 0, 0, 0],
                         [2, 0, 0, 0]],
                   index=["Normal", "AccA", "AccB"])

petri_net, place_id, transition_id = inter_tpn_pandas.net_create(movements, phases, cycles)
romeo_graph.net_romeo_graph(fileName, petri_net)

print("palceID = " + str(place_id) + "\ntransitionID = " + str(transition_id))
print(petri_net.transitions)

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
