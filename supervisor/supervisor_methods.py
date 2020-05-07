
# ------------------------------------- Variable Cycle - Mov Split ---------------------------------------------------
def split_pi_model_conf():
    my_congestion_level = ctrl.Antecedent(np.arange(0, 81, 1), 'my_congestion_level')  # Antes 101
    in_congestion_level = ctrl.Antecedent(np.arange(0, 81, 1), 'in_congestion_level')  # Antes 101
    out_congestion_level = ctrl.Antecedent(np.arange(0, 81, 1), 'out_congestion_level')  # Antes 101
    split = ctrl.Consequent(np.arange(-2, 3, 1), 'split')

    # Membership Functions definition
    my_congestion_level.automf(5, 'quant')
    in_congestion_level.automf(5, 'quant')
    out_congestion_level.automf(5, 'quant')
    split.automf(5, 'quant')

    # Graph the Membership Functions
    # my_congestion_level.view()
    # in_congestion_level.view()
    # out_congestion_level.view()
    # split.view()

    # Define the Expert Rules
    split_values_vector = [1, 1, 2, 2, 3, 4, 4, 5, 5]
    rules = []
    for my_cong in range(5):
        for in_cong in range(5):
            for out_cong in range(5):
                my_label = set_five_quant_label(my_cong + 1)
                in_label = set_five_quant_label(in_cong + 1)
                out_label = set_five_quant_label(5 - out_cong)
                split_label = set_five_quant_label(split_values_vector[in_cong + out_cong] - 2 + my_cong)
                rules.append(ctrl.Rule(my_congestion_level[my_label] &
                                       in_congestion_level[in_label] &
                                       out_congestion_level[out_label],
                                       split[split_label]))

    # print(rules)
    split_model = ctrl.ControlSystem(rules)
    split_measuring_sim = ctrl.ControlSystemSimulation(split_model)

    return split_measuring_sim, split


def split_measure(split_measuring_sim, movement, neighbors, split):
    # print("Movement to measure Split: ", movement.id)
    split_measuring_sim.input['my_congestion_level'] = movement.congestionLevel

    # print("In Neighbor: ", movement.in_neighbors[1])
    if movement.in_neighbors[1] in neighbors.keys():
        in_congestion_level = (neighbors[movement.in_neighbors[1]].mov_congestion[movement.in_neighbors[0][0]] +
                               neighbors[movement.in_neighbors[1]].mov_congestion[movement.in_neighbors[0][1]]) / 2
        # print("in_congestion_level", in_congestion_level)
    else:
        in_congestion_level = 50.0
    split_measuring_sim.input['in_congestion_level'] = in_congestion_level

    # print("Out Neighbor: ", movement.out_neighbors[1])
    if movement.out_neighbors[1] in neighbors.keys():
        out_congestion_level = (neighbors[movement.out_neighbors[1]].mov_congestion[movement.out_neighbors[0][0]] +
                                neighbors[movement.out_neighbors[1]].mov_congestion[movement.out_neighbors[0][1]]) / 2
        # print("out_congestion_level: ", out_congestion_level)
    else:
        out_congestion_level = 50.0
    split_measuring_sim.input['out_congestion_level'] = out_congestion_level

    # Crunch the numbers
    split_measuring_sim.compute()
    with open("sup_%s.log" % intersection_id, "a") as f:
        f.write(str(movement.congestionLevel) + "; " +
                str(in_congestion_level) + "; " +
                str(out_congestion_level) + "; " +
                str(split_measuring_sim.output['split']) + "; ")
    print("Split_", movement.id, " = ", split_measuring_sim.output['split'])
    # print("my_congestion_level = ", movement.congestionLevel,
    #       "; in_congestion_level = ", in_congestion_level,
    #       "; out_congestion_level = ", out_congestion_level)
    # split.view(sim=split_measuring_sim)

    return split_measuring_sim.output['split']


def config_mov_split(split_cal):
    mean_green = 16
    actual_green = min(mean_green + int(split_cal), 100)
    return actual_green


def config_pi_mov_split(movement, split_cal):
    actual_green = movement.split + split_cal
    if actual_green <= 0:
        actual_green = 0.0
    elif actual_green >= 25:
        actual_green = 25.0
    return actual_green


