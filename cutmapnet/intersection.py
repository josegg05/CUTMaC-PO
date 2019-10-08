from cutmapnet.petri_nets import tpn
from cutmapnet.petri_nets import inter_tpn
from cutmapnet.petri_nets import net_snakes
import snakes.plugins
import time
import paho.mqtt.client as mqtt

snakes.plugins.load(tpn, "snakes.nets", "snk")
from snk import *


# def net_snakes_create(petri_net):
#     petri_snake = PetriNet("CUTMaPNet")
#     # petri_net.places.set_index("name", inplace=True)
#     # petri_net.transitions.set_index("name", inplace=True)
#     for x in list(petri_net.places.index.values):
#         m0 = []
#         for y in range(petri_net.places.loc[x]["M0"]):
#             m0.append(dot)
#         petri_snake.add_place(Place(x, m0))
#     for x in list(petri_net.transitions.index.values):
#         # print(x)
#         petri_snake.add_transition(Transition(x, min_time=petri_net.transitions.loc[x]["time"]))
#
#         if petri_net.transitions.loc[x]["arcs_in"] != "NaN":
#             arcs_in_t = list(petri_net.transitions.loc[x]["arcs_in"])
#             for y in range(len(arcs_in_t)):
#                 if "*" not in arcs_in_t[y]:
#                     petri_snake.add_input(arcs_in_t[y], x, Value(dot))
#             arcs_out_t = list(petri_net.transitions.loc[x]["arcs_out"])
#             for y in range(len(arcs_out_t)):
#                 if "*" not in arcs_out_t[y]:
#                     petri_snake.add_output(arcs_out_t[y], x, Value(dot))
#     return petri_snake


# petri_net_inter = petri_net_intersection_create()

def mqtt_conf() -> mqtt.Client:
    broker_address = "192.168.5.95"   # "192.168.1.95"
    # broker_address="iot.eclipse.org" # use external broker
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker_address)  # connect to broker
    return client


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("intersection/0002/tls")
    client.subscribe("intersection/0003/tls")
    client.subscribe("intersection/0004/tls")
    client.subscribe("intersection/0005/tls")
    client.subscribe("intersection/0006/tls")
    client.subscribe("intersection/0007/tls")
    client.subscribe("intersection/0008/tls")
    client.subscribe("intersection/0009/tls")
    client.subscribe("intersection/00010/tls")
    client.subscribe("intersection/00011/tls")
    client.subscribe("intersection/00012/tls")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

def run():
    movements = [0, 1, 2, 3, 4, 5, 6, 7]
    phases = [[0, 4], [0, 5], [1, 4], [1, 5], [2, 6], [2, 7], [3, 6], [3, 7]]
    cycles = [[1, 2, 3, 4, 5, 6, 7, 0],
              [2, 2, 3, 4, 5, 2, 2, 2],
              [1, 5, 0, 0, 0, 7, 0, 0],
              [1, 3, 1, 4, 6, 1, 1, 1],
              [2, 0, 6, 0, 0, 0, 7, 0]]
    cycles_names = ["Normal", "AccA", "AccB", "AccC", "AccD"]
    petri_net_inter, place_id, transition_id = inter_tpn.net_create(movements, phases, cycles, cycles_names)
    petri_net_snake = net_snakes.net_snakes_create(petri_net_inter)

    init = petri_net_snake.get_marking()
    print(init)

    petri_net_snake.set_marking(
        init)  # Acts like n.reset(), because each transition has a place in its pre-set whose marking is reset, just like for method reset
    time_0 = time.perf_counter()
    time_current = 0.0
    delay = 0.0
    step = 1.0

    print("\n\nStart the Intersection Petri Net:")
    while True:
        # Print the current time and delay
        print("Time:[%s] " % time_current, "delay:", delay)

        # Fires all the fireable transitions
        p_fire = True
        count_fire = 0
        while p_fire:
            p_fire = False
            # if count_fire == 0:
            #     print(" , ".join("%s[%s,%s]=%s" % (t, t.min_time, t.max_time,
            #                                        "#" if t.time is None else t.time)
            #                      for t in petri_net_snake.transition()))
            for t in petri_net_snake.transition():
                try:
                    petri_net_snake.transition(t.name).fire(Substitution())
                    p_fire = True
                    count_fire += 1
                    if "Green" in t.name:
                        print("Voy a poner en GREEN el Movimiento %s" % t.name[-1])
                    elif "Yel" in t.name:
                        print("Voy a poner en YELLOW el Movimiento %s" % t.name[-1])
                    elif "Red" in t.name:
                        print("Voy a poner en RED el Movimiento %s" % t.name[-1])
                    print("[%s] fire: %s, count_fire: %s" % (time_current, t.name, count_fire))
                except:
                    pass

        # Wait for a second to transit
        time_current += 1.0
        while time.perf_counter() < time_0 + time_current:
            pass
        # Update the network time
        delay = petri_net_snake.time(step)

        # Add accident in B at t = 30
        if time_current == 30:
            petri_net_snake.place("Normal_to_AccB").add(dot)
        # Remove accident in B at t = 60
        if time_current == 60:
            petri_net_snake.place("AccB_to_Normal").add(dot)

client: mqtt.Client = mqtt_conf()
run()
