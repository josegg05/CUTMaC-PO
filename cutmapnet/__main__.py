from tscm.petri_nets import tpn, net_snakes, inter_tpn_v2
from intersection import intersections_classes
from intersection import intersections_config
import snakes.plugins
import time
import paho.mqtt.client as mqtt
import json
import datetime
import numpy as np
from skfuzzy import control as ctrl

# import logging

snakes.plugins.load(tpn, "snakes.nets", "snk")
from snk import *

# Define the global variable of command_received
intersection_id = "0002"
start_flag = False
msg_dic = []


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    global intersection_id
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("intersection/%s/e2det/n" % intersection_id)
    client.subscribe("intersection/%s/e2det/e" % intersection_id)
    client.subscribe("intersection/%s/e2det/s" % intersection_id)
    client.subscribe("intersection/%s/e2det/w" % intersection_id)
    client.subscribe("intersection/all/start")
    print("intersection/%s/e2det/n" % intersection_id)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global msg_dic
    global start_flag
    msg.payload = msg.payload.decode("utf-8")
    if msg.topic == "intersection/all/start":
        print("Message %s" % str(msg.payload))
        if "start" in str(msg.payload):
            start_flag = True
        elif "stop" in str(msg.payload):
            start_flag = False
    else:
        msg_dic.append(json.loads(msg.payload))
        print("message arrive from topic: ", msg.topic)
        print(msg.topic + " " + str(msg.payload))


def mqtt_conf() -> mqtt.Client:
    broker_address = "localhost"  # PC Office: "192.168.0.196"; PC Lab: "192.168.5.95"
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker_address)  # connect to broker
    return client


def subscribe_neighbors(neighbors):
    for x in neighbors.values():
        if x is not "":
            client_intersection.subscribe("intersection/" + x + "/state")
            print("Subscribed to: 'intersection/" + x + "/state'")
    return


def manage_flow(msg_in, movements, moves_green, moves_detectors, neighbors):
    # Function that saves the detectors and neighbor congestion info
    detector_id = msg_in["id"][-3:]
    msg_id = msg_in["id"]
    print("detector_id: ", detector_id)
    mov_ids = []
    if "e2det" in msg_id:  # My Flow Change
        print("Detector value changed in lane " + msg_in['laneId'])
        for mov in range(8):  # 8 movements
            if detector_id in moves_detectors[mov]:
                mov_ids.append(mov)
        print("Moves affected: ", mov_ids)
        for mov in mov_ids:
            if mov in moves_green:
                movements[mov].set_jam_length_vehicle(detector_id, msg_in["jamLengthVehicle"])
                movements[mov].set_mean_speed(detector_id, msg_in["meanSpeed"])
            movements[mov].set_occupancy(detector_id, msg_in["occupancy"])
            movements[mov].set_vehicle_number(detector_id, msg_in["vehicleNumber"])

    elif "state" in msg_id:  # Neighbor Flow Changes
        print("Flow status changes on neighbor " + msg_in['id'])
        for i in neighbors:
            if neighbors[i].id == msg_in["id"][13:17]:
                neighbors[i].mov_congestion = msg_in["mov_congestion"]

    return