def split_set(mov_displays_change, split_measuring_sim, movements, neighbors, split, time_current, id):
    mov_splits_changed = {}
    for mov in mov_displays_change:
        with open("sup_%s.log" % intersection_id, "a") as f:
            f.write(str(movements[mov].id) + "; " + str(time_current) + "; ")
        # TODO: Read the dtm log and write the info to the complete log
        split_cal = split_measure(split_measuring_sim, movements[mov], neighbors, split)
        actual_green = config_pi_mov_split(movements[mov], split_cal)
        movements[mov].split = actual_green
        mov_splits_changed[mov] = actual_green
        print("tAct_" + str(movements[mov].id) + "_time = ", actual_green)
        with open("sup_%s.log" % intersection_id, "a") as f:
            f.write(str(actual_green) + "\n")
    # Done: TODO: Send t_split to the TPN
    split_msg = {
        "id": id,
        "type": "config",
        "category": {
            "value": ["split"]
        },
        "value": {
            "value": mov_splits_changed
        }
    }
    return split_msg


def run_variable_mov():
    global msg_dic

    tscm_topic_split = b"super/tscm/command"
    tscm_topic_cycle = b"super/tscm/command"
    dtm_topic_congestion = b"super/dtm/command"
    dtm_topic_display = b"super/dtm/state"
    pub_socket = pub_zmq_config("5558")
    dtm_sub_socket = sub_zmq_config("5556", b"dtm/state")
    tscm_sub_socket = sub_zmq_config("5557", b"tscm/state")
    poller = poller_config([dtm_sub_socket, tscm_sub_socket])

    # Setup of the intersection
    inter_info = intersections_classes.Intersection(intersection_id, intersections_config.INTER_CONFIG_OSM)

    # Define my_topic
    my_topic = inter_info.state_topic
    # Subscribe to neighbors state topics
    subscribe_neighbors(inter_info.neighbors_ids)

    # Setup the split controller
    split_measuring_sim, split = split_pi_model_conf()

    # Reset Loop
    # while True:
    accident_lanes = []
    movements = {}  # dictionary of movements
    neighbors = {}  # dictionary of neighbors
    phases_list = [[0, 4], [0, 5], [1, 4], [1, 5], [2, 6], [2, 7], [3, 6], [3, 7]]

    # Create intersection Movements
    for i in range(len(inter_info.movements)):
        if (i == 0) or (inter_info.movements[i] >= inter_info.movements[i - 1]):
            movements[inter_info.movements[i]] = intersections_classes.Movement(inter_info.movements[i], inter_info)
        else:
            break
    print("Intersection Movements: ", movements)

    # Create intersection neighbors
    for i in inter_info.neighbors_ids:
        if inter_info.neighbors_ids[i] != "":
            neighbors[i] = intersections_classes.Neighbor(inter_info.neighbors_ids[i], i)
    print("Intersection Neighbors: ", neighbors)

    # Beging the log
    with open("sup_%s.log" % intersection_id, "w") as f:
        f.write("movement_id; time; my_congestion_level; in_congestion_level; out_congestion_level; split; act_time\n")

    # Intersection ready tu start
    print("Intersection '%s' READY:" % intersection_id)
    while not start_flag:
        pass  # Do nothing waiting for the start signal

    # Set Petri Net Time, delay and step variables initial values to start
    time_0 = time.perf_counter()
    time_current = 0.0

    # Start the Intersection Petri Net
    print("\n\nStart the Intersection Petri Net:")
    while start_flag:
        # Manage mqtt msgs received
        if msg_dic:
            msg_mqtt = msg_dic.pop(0)
            msg_id = msg_mqtt['id']
            msg_type = msg_mqtt['type']
            if ("state" in msg_id):
                if msg_type == "TrafficFlowObserved":
                    manage_flow(msg_mqtt, neighbors)
                elif msg_type == "AccidentObserved":
                    manage_accidents(msg_mqtt, inter_info.neighbors_ids, accident_lanes)

        # TODO:
        #  Done: If new Phase: Send cong_measure command to dtm with msg.attribute = [mov1, mov2]
        #  Done: If Display change: Send Display state to DTM
        #   Done: If new Red: Send new Cycle if there is one
        #   Done: If new Green: Send mov split to TPN
        poll = dict(poller.poll(20))
        if tscm_sub_socket in poll and poll[tscm_sub_socket] == zmq.POLLIN:
            [top, contents] = tscm_sub_socket.recv_multipart()
            msg_zmq = json.loads(contents.decode())
            msg_type = msg_zmq['type']
            if b"tscm" in top and "state" in msg_type:  # Puede ser parte del ombre
                print(msg_zmq)
                # Measure congestion of correspondent Movement
                if "phase" in msg_zmq['category']["value"]:  # Debe ser el nombre exacto
                    print(time_current, "Measure congestion of the Movement of the next Phase -->",
                          msg_zmq['state']["value"])
                    mov_congestion_measure = [phases_list[i] for i in range(len(msg_zmq["state"]["value"])) if
                                              msg_zmq["state"]["value"][i] != 0]  # list of list
                    congestion_msg = {
                        "id": inter_info.id,
                        "type": "stateMeasure",
                        "category": {
                            "value": ["mov_congestion"]
                        },
                        "value": {
                            "value": mov_congestion_measure[0]  # list of movements involved
                        }
                    }
                    pub_socket.send_multipart([dtm_topic_congestion, json.dumps(congestion_msg).encode()])
                if "display" in msg_zmq['category']["value"]:
                    pub_socket.send_multipart([dtm_topic_display, contents])  # Send Display State to DTM
                    msg_displays = list(msg_zmq["state"]["value"])  # Ej: ["r", "r", "r", "r", "r", "r", "r", "r"]
                    mov_displays_change = {}  # dic -> {mov: "display"}. Ej: {2: "y", 7: "y"}
                    for mov in range(len(msg_displays)):
                        if mov in movements and movements[mov].light_state != msg_displays[mov]:
                            # print("The movement", mov, "is", movements[mov])
                            mov_displays_change[mov] = msg_displays[mov]
                            movements[mov].light_state = msg_displays[mov]
                    if "r" in mov_displays_change.values():
                        # TODO: Crear el msg de cycle_msg con la info de los movimientos
                        pass
                        # cycle_msg = cycle_set(msg_zmq["id"])
                        # pub_socket.send_multipart([tscm_topic_cycle, json.dumps(cycle_msg).encode()])
                    # Measure split of correspondent Movement
                    elif "G" in mov_displays_change.values():
                        print("Calculate split of movements: ", mov_displays_change)
                        split_msg = split_set(mov_displays_change, split_measuring_sim, movements, neighbors, split,
                                              time_current, msg_zmq["id"])
                        pub_socket.send_multipart([tscm_topic_split, json.dumps(split_msg).encode()])

        if dtm_sub_socket in poll and poll[dtm_sub_socket] == zmq.POLLIN:
            [top, contents] = dtm_sub_socket.recv_multipart()
            msg_zmq = json.loads(contents.decode())
            print(msg_zmq)
            msg_type = msg_zmq['type']
            if b"dtm" in top and "state" in msg_type:
                if "mov_congestion" in msg_zmq['category']["value"]:
                    mov_congestion = msg_zmq['state']["value"]
                    print(time_current, "Congestion of movements :", mov_congestion, "arrived")
                    for mov in mov_congestion:
                        movements[int(mov)].congestionLevel = mov_congestion[mov]
                    # Send state to the Neighbors
                    send_state(my_topic, movements)
                elif "mov_accident" in msg_zmq['category']["value"]:
                    mov_accident = msg_zmq['state']["value"]
                    for mov in range(len(mov_accident)):
                        movements[int(mov)].accident = mov_accident[mov]

        # Update time_current
        if time.perf_counter() >= time_0 + time_current + 1:
            time_current += 1.0
        # Wait for a second to transit
        # time_current += 1.0
        # while time.perf_counter() < time_0 + time_current:
        #     pass

