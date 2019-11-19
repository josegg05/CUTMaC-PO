from cutmapnet.petri_nets import tpn
from cutmapnet.petri_nets import inter_tpn
from cutmapnet.petri_nets import net_snakes
from cutmapnet.petri_nets import intersections_info
import snakes.plugins
import time
import paho.mqtt.client as mqtt
import json
import datetime
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

snakes.plugins.load(tpn, "snakes.nets", "snk")
from snk import *

# Define the global variable of command_received
my_detector_change = False
my_accident_change = False
neighbor_flow_change = False
neighbor_accident_change = False
msg_dic = []


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("intersection/0002/e2det/n")
    client.subscribe("intersection/0002/e2det/e")
    client.subscribe("intersection/0002/e2det/s")
    client.subscribe("intersection/0002/e2det/w")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    msg_type = str(json.loads(msg.payload)["type"])
    global msg_dic

    if "e2det" in msg.topic:
        if msg_type == "TrafficFlowObserved":
            global my_detector_change
            msg_dic.append(json.loads(msg.payload))
            my_detector_change = True
            print(f"Detector value changed lane {msg_dic['laneId']}")
        elif msg_type == "AccidentObserved":
            global my_accident_change
            msg_dic.append(json.loads(msg.payload))
            my_accident_change = True
            print(f"Accident status changes on street {msg_dic['id']}")
    elif "state" in msg.topic:
        if msg_type == "TrafficFlowObserved":
            global neighbor_flow_change
            msg_dic.append(json.loads(msg.payload))
            neighbor_flow_change = True
            print(f"Flow status changes on neighbor {msg_dic['id']}")
        elif msg_type == "AccidentObserved":
            global neighbor_accident_change
            msg_dic.append(json.loads(msg.payload))
            neighbor_accident_change = True
            print(f"Accident status changes on neighbor {msg_dic['id']}")


def mqtt_conf() -> mqtt.Client:
    broker_address = "192.168.0.196"  # "192.168.1.95"
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


def manage_accidents(petri_net_snake, neighbors, accident_lanes):
    global neighbor_accident_change
    global my_accident_change
    global msg_dic
    direction = ""

    if my_accident_change:
        my_accident_change = False
        direction = msg_dic['id'][24]
        if msg_dic["accidentOnLane"]:
            place_name = f"Normal_to_Acc{direction.capitalize()}I"
            accident_lanes.append(msg_dic['id'])
        else:
            place_name = f"Acc{direction.capitalize()}I_to_Normal"
            accident_lanes.remove(msg_dic['id'])

        msg = {
            "id": msg_dic['id'],
            "type": "AccidentObserved",
            "laneId": msg_dic['laneId'],
            "location": msg_dic['location'],
            "dateObserved": datetime.datetime.utcnow().isoformat(),
            "accidentOnLane": msg_dic["accidentOnLane"],  # It has to be configured
            "laneDirection": msg_dic['laneDirection']
        }
        client_intersection.publish(msg_dic['id'][0:18] + "state", json.dumps(msg))

    if neighbor_accident_change:
        neighbor_accident_change = False
        accident_neighbor = msg_dic['id'][13:17]
        for dir, neigh in neighbors.items():  # for name, age in dictionary.iteritems():  (for Python 2.x)
            if neigh == accident_neighbor:
                if (dir == "S" and msg_dic['id'][24] == "n") or \
                   (dir == "E" and msg_dic['id'][24] == "w") or \
                   (dir == "N" and msg_dic['id'][24] == "s") or \
                   (dir == "W" and msg_dic['id'][24] == "e"):
                    direction = dir
                    print(direction)

        if msg_dic["accidentOnLane"]:
            place_name = f"Normal_to_Acc{direction}O"
            accident_lanes.append(msg_dic['id'])
        else:
            place_name = f"Acc{direction}O_to_Normal"
            accident_lanes.remove(msg_dic['id'])

    if direction is not "":
        petri_net_snake.place(place_name).add(dot)
    else:
        print(f"Error. Neighbor {accident_neighbor} not found")
    return


def congestion_estimator_conf():
    # Antecedent/Consequent and universe definition variables
    jamLengthVehicle = ctrl.Antecedent(np.arange(0, 21, 1), 'jamLengthVehicle')
    occupancy = ctrl.Antecedent(np.arange(0, 101, 1), 'occupancy')
    meanSpeed = ctrl.Antecedent(np.arange(0, 61, 1), 'meanSpeed')
    vehicleNumber = ctrl.Antecedent(np.arange(0, 21, 1), 'vehicleNumber')
    congestion = ctrl.Consequent(np.arange(0, 101, 1), 'congestion')

    # Membership Functions definition
    jamLengthVehicle.automf(3, 'quant')
    occupancy.automf(3, 'quant')
    meanSpeed.automf(3, 'quant')
    vehicleNumber.automf(3, 'quant')
    congestion.automf(5, 'quant')

    # Graph the Membership Functions
    # jamLengthVehicle.view()
    # occupancy.view()
    # meanSpeed.view()
    # vehicleNumber.view()
    # congestion.view()

    # TODO: Define the real rules to measure Intersection Congestion
    # Define the Expert Rules
    rules = [
        ctrl.Rule((jamLengthVehicle['high'] | occupancy['high']) & meanSpeed['low'], congestion['higher']),
        ctrl.Rule((jamLengthVehicle['high'] | occupancy['high']) & meanSpeed['average'], congestion['high']),
        ctrl.Rule((jamLengthVehicle['high'] | occupancy['high']) & meanSpeed['high'], congestion['high']),
        ctrl.Rule((jamLengthVehicle['average'] | occupancy['average']) & meanSpeed['average'], congestion['average']),
        ctrl.Rule((jamLengthVehicle['low'] | occupancy['low']) & meanSpeed['low'], congestion['low']),
        ctrl.Rule((jamLengthVehicle['low'] | occupancy['low']) & meanSpeed['average'], congestion['low']),
        ctrl.Rule((jamLengthVehicle['low'] | occupancy['low']) & meanSpeed['high'], congestion['lower'])
    ]

    # Controller definition
    congestion_estimator = ctrl.ControlSystem(rules)
    congestion_measure = ctrl.ControlSystemSimulation(congestion_estimator)

    return congestion_measure, congestion


