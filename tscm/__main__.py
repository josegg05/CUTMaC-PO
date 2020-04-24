from petri_nets import tpn
from petri_nets import inter_tpn_v2
from petri_nets import net_snakes
from petri_nets import intersections_classes
import snakes.plugins
import time
import paho.mqtt.client as mqtt
import json
import zmq
import sys

snakes.plugins.load(tpn, "snakes.nets", "snk")
from snk import *

# Define the global variable of command_received
intersection_id = ""
start_flag = False
msg_dic = []


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("intersection/all/start")


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
        print("message arrive from topic: " + msg.topic + " " + str(msg.payload))


def mqtt_conf() -> mqtt.Client:
    broker_address = "localhost"  # PC Office: "192.168.0.196"; PC Lab: "192.168.5.95"
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker_address)  # connect to broker
    return client


def pub_zmq_config(port):
    context = zmq.Context()
    sock = context.socket(zmq.PUB)
    sock.bind("tcp://127.0.0.1:%s" % port)
    time.sleep(0.5)
    return sock


def sub_zmq_config(port):
    context = zmq.Context()
    print("Connecting to server on port %s" % port)
    sock = context.socket(zmq.SUB)
    sock.connect("tcp://127.0.0.1:%s" % port)
    sock.setsockopt(zmq.SUBSCRIBE, b"super/tscm/command")
    time.sleep(0.5)
    return sock


def poller_config(socket):
    poller = zmq.Poller()
    if len(socket) > 1:
        for sock in socket:
            poller.register(sock, zmq.POLLIN)
    else:
        poller.register(socket[0], zmq.POLLIN)
    return poller


def set_tls_lights(transitions_fire, inter_info, mv_displays, cycle):
    l_change = False
    moves_displays = mv_displays
    for transition in transitions_fire:
        if "tGreen" in transition:
            print("Voy a poner en GREEN el Movimiento %s" % transition[-1])
            l_change = True
            moves_displays[int(transition[-1])] = "G"
            for j in inter_info.m_lights[cycle][int(transition[-1])]:
                inter_info.lights[j] = "G"
        elif "tYel" in transition:
            print("Voy a poner en YELLOW el Movimiento %s" % transition[-1])
            l_change = True
            moves_displays[int(transition[-1])] = "y"
            for j in inter_info.m_lights[cycle][int(transition[-1])]:
                inter_info.lights[j] = "y"
        elif "tRed" in transition:
            print("Voy a poner en RED el Movimiento %s" % transition[-1])
            l_change = True
            moves_displays[int(transition[-1])] = "r"
            for j in inter_info.m_lights[cycle][int(transition[-1])]:
                inter_info.lights[j] = "r"

    # Set control msg to simulation
    if l_change:
        control_msg = {
            "tls_id": inter_info.tls_id,
            "type": "tlsControl",
            "command": "setPhase",
            "data": "".join(inter_info.lights)
        }

        display_state_msg = {
            "id": inter_info.tls_id,
            "type": "stateChange",
            "category": {
                "value": ["display"]
            },
            "state": {
                "value": moves_displays
            }
        }
    else:
        control_msg = {}
        display_state_msg = {}

    return moves_displays, display_state_msg, control_msg


def config_mov_split(petri_net_snake, mov_splits):
    for mov in mov_splits:
        transition_name = "tAct_" + str(mov)
        petri_net_snake.transition(transition_name).min_time = mov_splits[mov]
        print("tAct_" + str(mov) + "_time = ",  mov_splits[mov])
    return


def config_cycle(petri_net_snake, cycle_name):
    if not petri_net_snake.place(cycle_name).tokens:
        petri_net_snake.place("C" + cycle_name).add(dot)
    return


def set_phase_state(transition, phases_state, id):
    print("Start Process to change to next Phase --> %s" % transition[-1])
    phases_state[int(transition[-2])] = 0
    phases_state[int(transition[-1])] = 1

    phase_state_msg = {
        "id": id,
        "type": "stateChange",
        "category": {
            "value": ["phase"]
        },
        "state": {
            "value": phases_state
        }
    }
    return phase_state_msg, phases_state


def run():
    global intersection_id
    global start_flag
    global msg_dic

    super_topic_display = b"tscm/state"
    super_topic_phase = b"tscm/state"

    # Setup of the intersection
    inter_info = intersections_classes.Intersection(intersection_id)
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

    # Set initial Cycle
    cycle = 0

    # Set initial phases_state
    phases_state = [0, 0, 0, 0, 0, 0, 0, 0]
    for place in petri_net_inter.places:
        if "P" in place[0] and place[0] is not "PTC":
            print(place)
            #phases_state[place[0][-1]] = (int(place[4]))  # Markings
            phases_state[int(place[0][-1])] = (int(place[4]))  # Markings
    print("Phases states are: ", phases_state)

    # Create intersection Movements displays
    moves_displays_state = ["r", "r", "r", "r", "r", "r", "r", "r"]

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

        # Measure congestion and split of correspondent Movement
        for transition in transitions_fire:
            if "t1_" in transition:  # A Phase Transition t1_xy fires
                phase_state_msg, phases_state = set_phase_state(transition, phases_state.copy(), inter_info.tls_id)
                # Done: TODO: Send state_msg to supervisor
                pub_socket.send_multipart([super_topic_phase, json.dumps(phase_state_msg).encode()])

        # Set the TS displays
        moves_displays_state, display_state_msg, control_msg = set_tls_lights(transitions_fire, inter_info, moves_displays_state.copy(), cycle)
        if control_msg:
            client_intersection.publish(inter_info.tls_id, json.dumps(control_msg))
            print("send: ", control_msg)
        # Done: TODO: Send display_state_msg to supervisor
        if display_state_msg:
            pub_socket.send_multipart([super_topic_display, json.dumps(display_state_msg).encode()])



        # Done: TODO: Make the zmq msgs receiver
        poll = dict(poller.poll(20))
        if sub_socket in poll and poll[sub_socket] == zmq.POLLIN:
            [top, contents] = sub_socket.recv_multipart()
            msg_zmq = json.loads(contents.decode())
            if b"command" in top:
                if msg_zmq["type"] == "config" and "split" in msg_zmq["category"]["value"]:
                    config_mov_split(petri_net_snake, msg_zmq["value"]["value"])
                elif msg_zmq["type"] == "config" and "cycle" in msg_zmq["category"]["value"]:
                    config_cycle(petri_net_snake, msg_zmq["value"]["value"][0])

        # Wait for a second to transit
        time_current += 1.0
        while time.perf_counter() < time_0 + time_current:
            pass
        # Update the network time
        # print("step = ", step)
        delay = petri_net_snake.time(step)


if __name__ == '__main__':
    with open("inter_id.txt", "r") as f:
        intersection_id = f.read()
    print("Intersection_ID: ", intersection_id)
    client_intersection = mqtt_conf()
    # client_intersection: mqtt.Client = mqtt_conf()
    client_intersection.loop_start()  # Necessary to maintain connection
    pub_socket = pub_zmq_config("5557")
    sub_socket = sub_zmq_config("5558")
    poller = poller_config([sub_socket])
    run()