# ------------------------------------- Fixed Cycle - Delayed --------------------------------------------------------
def split_model_conf():
    my_congestion_level = ctrl.Antecedent(np.arange(0, 81, 1), 'my_congestion_level')  # Antes 101
    in_congestion_level = ctrl.Antecedent(np.arange(0, 81, 1), 'in_congestion_level')  # Antes 101
    out_congestion_level = ctrl.Antecedent(np.arange(0, 81, 1), 'out_congestion_level')  # Antes 101
    split = ctrl.Consequent(np.arange(0, 101, 1), 'split')

    # Membership Functions definition
    my_congestion_level.automf(5, 'quant')
    in_congestion_level.automf(5, 'quant')
    out_congestion_level.automf(5, 'quant')
    split.automf(5, 'quant')

    # Graph the Membership Functions
    # my_congestion_level.view()
    # in_congestion_level.view()
    # out_congestion_level.view()
    # split.view()

    # Define the Expert Rules
    split_values_vector = [1, 1, 2, 2, 3, 4, 4, 5, 5]
    rules = []
    for my_cong in range(5):
        for in_cong in range(5):
            for out_cong in range(5):
                my_label = set_five_quant_label(my_cong + 1)
                in_label = set_five_quant_label(in_cong + 1)
                out_label = set_five_quant_label(5 - out_cong)
                split_label = set_five_quant_label(split_values_vector[in_cong + out_cong] - 2 + my_cong)
                rules.append(ctrl.Rule(my_congestion_level[my_label] &
                                       in_congestion_level[in_label] &
                                       out_congestion_level[out_label],
                                       split[split_label]))

    # print(rules)
    split_model = ctrl.ControlSystem(rules)
    split_measuring_sim = ctrl.ControlSystemSimulation(split_model)

    return split_measuring_sim, split


