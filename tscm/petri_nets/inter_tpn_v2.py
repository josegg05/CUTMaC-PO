# Program creates all vectors of a intersection timed petri net


class PetriNetInfo:
    def __init__(self):
        self.places = [["name", "color", "x_pos", "y_pos", "M0", "id"]]
        self.transitions = [["name", "color", "x_pos", "y_pos", "min_time ", "max_time", "arcs_in", "arcs_out", "id"]]


def net_create(movements, phases, cycles, cycles_names):
    p_id = 1
    t_id = 1
    petri_net = PetriNetInfo()

    p_names_sem = ['GG_', 'DG_', 'GR_', 'mG_', 'DY_', 'EG_', 'M_', 'SM_', 'RG_', 'RR_']#, 'FOS_']
    p_color_sem = [0, 3, 0, 0, 4, 0, 0, 0, 0, 5]#, 0]<
    p_pos_x_sem = [0, 75, 150, 0, 150, 0, 75, 150, 0, 150, 75, 75]#, 75]
    p_pos_y_sem = [0, 30, 0, 60, 60, 120, 90, 120, 180, 180,]# 180]

    t_names_sem = ['tGreen_', 'tYel_', 'tmin_', 'tStop_', 'tMax_', 'tFO_', 'tAct_', 'tRed_']
    all_red = 2
    t_min_time_sem = [0, 0, 4, 3, 200, 300, 16, 0]  # time of tAct is the same as initial time of Movement objects
    t_max_time_sem = [None, None, 4, 3, 200, 300, 100, None]
    t_color_sem = [0, 0, 1, 1, 1, 0, 1, 0]
    t_pos_x_sem = [0, 150, 0, 150, -75, 0, 75, 150]
    t_pos_y_sem = [30, 30, 90, 90, 150, 150, 150, 150]

    arcs_in_sem = [['GG_'], ['DG_', 'GR_'], ['mG_'], ['DY_'], ['EG_'], ['EG_'], ['EG_'], ['M_', 'SM_']]
    arcs_out_sem = [['DG_', 'mG_', 'M_'], ['DY_'], ['EG_'], ['SM_'], ['RG_'], ['RG_'], ['RG_'], ['RR_']]

    pos_x_init = [121, 421, 721, 1021, 1321, 1621, 1921, 2221]
    pos_y_init = [4951, 4951, 4951, 4951, 4951, 4951, 4951, 4951]

    phases_list = [[0, 4], [0, 5], [1, 4], [1, 5], [2, 6], [2, 7], [3, 6], [3, 7]]
    phases_refactor = {}
    for ph_idx in range(len(phases)):
        phases_refactor[ph_idx] = phases_list.index(phases[ph_idx])

    m0_places = ["P" + str(phases_refactor[cycles[0][0]]), "Normal"]
    for mov in movements:
        if mov in phases[0]:
            m_temp = "GG_" + str(mov)
        else:
            m_temp = "RR_" + str(mov)
        m0_places.append(m_temp)
    print(m0_places)

    # Create IDM
    for mov in movements:
        # Create Semaphore places
        for p_idx in range(len(p_names_sem)):
            p_ident = p_names_sem[p_idx] + str(mov)
            m0 = 0
            if p_ident in m0_places:
                m0 = 1
            petri_net.places.append(
                [p_ident, p_color_sem[p_idx], p_pos_x_sem[p_idx] + pos_x_init[mov],
                 pos_y_init[mov] - p_pos_y_sem[p_idx], m0, p_id])
            p_id += 1

        # Create Semaphore transitions
        for t_idx in range(len(t_names_sem)):
            t_ident = t_names_sem[t_idx] + str(mov)
            petri_net.transitions.append(
                [t_ident, t_color_sem[t_idx], t_pos_x_sem[t_idx] + pos_x_init[mov],
                 pos_y_init[mov] - t_pos_y_sem[t_idx], t_min_time_sem[t_idx], t_max_time_sem[t_idx], "", "",
                 t_id])

            arcs_in_t = list(arcs_in_sem[t_idx])
            for acr_idx in range(len(arcs_in_t)):
                arcs_in_t[acr_idx] = arcs_in_t[acr_idx] + str(mov)
            petri_net.transitions[t_id][6] = arcs_in_t  # "arcs_in"

            arcs_out_t = list(arcs_out_sem[t_idx])
            for acr_idx in range(len(arcs_out_t)):
                arcs_out_t[acr_idx] = arcs_out_t[acr_idx] + str(mov)
            petri_net.transitions[t_id][7] = arcs_out_t  # "arcs_out"

            t_id += 1

    # Create PTM & ACRM
    phase_changes_pairs = []
    for ph_idx in range(len(phases)):
        for cy_idx in range(len(cycles)):
            if [ph_idx, cycles[cy_idx][ph_idx]] not in phase_changes_pairs:
                phase_changes_pairs.append([ph_idx, cycles[cy_idx][ph_idx]])

    phase_changes = []
    for ph_pair in phase_changes_pairs:
        phase_changes.append("C_" + str(phases_refactor[ph_pair[0]]) + str(phases_refactor[ph_pair[1]]))

    print("Move Changes: " + str(phase_changes))
    # Create Cycle change process
    for ph_idx in range(len(phases_list)):  # Start phase
        for ph_idx_goal in range(len(phases_list)):  # Golas phase
            # if x != i:
            if ("C_" + str(ph_idx) + str(ph_idx_goal)) in phase_changes:
                # print("C_" + str(x) + str(ph_idx_goal))
                dir_start_list = phases_list[ph_idx]
                dir_goal_list = phases_list[ph_idx_goal]

                p_ident = "C_" + str(ph_idx) + str(ph_idx_goal)
                m0 = 0
                if p_ident in m0_places:
                    m0 = 1
                petri_net.places.append(
                    [p_ident, 0, 75 + pos_x_init[ph_idx],
                     pos_y_init[ph_idx] - 270 - 120 * ph_idx_goal, m0, p_id])
                p_id += 1

                if dir_start_list[0] in dir_goal_list:
                    goal = [y for y in dir_goal_list if y != dir_start_list[0]]
                    arcs_in_1 = ["DG_" + str(dir_start_list[0]),
                                 "RG_" + str(dir_start_list[1]),
                                 "RR_" + str(goal[0]),
                                 "P" + str(ph_idx_goal)]
                    arcs_out_1 = ["DG_" + str(dir_start_list[0]),
                                  "GR_" + str(dir_start_list[1]),
                                  p_ident,
                                  "PTC"]
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
                                 "P" + str(ph_idx_goal)]
                    arcs_out_1 = ["DG_" + str(dir_start_list[1]),
                                  "GR_" + str(dir_start_list[0]),
                                  p_ident,
                                  "PTC"]
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
                                 "P" + str(ph_idx_goal)]
                    arcs_out_1 = ["GR_" + str(dir_start_list[0]),
                                  "GR_" + str(dir_start_list[1]),
                                  p_ident,
                                  "PTC"]
                    arcs_in_2 = ["RR_" + str(dir_start_list[0]),
                                 "RR_" + str(dir_start_list[1]),
                                 p_ident]
                    arcs_out_2 = ["RR_" + str(dir_start_list[0]),
                                  "RR_" + str(dir_start_list[1]),
                                  "GG_" + str(dir_goal_list[0]),
                                  "GG_" + str(dir_goal_list[1])]
                # print(arcs_in_1)
                t_ident = "t1_" + str(ph_idx) + str(ph_idx_goal)
                petri_net.transitions.append(
                    [t_ident, 0, 75 + pos_x_init[ph_idx],
                     pos_y_init[ph_idx] - 240 - 120 * ph_idx_goal, 0, None, arcs_in_1, arcs_out_1,
                     t_id])
                t_id += 1

                t_ident = "t2_" + str(ph_idx) + str(ph_idx_goal)
                petri_net.transitions.append(
                    [t_ident, 1, 75 + pos_x_init[ph_idx],
                     pos_y_init[ph_idx] - 300 - 120 * ph_idx_goal, all_red, all_red, arcs_in_2, arcs_out_2,
                     t_id])
                t_id += 1

        # Create Phases automatic change places. (x="2491" y="4681")
        p_ident = "P" + str(ph_idx)
        m0 = 0
        if p_ident in m0_places:
            m0 = 1
        petri_net.places.append(
            [p_ident, 0, 2491,
             pos_y_init[ph_idx] - 270 - 120 * ph_idx, m0, p_id])
        p_id += 1

        # Create Phases automatic change transitions
        count = -2
        for ph_idx_prev in range(len(phases)):
            for cy_idx in range(len(cycles)):
                if phases_refactor[cycles[cy_idx][ph_idx_prev]] == ph_idx:
                    count += 2
                    for ph_idx_prev_prev in range(len(phases)):
                        if ph_idx_prev_prev != ph_idx_prev and ("C_" + str(phases_refactor[ph_idx_prev_prev]) +
                                                                str(phases_refactor[ph_idx_prev])) in phase_changes:
                            arcs_in = [cycles_names[cy_idx], "PTC", "C_" + str(phases_refactor[ph_idx_prev_prev]) +
                                       str(phases_refactor[ph_idx_prev])]
                            arcs_out = [cycles_names[cy_idx], p_ident, "C_" + str(phases_refactor[ph_idx_prev_prev]) +
                                        str(phases_refactor[ph_idx_prev])]
                            delay = 1  # para que ocurra la trasición que apaga el DG
                            t_ident = "t" + cycles_names[cy_idx] + str(phases_refactor[ph_idx_prev_prev]) + \
                                      str(phases_refactor[ph_idx_prev]) + str(ph_idx)
                            petri_net.transitions.append(
                                [t_ident, 0, 2491 + 60 + ph_idx_prev_prev,
                                 pos_y_init[ph_idx] - count - 240 - 15 * cy_idx - 120 * ph_idx, delay, delay, arcs_in,
                                 arcs_out, t_id])
                            t_id += 1

    # Create PTC
    p_ident = "PTC"
    m0 = 0
    if p_ident in m0_places:
        m0 = 1
    petri_net.places.append(
        [p_ident, 0, 2491 + 120,
         pos_y_init[ph_idx] - 210 - 120 * 4, m0, p_id])
    p_id += 1

    # Create ACRMMext
    # for i in range(len(cycles)):
    #     p_ident = cycles_names[i]
    #     m0 = 0
    #     if p_ident == "Normal":
    #         m0 = 1
    #         petri_net.places.append(
    #             [p_ident, 0, 2491 + 180,
    #              pos_y_init[x] - 270 - 120 * i, m0, p_id])
    #         p_id += 1
    #     else:
    #         petri_net.places.append(
    #             [p_ident, 0, 2491 + 180,
    #              pos_y_init[x] - 270 - 120 * i, m0, p_id])
    #         p_id += 1
    #         p_ident2 = p_ident + "_to_Normal"
    #         petri_net.places.append(
    #             [p_ident2, 0, 2491 + 180 + 90,
    #              pos_y_init[x] - 210 - 120 * i, m0, p_id])
    #         p_id += 1
    #         p_ident3 = "Normal_to_" + p_ident
    #         petri_net.places.append(
    #             [p_ident3, 0, 2491 + 180 + 210,
    #              pos_y_init[x] - 210 - 120 * i, m0, p_id])
    #         p_id += 1
    #
    #         arcs_in_control = [["*Normal"], [p_ident2, p_ident], ["Normal", p_ident3], ["*" + p_ident]]
    #         arcs_out_control = [[p_ident2], ["Normal"], [p_ident], [p_ident3]]
    #         t_control_names = ["t_no_" + p_ident, "t" + p_ident + "_Normal", "tNormal_" + p_ident, "t_" + p_ident]
    #         for j in range(len(t_control_names)):
    #             arcs_in = arcs_in_control[j]
    #             arcs_out = arcs_out_control[j]
    #             t_ident = t_control_names[j]
    #             petri_net.transitions.append(
    #                 [t_ident, 0, 2491 + 180 + 60 + j * 60,
    #                  pos_y_init[x] - 210 - 120 * i, 0, None, arcs_in, arcs_out,
    #                  t_id])
    #             t_id += 1
    # Create Cycle types and accident controls
    for cy_idx in range(len(cycles_names)):
        p_ident = cycles_names[cy_idx]
        m0 = 0
        if p_ident == "Normal":
            m0 = 1
        petri_net.places.append(
            [p_ident, 0, 2491 + 180,
             pos_y_init[ph_idx] - 270 - 120 * cy_idx, m0, p_id])
        p_id += 1
        m0 = 0
        p_ident2 = "C" + p_ident  # "_to_Normal"
        petri_net.places.append(
            [p_ident2, 0, 2491 + 180 + 120,
             pos_y_init[ph_idx] - 270 - 120 * cy_idx, m0, p_id])
        p_id += 1

        t_ident = "tE" + p_ident
        petri_net.transitions.append(
            [t_ident, 0, 2491 + 180 + 180,
             pos_y_init[ph_idx] - 270 - 120 * cy_idx, 0, None, [], [p_ident2],
             t_id])
        t_id += 1

        for cy_idx_goal in range(len(cycles_names)):
            p_ident3 = cycles_names[cy_idx_goal]
            if p_ident3 is not p_ident:
                arcs_in = [p_ident2, p_ident3]
                arcs_out = [p_ident]
                t_ident = "tC" + p_ident + "_" + p_ident3
                petri_net.transitions.append(
                    [t_ident, 0, 2491 + 180 + 60,
                     pos_y_init[ph_idx] - 270 - 120 * cy_idx + 10 * cy_idx_goal, 0, None, arcs_in, arcs_out,
                     t_id])
                t_id += 1

    return petri_net, p_id, t_id