def manage_accidents(msg_in, petri_net_snake, neighbors_ids, accident_lanes):
    direction_IO = ""
    msg_id = msg_in["id"]

    if "e2det" in msg_id:  # My Accident
        print("Accident status changes on street " + msg_in['laneId'])
        direction_IO = msg_in['id'][24]
        if msg_in["accidentOnLane"]:
            place_name = "Normal_to_Acc" + direction_IO.capitalize() + "I"
            accident_lanes.append(msg_in['id'])
        else:
            place_name = "Acc" + direction_IO.capitalize() + "I_to_Normal"
            accident_lanes.remove(msg_in['id'])

        msg = {
            "id": msg_in['id'],
            "type": "AccidentObserved",
            "laneId": msg_in['laneId'],
            "location": msg_in['location'],
            "dateObserved": datetime.datetime.utcnow().isoformat(),
            "accidentOnLane": msg_in["accidentOnLane"],  # It has to be configured
            "laneDirection": msg_in['laneDirection']
        }
        client_intersection.publish(msg_in['id'][0:18] + "state", json.dumps(msg))

    elif "state" in msg_id:  # Neighbor Accident
        print("Accident status changes on neighbor " + msg_in['id'])
        accident_neighbor_id = msg_in['id'][13:17]
        for dir, neigh_id in neighbors_ids.items():
            if neigh_id == accident_neighbor_id:
                if (dir == "S" and msg_in['id'][24] == "n") or \
                        (dir == "E" and msg_in['id'][24] == "w") or \
                        (dir == "N" and msg_in['id'][24] == "s") or \
                        (dir == "W" and msg_in['id'][24] == "e"):
                    direction_IO = dir
                    print(direction_IO)

        if msg_in["accidentOnLane"]:
            place_name = "Normal_to_Acc" + direction_IO + "O"
            accident_lanes.append(msg_in['id'])
        else:
            place_name = "Acc" + direction_IO + "O_to_Normal"
            accident_lanes.remove(msg_in['id'])

    if direction_IO is not "":
        petri_net_snake.place(place_name).add(dot)
    else:
        print("Error. Neighbor " + accident_neighbor_id + " not found")

    return


def congestion_model_conf(max_speed, max_vehicle_number):
    # Antecedent/Consequent and universe definition variables
    jamLengthVehicle = ctrl.Antecedent(np.arange(0, max_vehicle_number + 2, 1), 'jamLengthVehicle')
    vehicleNumber = ctrl.Antecedent(np.arange(0, max_vehicle_number + 2, 1), 'vehicleNumber')
    occupancy = ctrl.Antecedent(np.arange(0, 101, 1), 'occupancy')
    meanSpeed = ctrl.Antecedent(np.arange(0, max_speed + 1, 1), 'meanSpeed')
    congestionLevel = ctrl.Consequent(np.arange(0, 101, 1), 'congestionLevel')

    # Membership Functions definition
    jamLengthVehicle.automf(3, 'quant')
    vehicleNumber.automf(3, 'quant')
    occupancy.automf(3, 'quant')
    meanSpeed.automf(3, 'quant')
    congestionLevel.automf(5, 'quant')

    # Graph the Membership Functions
    # jamLengthVehicle.view()
    # vehicleNumber.view()
    # occupancy.view()
    # meanSpeed.view()
    # congestionLevel.view()

    # Define the Expert Rules
    rules = [
        ctrl.Rule((vehicleNumber['high'] | occupancy['high']) & (jamLengthVehicle['high'] | meanSpeed['low']),
                  congestionLevel['higher']),
        ctrl.Rule((vehicleNumber['high'] | occupancy['high']) & (jamLengthVehicle['average'] | meanSpeed['average']),
                  congestionLevel['high']),
        ctrl.Rule((vehicleNumber['high'] | occupancy['high']) & (jamLengthVehicle['low'] | meanSpeed['high']),
                  congestionLevel['average']),
        ctrl.Rule((vehicleNumber['average'] | occupancy['average']) & (jamLengthVehicle['high'] | meanSpeed['low']),
                  congestionLevel['high']),
        ctrl.Rule(
            (vehicleNumber['average'] | occupancy['average']) & (jamLengthVehicle['average'] | meanSpeed['average']),
            congestionLevel['average']),
        ctrl.Rule((vehicleNumber['average'] | occupancy['average']) & (jamLengthVehicle['low'] | meanSpeed['high']),
                  congestionLevel['low']),
        ctrl.Rule((vehicleNumber['low'] | occupancy['low']) & (jamLengthVehicle['high'] | meanSpeed['low']),
                  congestionLevel['average']),
        ctrl.Rule((vehicleNumber['low'] | occupancy['low']) & (jamLengthVehicle['average'] | meanSpeed['average']),
                  congestionLevel['low']),
        ctrl.Rule((vehicleNumber['low'] | occupancy['low']) & (jamLengthVehicle['low'] | meanSpeed['high']),
                  congestionLevel['lower']),
    ]

    # Controller definition
    congestion_model = ctrl.ControlSystem(rules)
    congestion_measuring_sim = ctrl.ControlSystemSimulation(congestion_model)

    return congestion_measuring_sim, congestionLevel