def split_measure(split_measuring_sim, movement, neighbors, split):
    # print("Movement to measure Split: ", movement.id)
    split_measuring_sim.input['my_congestion_level'] = movement.congestionLevel

    # print("In Neighbor: ", movement.in_neighbors[1])
    if movement.in_neighbors[1] in neighbors.keys():
        in_congestion_level = (neighbors[movement.in_neighbors[1]].mov_congestion[movement.in_neighbors[0][0]] +
                               neighbors[movement.in_neighbors[1]].mov_congestion[movement.in_neighbors[0][1]]) / 2
        # print("in_congestion_level", in_congestion_level)
    else:
        in_congestion_level = 50.0
    split_measuring_sim.input['in_congestion_level'] = in_congestion_level

    # print("Out Neighbor: ", movement.out_neighbors[1])
    if movement.out_neighbors[1] in neighbors.keys():
        out_congestion_level = (neighbors[movement.out_neighbors[1]].mov_congestion[movement.out_neighbors[0][0]] +
                                neighbors[movement.out_neighbors[1]].mov_congestion[movement.out_neighbors[0][1]]) / 2
        # print("out_congestion_level: ", out_congestion_level)
    else:
        out_congestion_level = 50.0
    split_measuring_sim.input['out_congestion_level'] = out_congestion_level

    # Crunch the numbers
    split_measuring_sim.compute()
    with open("sup_%s.log" % intersection_id, "a") as f:
        f.write(str(movement.congestionLevel) + "; " +
                str(in_congestion_level) + "; " +
                str(out_congestion_level) + "; " +
                str(split_measuring_sim.output['split']) + "; ")
    print("Split_", movement.id, " = ", split_measuring_sim.output['split'])
    # print("my_congestion_level = ", movement.congestionLevel,
    #       "; in_congestion_level = ", in_congestion_level,
    #       "; out_congestion_level = ", out_congestion_level)
    # split.view(sim=split_measuring_sim)

    return split_measuring_sim.output['split']


def split_msg_set(phase_split, mov_displays_change, phase_list):
    mov_splits_changed = {}
    mov_changed = list(map(int, mov_displays_change.keys())).sort()  # Change list of str to a list of int
    for mov in mov_changed:
        mov_splits_changed[mov] = phase_split[phase_list.index(mov_changed)]

    split_msg = {
        "id": id,
        "type": "config",
        "category": {
            "value": ["split"]
        },
        "value": {
            "value": mov_splits_changed
        }
    }
    return split_msg