def controller_configuration():
    # TODO: configure the controller for the split
    return


def split_control(congestion_measure, congestion):
    # TODO: deal with sensor and other intersections msgs received
    # Example
    congestion_measure.input['jamLengthVehicle'] = 15
    congestion_measure.input['occupancy'] = 75
    congestion_measure.input['meanSpeed'] = 50
    # Crunch the numbers
    congestion_measure.compute()
    print(congestion_measure.output['congestion'])
    # congestion.view(sim=congestion_measure)

    return


def run():
    global my_detector_change
    global my_accident_change
    global neighbor_flow_change
    global neighbor_accident_change
    accident_lanes = []

    # Setup the controller
    congestion_measure, congestion = congestion_estimator_conf()
    split_control(congestion_measure, congestion)

    # Setup of the intersection
    inter_id = 2
    inter_info = intersections_info.Intersection(inter_id)
    inter_info.config()
    subscribe_neighbors(inter_info.neighbors)

    petri_net_inter, place_id, transition_id = inter_tpn.net_create(inter_info.movements, inter_info.phases,
                                                                    inter_info.cycles, inter_info.cycles_names)
    petri_net_snake = net_snakes.net_snakes_create(petri_net_inter)

    init = petri_net_snake.get_marking()
    print(init)

    # "petri_net_snake.set_marking(init)" Acts like n.reset(), because each transition has a place in its pre-set whose
    # marking is reset, just like for method reset
    petri_net_snake.set_marking(init)
    time_0 = time.perf_counter()
    time_current = 0.0
    delay = 0.0
    step = 1.0

    print("\n\nStart the Intersection Petri Net:")
    while True:

        # initialize variables for semaphore msg configuration
        l_change = False
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
        for i in transitions_fire:
            if "Green" in i:
                print("Voy a poner en GREEN el Movimiento %s" % i[-1])
                l_change = True
                for j in inter_info.m_lights[0][int(i[-1])]:
                    inter_info.lights[j] = "G"
            elif "Yel" in i:
                print("Voy a poner en YELLOW el Movimiento %s" % i[-1])
                l_change = True
                for j in inter_info.m_lights[0][int(i[-1])]:
                    inter_info.lights[j] = "y"
            elif "Red" in i:
                print("Voy a poner en RED el Movimiento %s" % i[-1])
                l_change = True
                for j in inter_info.m_lights[0][int(i[-1])]:
                    inter_info.lights[j] = "r"

        # Send control msg to simulation
        if l_change:
            control_msg = {
                "tlsID": inter_info.tlsID,
                "type": "tlsControl",
                "command": "setPhase",
                "data": "".join(inter_info.lights)
            }

            client_intersection.publish(inter_info.tlsID, json.dumps(control_msg))
            print("send: " + json.dumps(control_msg))

        # # Add accident in B at t = 30
        # if time_current == 30:
        #     petri_net_snake.place("Normal_to_AccEO").add(dot)
        # # Remove accident in B at t = 60
        # if time_current == 60:
        #     petri_net_snake.place("AccEO_to_Normal").add(dot)

        # Add accident in B at t = 30
        if time_current == 30:
            global msg_dic
            my_accident_change = True
            msg_dic = {
                "id": "intersection/0002/e2det/s03",
                "type": "AccidentObserved",
                "laneId": "436291016#3_3",
                "location": "here",
                "dateObserved": datetime.datetime.utcnow().isoformat(),
                "accidentOnLane": True,
                "laneDirection": "s-_wn_"
            }
        # Remove accident in B at t = 60
        if time_current == 300:
            my_accident_change = True
            msg_dic = {
                "id": "intersection/0002/e2det/s03",
                "type": "AccidentObserved",
                "laneId": "436291016#3_3",
                "location": "here",
                "dateObserved": datetime.datetime.utcnow().isoformat(),
                "accidentOnLane": False,
                "laneDirection": "s-_wn_"
            }

        # Manage Split

        # Manage accidents
        if my_accident_change or neighbor_accident_change:
            manage_accidents(petri_net_snake, inter_info.neighbors, accident_lanes)

        # Wait for a second to transit
        time_current += 1.0
        while time.perf_counter() < time_0 + time_current:
            pass
        # Update the network time
        delay = petri_net_snake.time(step)


if __name__ == '__main__':
    client_intersection: mqtt.Client = mqtt_conf()
    client_intersection.loop_start()    # Necessary to maintain connection
    run()