def congestion_measure(congestion_measuring_sim, movement, congestionLevel):
    congestion = 0.0
    if movement.get_vehicle_number() != 0:
        congestion_measuring_sim.input['jamLengthVehicle'] = movement.get_jam_length_vehicle()
        congestion_measuring_sim.input['vehicleNumber'] = movement.get_vehicle_number()
        congestion_measuring_sim.input['occupancy'] = movement.get_occupancy()
        congestion_measuring_sim.input['meanSpeed'] = movement.get_mean_speed()
        # Crunch the numbers
        congestion_measuring_sim.compute()
        congestion = congestion_measuring_sim.output['congestionLevel']

    f.write(str(movement.get_jam_length_vehicle()) + "; " +
            str(movement.get_vehicle_number()) + "; " +
            str(movement.get_occupancy()) + "; " +
            str(movement.get_mean_speed()) + "; ")
    # f.write("Congestion_" + str(movement.id) + " = " + str(congestion) + "; ")
    print("Congestion_", movement.id, " = ", congestion)
    # print("jamLengthVehicle = ", movement.get_jam_length_vehicle(),
    #       "; vehicleNumber = ", movement.get_vehicle_number(),
    #       "; occupancy = ", movement.get_occupancy(),
    #       "; meanSpeed = ", movement.get_mean_speed())
    # congestionLevel.view(sim=congestion_measuring_sim)

    return congestion


def send_state(my_topic, movements):
    mov_congestion = []
    for mov in range(8):
        if mov in movements:
            mov_congestion.append(movements[mov].congestionLevel)
        else:
            mov_congestion.append(0)
    msg = {
        "id": my_topic,
        "type": "TrafficFlowObserved",
        "dateObserved": datetime.datetime.utcnow().isoformat(),
        "mov_congestion": mov_congestion
    }
    client_intersection.publish(my_topic, json.dumps(msg))
    return


def set_five_quant_label(level):
    label = ""
    if level <= 1:
        label = "lower"
    elif level == 2:
        label = "low"
    elif level == 3:
        label = "average"
    elif level == 4:
        label = "high"
    elif level >= 5:
        label = "higher"
    return label


def split_model_conf():
    my_congestion_level = ctrl.Antecedent(np.arange(0, 101, 1), 'my_congestion_level')
    in_congestion_level = ctrl.Antecedent(np.arange(0, 101, 1), 'in_congestion_level')
    out_congestion_level = ctrl.Antecedent(np.arange(0, 101, 1), 'out_congestion_level')
    split = ctrl.Consequent(np.arange(-13, 14, 1), 'split')

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


def split_pi_model_conf():
    my_congestion_level = ctrl.Antecedent(np.arange(0, 101, 1), 'my_congestion_level')
    in_congestion_level = ctrl.Antecedent(np.arange(0, 101, 1), 'in_congestion_level')
    out_congestion_level = ctrl.Antecedent(np.arange(0, 101, 1), 'out_congestion_level')
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
        in_congestion_level = 0.0
    split_measuring_sim.input['in_congestion_level'] = in_congestion_level

    # print("Out Neighbor: ", movement.out_neighbors[1])
    if movement.out_neighbors[1] in neighbors.keys():
        out_congestion_level = (neighbors[movement.out_neighbors[1]].mov_congestion[movement.out_neighbors[0][0]] +
                                neighbors[movement.out_neighbors[1]].mov_congestion[movement.out_neighbors[0][1]]) / 2
        # print("out_congestion_level: ", out_congestion_level)
    else:
        out_congestion_level = 0.0
    split_measuring_sim.input['out_congestion_level'] = out_congestion_level

    # Crunch the numbers
    split_measuring_sim.compute()
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


def config_mov_split(petri_net_snake, movement):
    mean_green = 13
    t_split = 0
    transition_name = "tAct_" + str(movement.id)
    t_split = min(mean_green + int(movement.split), petri_net_snake.transition(transition_name).max_time)
    petri_net_snake.transition(transition_name).min_time = t_split
    print("tAct_" + str(movement.id) + "_time = ", (mean_green + int(movement.split)))
    f.write(str(mean_green + int(movement.split)) + ";" + "\n")
    return


