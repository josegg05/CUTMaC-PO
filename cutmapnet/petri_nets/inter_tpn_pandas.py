# Program writes the Intersection html for ROMEO simulator
import pandas as pd


class PetriNetInfo:
    def __init__(self):
        self.places = pd.DataFrame(columns=["name", "color", "x_pos", "y_pos", "M0", "id"])
        self.transitions = pd.DataFrame(
            columns=["name", "color", "x_pos", "y_pos", "time", "arcs_in", "arcs_out", "id"])


def net_create(movements, phases, cycles):
    p_id = 1
    t_id = 1
    petri_net = PetriNetInfo()

    p_names_sem = ['GG_', 'DG_', 'GR_', 'mG_', 'DY_', 'EG_', 'M_', 'SM_', 'RG_', 'RR_', 'FOS_']
    p_color_sem = [0, 3, 0, 0, 4, 0, 0, 0, 0, 5, 0]
    p_pos_x_sem = [0, 75, 150, 0, 150, 0, 75, 150, 0, 150, 75, 75, 75]
    p_pos_y_sem = [0, 30, 0, 60, 60, 120, 90, 120, 180, 180, 180]

    #t_names_sem = ['t1_', 't2_', 'min_', 'Yel_', 'Max_', 'FO_', 'Act_', 't3_']
    t_names_sem = ['Green_', 'Yel_', 'min_', 'Stop_', 'Max_', 'FO_', 'Act_', 'Red_']
    all_red = 4
    t_time_sem = [0, 0, 20, 4, 100, 0, 50, 0]
    t_color_sem = [0, 0, 1, 1, 1, 0, 1, 0]
    t_pos_x_sem = [0, 150, 0, 150, -75, 0, 75, 150]
    t_pos_y_sem = [30, 30, 90, 90, 150, 150, 150, 150]

    pos_x_init = [121, 421, 721, 1021, 1321, 1621, 1921, 2221]
    pos_y_init = [4951, 4951, 4951, 4951, 4951, 4951, 4951, 4951]

    arcs_in = pd.Series(data=[['GG_'], ['DG_', 'GR_'], ['mG_'], ['DY_'], ['EG_'], ['EG_'], ['EG_'], ['M_', 'SM_']],
                        index=t_names_sem)
    arcs_out = pd.Series(data=[['DG_', 'mG_', 'M_'], ['DY_'], ['EG_'], ['SM_'], ['RG_'], ['RG_'], ['RG_'], ['RR_']],
                         index=t_names_sem)

    # movements = [0, 1, 2, 3, 4, 5, 6, 7]
    # phases = [[0, 4], [0, 5], [1, 4], [1, 5], [2, 6], [2, 7], [3, 6], [3, 7]]
    # cycles = pd.Series(data=[[1, 2, 3, 4, 5, 6, 7, 0],
    #                          [2, 2, 3, 4, 5, 2, 2, 2],
    #                          [1, 5, 0, 0, 0, 7, 0, 0],
    #                          [1, 3, 1, 4, 6, 1, 1, 1],
    #                          [2, 0, 6, 0, 0, 0, 7, 0]],
    #                    index=["Normal", "AccA", "AccB", "AccC", "AccD"])
    #m0_places = ["GG_0", "RR_1", "RR_2", "RR_3", "GG_4", "RR_5", "RR_6", "RR_7", "S1", "Normal"]
    m0_places = ["S1", "Normal"]
    for x in movements:
        if x in phases[0]:
            m_temp = "GG_" + str(x)
        else:
            m_temp = "RR_" + str(x)
        m0_places.append(m_temp)
    print(m0_places)

    # Create Semaphore
    for x in movements:
        # Create Semaphore places
        for i in range(len(p_names_sem)):
            p_ident = p_names_sem[i] + str(x)
            m0 = 0
            if p_ident in m0_places:
                m0 = 1
            petri_net.places = petri_net.places.append(
                {'name': p_ident, 'color': p_color_sem[i], "x_pos": p_pos_x_sem[i] + pos_x_init[x],
                 "y_pos": pos_y_init[x] - p_pos_y_sem[i], "M0": m0, "id": p_id}, ignore_index=True)
            p_id += 1

        # Create Semaphore transitions
        for i in range(len(t_names_sem)):
            t_ident = t_names_sem[i] + str(x)
            petri_net.transitions = petri_net.transitions.append(
                {'name': t_ident, 'color': t_color_sem[i], "x_pos": t_pos_x_sem[i] + pos_x_init[x],
                 "y_pos": pos_y_init[x] - t_pos_y_sem[i], "time": t_time_sem[i], "arcs_in": "", "arcs_out": "",
                 "id": t_id}, ignore_index=True)

            arcs_in_t = list(arcs_in.iloc[i])
            for j in range(len(arcs_in_t)):
                arcs_in_t[j] = arcs_in_t[j] + str(x)
            petri_net.transitions.at[t_id - 1, "arcs_in"] = arcs_in_t
            # if isinstance(arcs_out[i], str):
            arcs_out_t = list(arcs_out[i])
            for j in range(len(arcs_out_t)):
                arcs_out_t[j] = arcs_out_t[j] + str(x)
            petri_net.transitions.at[t_id - 1, "arcs_out"] = arcs_out_t

            t_id += 1

    phase_changes = []
    for x in range(len(phases)):
        for i in list(cycles.index.values):
            if ("C" + str(x) + str(cycles[i][x])) not in phase_changes:
                phase_changes.append("C" + str(x) + str(cycles[i][x]))

    print("Move Changes: " + str(phase_changes))
    # Create Cycle change procces
    for x in range(len(phases)):  # Start phase
        for i in range(len(phases)):  # Golas phase
            #if x != i:
            if ("C" + str(x) + str(i)) in phase_changes:
                #print("C" + str(x) + str(i))
                dir_start_list = phases[x]
                dir_goal_list = phases[i]

                p_ident = "C" + str(x) + str(i)
                m0 = 0
                if p_ident in m0_places:
                    m0 = 1
                petri_net.places = petri_net.places.append(
                    {'name': p_ident, 'color': 0, "x_pos": 75 + pos_x_init[x],
                     "y_pos": pos_y_init[x] - 270 - 120 * i, "M0": m0, "id": p_id}, ignore_index=True)
                p_id += 1

                if dir_start_list[0] in dir_goal_list:
                    goal = [y for y in dir_goal_list if y != dir_start_list[0]]
                    arcs_in_1 = ["DG_" + str(dir_start_list[0]),
                                 "RG_" + str(dir_start_list[1]),
                                 "RR_" + str(goal[0]),
                                 "S" + str(i)]
                    arcs_out_1 = ["DG_" + str(dir_start_list[0]),
                                  "GR_" + str(dir_start_list[1]),
                                  p_ident,
                                  "ST"]
                    arcs_in_2 = ["DG_" + str(dir_start_list[0]),
                                 "RR_" + str(dir_start_list[1]),
                                 p_ident]
                    arcs_out_2 = ["DG_" + str(dir_start_list[0]),
                                  "RR_" + str(dir_start_list[1]),
                                  "GG_" + str(goal[0])]
                elif dir_start_list[1] in dir_goal_list:
                    goal = [y for y in dir_goal_list if y != dir_start_list[0]]
                    arcs_in_1 = ["DG_" + str(dir_start_list[1]),
                                 "RG_" + str(dir_start_list[0]),
                                 "RR_" + str(goal[0]),
                                 "S" + str(i)]
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
                                 "S" + str(i)]
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
                # print(arcs_in_1)
                t_ident = "t1" + str(x) + str(i)
                petri_net.transitions = petri_net.transitions.append(
                    {'name': t_ident, 'color': 0, "x_pos": 75 + pos_x_init[x],
                     "y_pos": pos_y_init[x] - 240 - 120 * i, "time": 0, "arcs_in": arcs_in_1, "arcs_out": arcs_out_1,
                     "id": t_id}, ignore_index=True)
                t_id += 1

                t_ident = "t2" + str(x) + str(i)
                petri_net.transitions = petri_net.transitions.append(
                    {'name': t_ident, 'color': 1, "x_pos": 75 + pos_x_init[x],
                     "y_pos": pos_y_init[x] - 300 - 120 * i, "time": all_red, "arcs_in": arcs_in_2,
                     "arcs_out": arcs_out_2,
                     "id": t_id}, ignore_index=True)
                t_id += 1

        # Create Cycle change control x="2491" y="4681"
        p_ident = "S" + str(x)
        m0 = 0
        if p_ident in m0_places:
            m0 = 1
        petri_net.places = petri_net.places.append(
            {'name': p_ident, 'color': 0, "x_pos": 2491,
             "y_pos": pos_y_init[x] - 270 - 120 * x, "M0": m0, "id": p_id}, ignore_index=True)
        p_id += 1

        count = -2
        for i in range(len(phases)):
            for y in range(len(cycles)):
                if cycles[y][i] == x:
                    count += 2
                    for j in range(len(phases)):
                        if j != i and ("C" + str(j) + str(i)) in phase_changes:
                            arcs_in = [cycles.index.values[y], "ST", "C" + str(j) + str(i)]
                            arcs_out = [cycles.index.values[y], p_ident, "C" + str(j) + str(i)]
                            delay = 1  # para que ocurra la trasición que apaga el DG
                            t_ident = "t" + cycles.index.values[y] + str(j) + str(i) + str(x)
                            petri_net.transitions = petri_net.transitions.append(
                                {'name': t_ident, 'color': 0, "x_pos": 2491 + 60 + j,
                                 "y_pos": pos_y_init[x] - count - 240 - 15*y - 120 * x, "time": 1, "arcs_in": arcs_in,
                                 "arcs_out": arcs_out,
                                 "id": t_id}, ignore_index=True)
                            t_id += 1

    #Create Cycle types annd accident controls
    for i in range(len(cycles)):
        p_ident = cycles.index.values[i]
        m0 = 0
        if p_ident == "Normal":
            m0 = 1
            petri_net.places = petri_net.places.append(
                {'name': p_ident, 'color': 0, "x_pos": 2491 + 180,
                 "y_pos": pos_y_init[x] - 270 - 120 * i, "M0": m0, "id": p_id}, ignore_index=True)
            p_id += 1
        else:
            petri_net.places = petri_net.places.append(
                {'name': p_ident, 'color': 0, "x_pos": 2491 + 180,
                 "y_pos": pos_y_init[x] - 270 - 120 * i, "M0": m0, "id": p_id}, ignore_index=True)
            p_id += 1
            p_ident2 = p_ident + "_to_Normal"
            petri_net.places = petri_net.places.append(
                {'name': p_ident2, 'color': 0, "x_pos": 2491 + 180 + 90,
                 "y_pos": pos_y_init[x] - 210 - 120 * i, "M0": m0, "id": p_id}, ignore_index=True)
            p_id += 1
            p_ident3 = "Normal_to_" + p_ident
            petri_net.places = petri_net.places.append(
                {'name':p_ident3, 'color': 0, "x_pos": 2491 + 180 + 210,
                 "y_pos": pos_y_init[x] - 210 - 120 * i, "M0": m0, "id": p_id}, ignore_index=True)
            p_id += 1

            arcs_in_control = [["*Normal"], [p_ident2, p_ident], ["Normal", p_ident3], ["*" +  p_ident]]
            arcs_out_control = [[p_ident2], ["Normal"], [p_ident], [p_ident3]]
            t_control_names = ["t_no_"+p_ident, "tn_"+p_ident, "t"+p_ident+"_n", "t_" + p_ident]
            for j in range(len(t_control_names)):
                arcs_in = arcs_in_control[j]
                arcs_out = arcs_out_control[j]
                t_ident = t_control_names[j]
                petri_net.transitions = petri_net.transitions.append(
                    {'name': t_ident, 'color': 0, "x_pos": 2491 + 180 + 60 + j*60,
                     "y_pos": pos_y_init[x] - 210 - 120 * i, "time": 0, "arcs_in": arcs_in,
                     "arcs_out": arcs_out,
                     "id": t_id}, ignore_index=True)
                t_id += 1

    p_ident = "ST"
    m0 = 0
    if p_ident in m0_places:
        m0 = 1
    petri_net.places = petri_net.places.append(
        {'name': p_ident, 'color': 0, "x_pos": 2491 + 120,
         "y_pos": pos_y_init[x] - 210 - 120 * 4, "M0": m0, "id": p_id}, ignore_index=True)
    p_id += 1

    petri_net.places.set_index("name", inplace=True)
    petri_net.transitions.set_index("name", inplace=True)
    return petri_net, p_id, t_id