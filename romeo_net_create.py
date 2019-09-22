# Program writes the Intersection html for ROMEO simulator
import pandas as pd
import numpy as np


def semaphore_create(place_id, transition_id, file_name):
    file = open(file_name, "a")
    p_id = place_id
    t_id = transition_id

    p_names = ['GG_', 'DG_', 'GR_', 'mG_', 'DY_', 'EG_', 'M_', 'SM_', 'RG_', 'RR_', 'FOS_', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8']
    p_ids_array = pd.DataFrame(columns=p_names)
    p_color = [0, 3, 0, 0, 4, 0, 0, 0, 0, 5, 0]
    p_pos_x = [0, 75, 150, 0, 150, 0, 75, 150, 0, 150, 75, 75, 75]
    p_pos_y = [0, 30, 0, 60, 60, 120, 90, 120, 180, 180, 180]

    t_names = ['t1_', 't2_', 'min_', 'Yel_', 'Max_', 'FO_', 'Act_', 't3_', 't11', 't21', 't12', 't22', 't13', 't23', 't14', 't24', 't15', 't25', 't16', 't26', 't17', 't27', 't18', 't28']
    t_ids_array = pd.DataFrame(columns=t_names)
    all_red = 4
    t_time = [0, 0, 20, 4, 100, 0, 50, 0, 0, all_red, 0, all_red, 0, all_red, 0, all_red, 0, all_red, 0, all_red, 0, all_red, 0, all_red ]
    t_color = [0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
    t_pos_x = [0, 150, 0, 150, -75, 0, 75, 150, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75]
    t_pos_y = [30, 30, 90, 90, 150, 150, 150, 150]

    pos_x_init = [121, 421, 721, 1021, 1321, 1621, 1921, 2221]
    pos_y_init = [4951, 4951, 4951, 4951, 4951, 4951, 4951, 4951]

    arcs_in = pd.Series(data=['GG_', ['DG_', 'GR_'], 'mG_', 'DY_', 'EG_', 'EG_', 'EG_', ['M_', 'SM_']], index=t_names)
    arcs_out = pd.Series(data=[['DG_', 'mG_', 'M_'], 'DY_', 'EG_', 'SM_', 'RG_', 'RG_', 'RG_', 'RR_'], index=t_names)

    #print(arcs_in)
    #print(arcs_out)
    #print(len(arcs_in))
    #print(type(arcs_out[1]))
    for x in range(len(pos_x_init)):
        # Create Semaphore places
        a = np.zeros((len(p_names),), dtype=np.int)
        df = pd.DataFrame(data=[a], columns=p_names)
        p_ids_array = p_ids_array.append(df, ignore_index=True)
        for i in range(len(p_names)):
            p_ident = p_names[i] + str(x)
            place = [' <place id="%d" identifier="%s" label="%s" initialMarking="0" eft="0" lft="inf">\n' % (
                p_id, p_ident, p_ident),
                     '    <graphics color="%d">\n' % p_color[i],
                     '       <position x="%d" y="%d"/>\n' % (p_pos_x[i] + pos_x_init[x], pos_y_init[x] - p_pos_y[i]),
                     '       <deltaLabel deltax="10" deltay="10"/>\n',
                     '    </graphics> \n',
                     '    <scheduling gamma="0" omega="0"/> \n',
                     ' </place> ]\n\n']
            p_ids_array.loc[x][p_names[i]] = p_id
            p_id += 1
            file.writelines(place)
        # print(p_ids_array)

        # Create Semaphore transitions
        a = np.zeros((len(t_names),), dtype=np.int)
        df = pd.DataFrame(data=[a], columns=t_names)
        t_ids_array = t_ids_array.append(df, ignore_index=True)
        for i in range(len(t_names)):
            t_ident = t_names[i] + str(x)
            transition = [
                ' <transition id="%d" identifier="%s" label="%s"  eft="%d" lft="inf" speed="1" cost="0" unctrl="0" obs="1"  guard="">\n' % (
                    t_id, t_ident, t_ident, t_time[i]),
                '    <graphics color="%d">\n' % t_color[i],
                '       <position x="%d" y="%d"/>\n' % (t_pos_x[i] + pos_x_init[x], pos_y_init[x] - t_pos_y[i]),
                '       <deltaLabel deltax="25" deltay="0"/>\n',
                '       <deltaGuard deltax="20" deltay="-20"/>\n',
                '       <deltaUpdate deltax="20" deltay="10"/>\n',
                '       <deltaSpeed deltax="-20" deltay="5"/>\n',
                '       <deltaCost deltax="-20" deltay="5"/>\n',
                '    </graphics>\n',
                '    <update><![CDATA[]]></update>\n',
                ' </transition>\n\n']
            t_ids_array.loc[x][t_names[i]] = t_id
            t_id += 1
            file.writelines(transition)

        #Create Cycles change places and transitions
        #for i in range(len(pos_x_init)):
         #   if i != x:


        for i in range(len(t_names)):
            if isinstance(arcs_in[i], str):
                a_place = p_ids_array.loc[x][arcs_in[i]]
                a_transition = t_ids_array.loc[x][t_names[i]]
                arc = [
                    '<arc place="%d" transition="%d" type="PlaceTransition" weight="1" inhibitingCondition ="">\n' % (
                        a_place, a_transition),
                    ' <nail xnail="0" ynail="0"/>\n',
                    ' <graphics color="0">\n',
                    ' </graphics>\n',
                    '</arc>\n\n\n', ]
                file.writelines(arc)
            elif isinstance(arcs_in[i], list):
                arcs_in_t = arcs_in[i]
                for j in range(len(arcs_in_t)):
                    a_place = p_ids_array.loc[x][arcs_in_t[j]]
                    a_transition = t_ids_array.loc[x][t_names[i]]
                    arc = [
                        '<arc place="%d" transition="%d" type="PlaceTransition" weight="1" inhibitingCondition ="">\n' % (
                            a_place, a_transition),
                        ' <nail xnail="0" ynail="0"/>\n',
                        ' <graphics color="0">\n',
                        ' </graphics>\n',
                        '</arc>\n\n\n', ]
                    file.writelines(arc)

            if isinstance(arcs_out[i], str):
                a_place = p_ids_array.loc[x][arcs_out[i]]
                a_transition = t_ids_array.loc[x][t_names[i]]
                arc = [
                    '<arc place="%d" transition="%d" type="TransitionPlace" weight="1" inhibitingCondition ="">\n' % (
                        a_place, a_transition),
                    ' <nail xnail="0" ynail="0"/>\n',
                    ' <graphics color="0">\n',
                    ' </graphics>\n',
                    '</arc>\n\n\n', ]
                file.writelines(arc)
            elif isinstance(arcs_out[i], list):
                arcs_out_t = arcs_out[i]
                for j in range(len(arcs_out_t)):
                    a_place = p_ids_array.loc[x][arcs_out_t[j]]
                    a_transition = t_ids_array.loc[x][t_names[i]]
                    arc = [
                        '<arc place="%d" transition="%d" type="TransitionPlace" weight="1" inhibitingCondition ="">\n' % (
                            a_place, a_transition),
                        ' <nail xnail="0" ynail="0"/>\n',
                        ' <graphics color="0">\n',
                        ' </graphics>\n',
                        '</arc>\n\n\n', ]

                    file.writelines(arc)

    file1.close()
    return p_id, t_id


fileName = "intersection.xml"
file1 = open(fileName, "w")

InitHML = ['<?xml version="1.0" encoding="UTF-8" ?>\n',
           '<romeo version="Romeo v3.6.0"> </romeo>\n',
           '<TPN name="/home/jose/Desktop/UC/Investigación/PetriNets/romeo-3.6.0-linux/romeo-3.6.0/semaphore.xml">\n']
file1.writelines(InitHML)
file1.close()

placeID = 1
transitionID = 1

placeID, transitionID = semaphore_create(placeID, transitionID, fileName)
print("palceID = " + str(placeID) + "\ntransitionID = " + str(transitionID))

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