def config_pi_mov_split(petri_net_snake, movement):
    transition_name = "tAct_" + str(movement.id)
    actual_green = petri_net_snake.transition(transition_name).min_time + movement.split
    if actual_green <= 0:
        actual_green = 0.0
    elif actual_green >= 25:
        actual_green = 25.0
    petri_net_snake.transition(transition_name).min_time = actual_green
    print("tAct_" + str(movement.id) + "_time = ", actual_green)
    f.write(str(actual_green) + ";" + "\n")
    return


def set_tls_lights(transitions_fire, inter_info, moves_green):
    l_change = False
    for i in transitions_fire:
        if "tGreen" in i:
            print("Voy a poner en GREEN el Movimiento %s" % i[-1])
            l_change = True
            moves_green.append(int(i[-1]))
            for j in inter_info.m_lights[0][int(i[-1])]:
                inter_info.lights[j] = "G"
        elif "tYel" in i:
            print("Voy a poner en YELLOW el Movimiento %s" % i[-1])
            l_change = True
            moves_green.remove(int(i[-1]))
            for j in inter_info.m_lights[0][int(i[-1])]:
                inter_info.lights[j] = "y"
        elif "tRed" in i:
            print("Voy a poner en RED el Movimiento %s" % i[-1])
            l_change = True
            for j in inter_info.m_lights[0][int(i[-1])]:
                inter_info.lights[j] = "r"

    # Send control msg to simulation
    if l_change:
        control_msg = {
            "tls_id": inter_info.tls_id,
            "type": "tlsControl",
            "command": "setPhase",
            "data": "".join(inter_info.lights)
        }

        client_intersection.publish(inter_info.tls_id, json.dumps(control_msg))
        print("send: " + json.dumps(control_msg))

    return