def split_set(phase_split_percentage, cycle_length, time_current):
    split_sum = 0
    phase_split = [0, 0, 0, 0, 0, 0, 0, 0]
    for sp in phase_split_percentage:
        split_sum += sp
    for ph in range(len(phase_split_percentage)):
        phase_split[ph] = phase_split_percentage[ph]*cycle_length/split_sum
        with open("sup_%s.log" % intersection_id, "a") as f:
            f.write(str(ph) + "; " + str(time_current) + "; " + str(phase_split_percentage[ph]) + "; " +
                    str(phase_split[ph].split) + "\n")
    return phase_split



def run_static_delay():
    global msg_dic

    tscm_topic_split = b"super/tscm/command"
    tscm_topic_cycle = b"super/tscm/command"
    dtm_topic_congestion = b"super/dtm/command"
    dtm_topic_display = b"super/dtm/state"
    pub_socket = pub_zmq_config("5558")
    dtm_sub_socket = sub_zmq_config("5556", b"dtm/state")
    tscm_sub_socket = sub_zmq_config("5557", b"tscm/state")
    poller = poller_config([dtm_sub_socket, tscm_sub_socket])


    # Setup of the intersection
    inter_info = intersections_classes.Intersection(intersection_id, intersections_config.INTER_CONFIG_OSM)

    # Define my_topic
    my_topic = inter_info.state_topic
    # Subscribe to neighbors state topics
    subscribe_neighbors(inter_info.neighbors_ids)

    # Setup the split controller
    split_measuring_sim, split = split_pi_model_conf()

    # Reset Loop
    # while True:
    accident_lanes = []
    movements = {}  # dictionary of movements
    neighbors = {}  # dictionary of neighbors
    phases_list = [[0, 4], [0, 5], [1, 4], [1, 5], [2, 6], [2, 7], [3, 6], [3, 7]]
    phase_split_percentage = [0, 0, 0, 0, 0, 0, 0, 0]
    phase_split = [0, 0, 0, 0, 0, 0, 0, 0]
    first_phase = inter_info.phases[inter_info.cycles[0][-1]]  # List of movements of the first phase
    cycle_length = 64  # 16 seg/phases * 4 phases/cycle

    # Create intersection Movements
    for i in range(len(inter_info.movements)):
        if (i == 0) or (inter_info.movements[i] >= inter_info.movements[i - 1]):
            movements[inter_info.movements[i]] = intersections_classes.Movement(inter_info.movements[i], inter_info)
        else:
            break
    print("Intersection Movements: ", movements)

    # Create intersection neighbors
    for i in inter_info.neighbors_ids:
        if inter_info.neighbors_ids[i] != "":
            neighbors[i] = intersections_classes.Neighbor(inter_info.neighbors_ids[i], i)
    print("Intersection Neighbors: ", neighbors)

    # Beging the log
    with open("sup_%s.log" % intersection_id, "w") as f:
        f.write("phase_id; time; split_percentage; split\n")

    # Intersection ready tu start
    print("Intersection '%s' READY:" % intersection_id)
    while not start_flag:
        pass  # Do nothing waiting for the start signal

    # Set Petri Net Time, delay and step variables initial values to start
    time_0 = time.perf_counter()
    time_current = 0.0

    # Start the Intersection Petri Net
    print("\n\nStart the Intersection Petri Net:")
    while start_flag:
        # Manage mqtt msgs received
        if msg_dic:
            msg_mqtt = msg_dic.pop(0)
            msg_id = msg_mqtt['id']
            msg_type = msg_mqtt['type']
            if ("state" in msg_id):
                if msg_type == "TrafficFlowObserved":
                    manage_flow(msg_mqtt, neighbors)
                elif msg_type == "AccidentObserved":
                    manage_accidents(msg_mqtt, inter_info.neighbors_ids, accident_lanes)

        # TODO:
        #  Done: If new Phase: Send cong_measure command to dtm with msg.attribute = [mov1, mov2]
        #  Done: If Display change: Send Display state to DTM
        #   Done: If new Red: Send new Cycle if there is one
        #   Done: If new Green: Send mov split to TPN
        poll = dict(poller.poll(20))
        if tscm_sub_socket in poll and poll[tscm_sub_socket] == zmq.POLLIN:
            [top, contents] = tscm_sub_socket.recv_multipart()
            msg_zmq = json.loads(contents.decode())
            msg_type = msg_zmq['type']
            if b"tscm" in top and "state" in msg_type:  # Puede ser parte del ombre
                print(msg_zmq)
                # Measure congestion of correspondent Movement
                if "phase" in msg_zmq['category']["value"]:  # Debe ser el nombre exacto
                    print(time_current, "Measure congestion of the Movement of the next Phase -->",
                          msg_zmq['state']["value"])
                    mov_congestion_measure = [phases_list[i] for i in range(len(msg_zmq["state"]["value"])) if
                                              msg_zmq["state"]["value"][i] != 0]  # list of list

                    if first_phase in mov_congestion_measure:
                        split_set(phase_split, cycle_length, movements, time_current)

                    congestion_msg = {
                        "id": inter_info.id,
                        "type": "stateMeasure",
                        "category": {
                            "value": ["mov_congestion"]
                        },
                        "value": {
                            "value": mov_congestion_measure[0]  # list of movements involved
                        }
                    }
                    pub_socket.send_multipart([dtm_topic_congestion, json.dumps(congestion_msg).encode()])
                if "display" in msg_zmq['category']["value"]:
                    pub_socket.send_multipart([dtm_topic_display, contents])  # Send Display State to DTM
                    msg_displays = list(msg_zmq["state"]["value"])  # Ej: ["r", "r", "r", "r", "r", "r", "r", "r"]
                    mov_displays_change = {}  # dic -> {mov: "display"}. Ej: {2: "y", 7: "y"}
                    for mov in range(len(msg_displays)):
                        if mov in movements and movements[mov].light_state != msg_displays[mov]:
                            # print("The movement", mov, "is", movements[mov])
                            mov_displays_change[mov] = msg_displays[mov]
                            movements[mov].light_state = msg_displays[mov]
                    if "r" in mov_displays_change.values():
                        # TODO: Crear el msg de cycle_msg con la info de los movimientos
                        pass
                        # cycle_msg = cycle_set(msg_zmq["id"])
                        # pub_socket.send_multipart([tscm_topic_cycle, json.dumps(cycle_msg).encode()])
                    # Measure split of correspondent Movement
                    elif "G" in mov_displays_change.values():
                        print("Calculate split of movements: ", mov_displays_change)
                        split_msg = split_msg_set(phase_split, mov_displays_change, phases_list)
                        pub_socket.send_multipart([tscm_topic_split, json.dumps(split_msg).encode()])

        if dtm_sub_socket in poll and poll[dtm_sub_socket] == zmq.POLLIN:
            [top, contents] = dtm_sub_socket.recv_multipart()
            msg_zmq = json.loads(contents.decode())
            print(msg_zmq)
            msg_type = msg_zmq['type']
            if b"dtm" in top and "state" in msg_type:
                if "mov_congestion" in msg_zmq['category']["value"]:
                    mov_congestion = msg_zmq['state']["value"]
                    print(time_current, "Congestion of movements :", mov_congestion, "arrived")
                    split_temp = []
                    phase_movs = []
                    for mov in mov_congestion:
                        movements[int(mov)].congestionLevel = mov_congestion[mov]
                        phase_movs.append(int(mov))
                        split_temp.append(split_measure(split_measuring_sim, movements[int(mov)], neighbors, split))
                    phase_split_percentage[phases_list.index(phase_movs.sort())] = (split_temp[0] + split_temp[1])/len(split_temp)
                    # Send state to the Neighbors
                    send_state(my_topic, movements)
                elif "mov_accident" in msg_zmq['category']["value"]:
                    mov_accident = msg_zmq['state']["value"]
                    for mov in range(len(mov_accident)):
                        movements[int(mov)].accident = mov_accident[mov]

        # Update time_current
        if time.perf_counter() >= time_0 + time_current + 1:
            time_current += 1.0
        # Wait for a second to transit
        # time_current += 1.0
        # while time.perf_counter() < time_0 + time_current:
        # pass