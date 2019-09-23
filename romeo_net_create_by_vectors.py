# Program writes the Intersection html for ROMEO simulator
import pandas as pd
import numpy as np


class PetriNet:
    def __init__(self):
        self.places = pd.DataFrame(columns=["name", "color", "x_pos", "y_pos", "M0", "id"])
        self.transitions = pd.DataFrame(columns=["name", "color", "x_pos", "y_pos", "time", "arcs_in", "arcs_out", "id"])
        self.arcs = []


def net_create():
    p_id = 1
    t_id = 1
    petri_net = PetriNet()

    p_names_sem = ['GG_', 'DG_', 'GR_', 'mG_', 'DY_', 'EG_', 'M_', 'SM_', 'RG_', 'RR_', 'FOS_']
    p_color_sem = [0, 3, 0, 0, 4, 0, 0, 0, 0, 5, 0]
    p_pos_x_sem = [0, 75, 150, 0, 150, 0, 75, 150, 0, 150, 75, 75, 75]
    p_pos_y_sem = [0, 30, 0, 60, 60, 120, 90, 120, 180, 180, 180]

    t_names_sem = ['t1_', 't2_', 'min_', 'Yel_', 'Max_', 'FO_', 'Act_', 't3_']
    all_red = 4
    t_time_sem = [0, 0, 20, 4, 100, 0, 50, 0]
    t_color_sem = [0, 0, 1, 1, 1, 0, 1, 0]
    t_pos_x_sem = [0, 150, 0, 150, -75, 0, 75, 150]
    t_pos_y_sem = [30, 30, 90, 90, 150, 150, 150, 150]

    pos_x_init = [121, 421, 721, 1021, 1321, 1621, 1921, 2221]
    pos_y_init = [4951, 4951, 4951, 4951, 4951, 4951, 4951, 4951]

    arcs_in = pd.Series(data=['GG_', ['DG_', 'GR_'], 'mG_', 'DY_', 'EG_', 'EG_', 'EG_', ['M_', 'SM_']],
                        index=t_names_sem)
    arcs_out = pd.Series(data=[['DG_', 'mG_', 'M_'], 'DY_', 'EG_', 'SM_', 'RG_', 'RG_', 'RG_', 'RR_'],
                         index=t_names_sem)

    directions = [0, 1, 2, 3, 4, 5, 6, 7]
    phases = [[0, 4], [0, 5], [1, 4], [1, 5], [2, 6], [2, 7], [3, 6], [3, 7]]
    cycle_normal_select = [1, 2, 3, 4, 5, 6, 7, 0]
    cycle_acc_a_select = [2, 2, 3, 4, 5, 2, 2, 2]
    cycle_acc_b_select = [1, 5, 0, 0, 0, 7, 0, 0]
    cycle_acc_c_select = [1, 3, 1, 4, 6, 1, 1, 1]
    cycle_acc_d_select = [2, 0, 6, 0, 0, 0, 7, 0]

    for x in directions:
        # Create Semaphore places
        for i in range(len(p_names_sem)):
            p_ident = p_names_sem[i] + str(x)
            petri_net.places = petri_net.places.append(
                {'name': p_ident, 'color': p_color_sem[i], "x_pos": p_pos_x_sem[i] + pos_x_init[x],
                 "y_pos": pos_y_init[x] - p_pos_y_sem[i], "M0": 0, "id": p_id}, ignore_index=True)
            p_id += 1

        # Create Semaphore transitions
        for i in range(len(t_names_sem)):
            t_ident = t_names_sem[i] + str(x)
            petri_net.transitions = petri_net.transitions.append(
                {'name': t_ident, 'color': t_color_sem[i], "x_pos": t_pos_x_sem[i] + pos_x_init[x],
                 "y_pos": pos_y_init[x] - t_pos_y_sem[i], "time": t_time_sem[i], "arcs_in": "", "arcs_out": "",
                 "id": t_id}, ignore_index=True)

            if isinstance(arcs_in[i], str):
                petri_net.transitions.at[t_id - 1, "arcs_in"] = arcs_in[i] + str(x)
            elif isinstance(arcs_in[i], list):
                arcs_in_t = list(arcs_in.iloc[i])
                for j in range(len(arcs_in_t)):
                    arcs_in_t[j] = arcs_in_t[j] + str(x)
                petri_net.transitions.at[t_id - 1, "arcs_in"] = arcs_in_t
            if isinstance(arcs_out[i], str):
                petri_net.transitions.at[t_id - 1, "arcs_out"] = arcs_out[i] + str(x)
            elif isinstance(arcs_out[i], list):
                arcs_out_t = list(arcs_out[i])
                for j in range(len(arcs_out_t)):
                    arcs_out_t[j] = arcs_out_t[j] + str(x)
                petri_net.transitions.at[t_id - 1, "arcs_out"] = arcs_out_t

            t_id += 1

    # Create Cycle change procces
    for x in range(len(phases)):#Start phase
        for i in range(len(phases)):#Golas phase
            if x != i:
                dir_start_list = phases[x]
                dir_goal_list = phases[i]

                p_ident = "C" + str(x) + str(i)
                petri_net.places = petri_net.places.append(
                    {'name': p_ident, 'color': 0, "x_pos": 75 + pos_x_init[x],
                     "y_pos": pos_y_init[x] - 270 - 120 * i, "M0": 0, "id": p_id}, ignore_index=True)
                p_id += 1

                if dir_start_list[0] in dir_goal_list:
                    goal = [y for y in dir_goal_list if y != dir_start_list[0]]
                    arcs_in_1 = ["DG_"+str(dir_start_list[0]),
                                 "RG_"+str(dir_start_list[1]),
                                 "RR_"+str(goal[0]),
                                 "S"+str(i)]
                    arcs_out_1 = ["DG_"+str(dir_start_list[0]),
                                  "GR_"+str(dir_start_list[1]),
                                  p_ident,
                                  "ST"]
                    arcs_in_2 = ["DG_"+str(dir_start_list[0]),
                                 "RR_"+str(dir_start_list[1]),
                                 p_ident]
                    arcs_out_2 = ["DG_" + str(dir_start_list[0]),
                                  "RR_" + str(dir_start_list[1]),
                                  "GG_" + str(goal[0])]
                elif dir_start_list[1] in dir_goal_list:
                    goal = [y for y in dir_goal_list if y != dir_start_list[0]]
                    arcs_in_1 = ["DG_" + str(dir_start_list[1]),
                                 "RG_" + str(dir_start_list[0]),
                                 "RR_" + str(goal[0]),
                                 "S"+str(i)]
                    arcs_out_1 = ["DG_" + str(dir_start_list[1]),
                                  "GR_" + str(dir_start_list[0]),
                                  p_ident,
                                  "ST"]
                    arcs_in_2 = ["DG_" + str(dir_start_list[1]),
                                 "RR_" + str(dir_start_list[0]),
                                 p_ident]
                    arcs_out_2 = ["DG_" + str(dir_start_list[1]),
                                  "RR_" + str(dir_start_list[0]),
                                  "GG_" + str(goal[0])]
                else:
                    arcs_in_1 = ["RG_" + str(dir_start_list[0]),
                                 "RG_" + str(dir_start_list[1]),
                                 "RR_" + str(dir_goal_list[0]),
                                 "RR_" + str(dir_goal_list[1]),
                                 "S"+str(i)]
                    arcs_out_1 = ["GR_" + str(dir_start_list[0]),
                                  "GR_" + str(dir_start_list[1]),
                                  p_ident,
                                  "ST"]
                    arcs_in_2 = ["RR_" + str(dir_start_list[0]),
                                 "RR_" + str(dir_start_list[1]),
                                 p_ident]
                    arcs_out_2 = ["RR_" + str(dir_start_list[0]),
                                  "RR_" + str(dir_start_list[1]),
                                  "GG_" + str(dir_goal_list[0]),
                                  "GG_" + str(dir_goal_list[1])]
                #print(arcs_in_1)
                t_ident = "t1" + str(x) + str(i)
                petri_net.transitions = petri_net.transitions.append(
                    {'name': t_ident, 'color': 0, "x_pos": 75 + pos_x_init[x],
                     "y_pos": pos_y_init[x] - 240 - 120 * i, "time": 0, "arcs_in": arcs_in_1, "arcs_out": arcs_out_1,
                     "id": t_id}, ignore_index=True)
                t_id += 1

                t_ident = "t2" + str(x) + str(i)
                petri_net.transitions = petri_net.transitions.append(
                    {'name': t_ident, 'color': 1, "x_pos": 75 + pos_x_init[x],
                     "y_pos": pos_y_init[x] - 300 - 120 * i, "time": all_red, "arcs_in": arcs_in_2, "arcs_out": arcs_out_2,
                     "id": t_id}, ignore_index=True)
                t_id += 1

        # Create Cycle change control x="2491" y="4681"
        p_ident = "S" + str(x)
        petri_net.places = petri_net.places.append(
            {'name': p_ident, 'color': 0, "x_pos": 2491,
             "y_pos": pos_y_init[x] - 270 - 120 * x, "M0": 0, "id": p_id}, ignore_index=True)
        p_id += 1

        arcs_in = ["Normal",
                   "ST"]
        for i in range(len(cycle_normal_select)):
            if cycle_normal_select[i] == x:
                for j in range(len(phases)):
                    if j != i:
                        arcs_in.append("C" + str(j) + str(i))

        arcs_out = ["Normal",
                    p_ident]
        t_ident = "tn" + str(x)
        petri_net.transitions = petri_net.transitions.append(
            {'name': t_ident, 'color': 0, "x_pos": 2491 + 60,
             "y_pos": pos_y_init[x] - 270 - 120 * x, "time": 0, "arcs_in": arcs_in, "arcs_out": arcs_out,
             "id": t_id}, ignore_index=True)
        t_id += 1

    p_ident = "Normal"
    petri_net.places = petri_net.places.append(
        {'name': p_ident, 'color': 0, "x_pos": 2491 + 180,
         "y_pos": pos_y_init[x] - 270 - 120 * 4, "M0": 1, "id": p_id}, ignore_index=True)
    p_id += 1
    p_ident = "ST"
    petri_net.places = petri_net.places.append(
        {'name': p_ident, 'color': 0, "x_pos": 2491 + 120,
         "y_pos": pos_y_init[x] - 270 - 120 * 4, "M0": 0, "id": p_id}, ignore_index=True)
    p_id += 1


    return petri_net, p_id, t_id