def run():
    global intersection_id
    global start_flag
    global msg_dic

    # Setup of the intersection
    inter_info = intersections_classes.Intersection(intersection_id, intersections_config.INTER_CONFIG_OSM)

    # Define my_topic
    my_topic = inter_info.state_topic
    # Subscribe to neighbors state topics
    subscribe_neighbors(inter_info.neighbors_ids)

    # Setup the congestion model and split controller
    congestion_measuring_sim, congestionLevel = congestion_model_conf(inter_info.m_max_speed,
                                                                      inter_info.m_max_vehicle_number)
    split_measuring_sim, split = split_pi_model_conf()

    # Reset Loop
    # while True:
    accident_lanes = []
    movements = {}  # dictionary of movements
    neighbors = {}  # dictionary of neighbors
    moves_green = []
    phases_list = [[0, 4], [0, 5], [1, 4], [1, 5], [2, 6], [2, 7], [3, 6], [3, 7]]

    # Create intersection Movements
    for i in range(len(inter_info.movements)):
        if (i == 0) or (inter_info.movements[i] > inter_info.movements[i - 1]):
            movements[inter_info.movements[i]] = intersections_classes.Movement(inter_info.movements[i], inter_info)
    print("Intersection Movements: ", movements)

    # Create intersection neighbors
    for i in inter_info.neighbors_ids:
        if inter_info.neighbors_ids[i] != "":
            neighbors[i] = intersections_classes.Neighbor(inter_info.neighbors_ids[i], i)
    print("Intersection Neighbors: ", neighbors)

    # Set the definition vectors of the Timed Petri Net
    petri_net_inter, place_id, transition_id = inter_tpn_v2.net_create(inter_info.movements, inter_info.phases,
                                                                       inter_info.cycles, inter_info.cycles_names)

    # Create de SNAKE Petri Net
    petri_net_snake = net_snakes.net_snakes_create(petri_net_inter)
    init = petri_net_snake.get_marking()
    # "petri_net_snake.set_marking(init)" Acts like n.reset(), because each transition has a place in its pre-set whose
    # marking is reset, just like for method reset
    petri_net_snake.set_marking(init)
    print(init)

    print("Tokens de Normal = ", petri_net_snake.place("CNormal").tokens)
    print("Intersection '%s' READY:" % intersection_id)
    while not start_flag:
        pass  # Do nothing waiting for the start signal

    # Set Petri Net Time, delay and step variables initial values to start
    time_0 = time.perf_counter()
    time_current = 0.0
    delay = 0.0
    step = 1.0

    # Start the Intersection Petri Net
    print("\n\nStart the Intersection Petri Net:")
    while start_flag:
        transitions_fire = []

        # Print the current time and delay
        print("Time:[%s] " % time_current, "delay:", delay)

        # Fires all the fireable transitions
        p_fire = True
        count_fire = 0
        while p_fire:
            p_fire = False
            for t in petri_net_snake.transition():
                try:
                    petri_net_snake.transition(t.name).fire(Substitution())
                    p_fire = True
                    count_fire += 1
                    transitions_fire.append(str(t.name))
                    print("[%s] fire: %s, count_fire: %s" % (time_current, t.name, count_fire))
                except:
                    pass
        # print(transitions_fire)

        # Set the TS
        set_tls_lights(transitions_fire, inter_info, moves_green)
        # print("Moves in Green: ", moves_green)

        # Measure congestion and split of correspondent Movement
        for i in transitions_fire:
            if (("tNormal" in i) or ("tAcc" in i)) and (i[-1] not in ["l", "I", "O"]):
                print("Measure congestion and split of the Movement of the next Phase --> %s" % i[-2])
                # for j in inter_info.phases[int(i[-2])]:  # For inter_tpn
                for mov in phases_list[int(i[-2])]:  # For inter_tpn_v2
                    if mov in movements.keys():
                        f.write(str(movements[mov].id) + "; " + str(time_current) + "; ")
                        movements[j].congestionLevel = congestion_measure(congestion_measuring_sim, movements[mov],
                                                                          congestionLevel)
                        movements[mov].split = split_measure(split_measuring_sim, movements[mov], neighbors, split)
                        config_pi_mov_split(petri_net_snake, movements[mov])
                send_state(my_topic, movements)

        # # Add accident in B at t = 30
        # if time_current == 30:
        #     my_accident_change = True
        #     msg_dic.append({
        #         "id": "intersection/0002/e2det/s03",
        #         "type": "AccidentObserved",
        #         "laneId": "436291016#3_3",
        #         "location": "here",
        #         "dateObserved": datetime.datetime.utcnow().isoformat(),
        #         "accidentOnLane": True,
        #         "laneDirection": "s-_wn_"
        #     })
        # # Remove accident in B at t = 300
        # if time_current == 300:
        #     my_accident_change = True
        #     msg_dic.append({
        #         "id": "intersection/0002/e2det/s03",
        #         "type": "AccidentObserved",
        #         "laneId": "436291016#3_3",
        #         "location": "here",
        #         "dateObserved": datetime.datetime.utcnow().isoformat(),
        #         "accidentOnLane": False,
        #         "laneDirection": "s-_wn_"
        #     })

        # Manage msgs received
        if msg_dic:
            msg_in = msg_dic.pop(0)
            msg_id = msg_in['id']
            msg_type = msg_in['type']
            if ("e2det" in msg_id) or ("state" in msg_id):
                if msg_type == "TrafficFlowObserved":
                    manage_flow(msg_in, movements, moves_green, inter_info.m_detectors, neighbors)
                elif msg_type == "AccidentObserved":
                    manage_accidents(msg_in, petri_net_snake, inter_info.neighbors_ids, accident_lanes)

        # Wait for a second to transit
        time_current += 1.0
        while time.perf_counter() < time_0 + time_current:
            pass
        # Update the network time
        # print("step = ", step)
        delay = petri_net_snake.time(step)


if __name__ == '__main__':
    client_intersection = mqtt_conf()
    # client_intersection: mqtt.Client = mqtt_conf()
    client_intersection.loop_start()  # Necessary to maintain connection
    f = open("app_%s.log" % intersection_id, "w+")
    f.write("movement_id; time; jam_length_vehicle; vehicle_number; occupancy; mean_speed; my_congestion_level; "
            "in_congestion_level; out_congestion_level; split; act_ime;\n")
    run()
    f.close()