def net_graph(file_name, petri_net):
    file = open(file_name, "a")
    petri_net.places.set_index("name", inplace=True)
    petri_net.transitions.set_index("name", inplace=True)
    for i in list(petri_net.places.index.values):
        place = [
            ' <place id="%d" identifier="%s" label="%s" initialMarking="%d" eft="0" lft="inf">\n' % (
                petri_net.places.loc[i]["id"], i, i,petri_net.places.loc[i]["M0"]),
            '    <graphics color="%d">\n' % petri_net.places.loc[i]["color"],
            '       <position x="%d" y="%d"/>\n' % (
                petri_net.places.loc[i]["x_pos"], petri_net.places.loc[i]["y_pos"]),
            '       <deltaLabel deltax="10" deltay="10"/>\n',
            '    </graphics> \n',
            '    <scheduling gamma="0" omega="0"/> \n',
            ' </place> ]\n\n']
        file.writelines(place)
        # print(p_ids_array)

    for i in list(petri_net.transitions.index.values):
        transition = [
            ' <transition id="%d" identifier="%s" label="%s"  eft="%d" lft="inf" speed="1" cost="0" unctrl="0" obs="1"  guard="">\n' % (
                petri_net.transitions.loc[i]["id"], i,
                i, petri_net.transitions.loc[i]["time"]),
            '    <graphics color="%d">\n' % petri_net.transitions.loc[i]["color"],
            '       <position x="%d" y="%d"/>\n' % (petri_net.transitions.loc[i]["x_pos"], petri_net.transitions.loc[i]["y_pos"]),
            '       <deltaLabel deltax="25" deltay="0"/>\n',
            '       <deltaGuard deltax="20" deltay="-20"/>\n',
            '       <deltaUpdate deltax="20" deltay="10"/>\n',
            '       <deltaSpeed deltax="-20" deltay="5"/>\n',
            '       <deltaCost deltax="-20" deltay="5"/>\n',
            '    </graphics>\n',
            '    <update><![CDATA[]]></update>\n',
            ' </transition>\n\n']
        file.writelines(transition)

        if petri_net.transitions.loc[i]["arcs_in"] != "NaN":
            a_transition = petri_net.transitions.loc[i]["id"]
            if isinstance(petri_net.transitions.loc[i]["arcs_in"], str):
                a_place = petri_net.places.loc[petri_net.transitions.loc[i]["arcs_in"]]["id"]
                arc = [
                    '<arc place="%d" transition="%d" type="PlaceTransition" weight="1" inhibitingCondition ="">\n' % (
                        a_place, a_transition),
                    ' <nail xnail="0" ynail="0"/>\n',
                    ' <graphics color="0">\n',
                    ' </graphics>\n',
                    '</arc>\n\n\n', ]
                file.writelines(arc)
            elif isinstance(petri_net.transitions.loc[i]["arcs_in"], list):
                arcs_in_t = list(petri_net.transitions.loc[i]["arcs_in"])
                for j in range(len(arcs_in_t)):
                    a_place = petri_net.places.loc[arcs_in_t[j]]["id"]
                    arc = [
                        '<arc place="%d" transition="%d" type="PlaceTransition" weight="1" inhibitingCondition ="">\n' % (
                            a_place, a_transition),
                        ' <nail xnail="0" ynail="0"/>\n',
                        ' <graphics color="0">\n',
                        ' </graphics>\n',
                        '</arc>\n\n\n', ]
                    file.writelines(arc)

            if isinstance(petri_net.transitions.loc[i]["arcs_out"], str):
                a_place = petri_net.places.loc[petri_net.transitions.loc[i]["arcs_out"]]["id"]
                arc = [
                    '<arc place="%d" transition="%d" type="TransitionPlace" weight="1" inhibitingCondition ="">\n' % (
                        a_place, a_transition),
                    ' <nail xnail="0" ynail="0"/>\n',
                    ' <graphics color="0">\n',
                    ' </graphics>\n',
                    '</arc>\n\n\n', ]
                file.writelines(arc)
            elif isinstance(petri_net.transitions.loc[i]["arcs_out"], list):
                arcs_out_t = list(petri_net.transitions.loc[i]["arcs_out"])
                for j in range(len(arcs_out_t)):
                    a_place = petri_net.places.loc[arcs_out_t[j]]["id"]
                    arc = [
                        '<arc place="%d" transition="%d" type="TransitionPlace" weight="1" inhibitingCondition ="">\n' % (
                            a_place, a_transition),
                        ' <nail xnail="0" ynail="0"/>\n',
                        ' <graphics color="0">\n',
                        ' </graphics>\n',
                        '</arc>\n\n\n', ]

                    file.writelines(arc)
    file.close()
    return 0


fileName = "intersection2.xml"
file1 = open(fileName, "w")

InitHML = ['<?xml version="1.0" encoding="UTF-8" ?>\n',
           '<romeo version="Romeo v3.6.0"> </romeo>\n',
           '<TPN name="/home/jose/Desktop/UC/Investigación/PetriNets/romeo-3.6.0-linux/romeo-3.6.0/semaphore.xml">\n']
file1.writelines(InitHML)
file1.close()

petri_net, place_id, transition_id = net_create()
net_graph(fileName, petri_net)

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
