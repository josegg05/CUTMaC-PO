from cutmapnet.petri_nets import tpn
from cutmapnet.petri_nets import inter_tpn
from cutmapnet.petri_nets import net_snakes
import snakes.plugins
import time
import paho.mqtt.client as mqtt

snakes.plugins.load(tpn, "snakes.nets", "snk")
from snk import *


# from cutmapnet import intersection

def mqtt_conf() -> mqtt.Client:
    broker_address = "192.168.5.95"  # "192.168.1.95"
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


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


def run():
    # movements = [0, 1, 2, 3, 4, 5, 6, 7]
    # phases = [[0, 4], [0, 5], [1, 4], [1, 5], [2, 6], [2, 7], [3, 6], [3, 7]]
    # cycles = [[1, 2, 3, 4, 5, 6, 7, 0],
    #           [2, 2, 3, 4, 5, 2, 2, 2],
    #           [1, 5, 0, 0, 0, 7, 0, 0],
    #           [1, 3, 1, 4, 6, 1, 1, 1],
    #           [2, 0, 6, 0, 0, 0, 7, 0]]
    # cycles_names = ["Normal", "AccA", "AccB", "AccC", "AccD"]

    # Setup of the intersection
    movements = [0, 1, 3, 4, 5, 7]
    m_lights = [[2], [], [], [3, 4, 5, 6], [], [0, 1], [], []]  # Lights associated with every movement
    phases = [[3, 7], [0, 5], [0, 4], [1, 5]]
    # lights = [["rrrGGGG", "rrryyyy"], ["GGGrrrr", "yyyrrrr"], ["rrGrrrr", "rryrrrr"], ["GGrrrrr", "yyrrrrr"], ["rrrrrrr"]]
    lights = list("rrrrrrr")
    cycles = [[1, 0, 0, 0],
              [2, 0, 0, 0],
              [3, 0, 0, 0]]
    cycles_names = ["Normal", "AccA", "AccB"]

    petri_net_inter, place_id, transition_id = inter_tpn.net_create(movements, phases, cycles, cycles_names)
    petri_net_snake = net_snakes.net_snakes_create(petri_net_inter)

    init = petri_net_snake.get_marking()
    print(init)

    petri_net_snake.set_marking(
        init)  # Acts like n.reset(), because each transition has a place in its pre-set whose marking is reset,
    # just like for method reset
    time_0 = time.perf_counter()
    time_current = 0.0
    delay = 0.0
    step = 1.0

    # green = []
    # yellow = []
    # red = []

    print("\n\nStart the Intersection Petri Net:")
    while True:
        g_current = []
        y_current = []
        r_current = []
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
            # if count_fire == 0:
            #     print(" , ".join("%s[%s,%s]=%s" % (t, t.min_time, t.max_time,
            #                                        "#" if t.time is None else t.time)
            #                      for t in petri_net_snake.transition()))
            for t in petri_net_snake.transition():
                try:
                    petri_net_snake.transition(t.name).fire(Substitution())
                    p_fire = True
                    count_fire += 1
                    transitions_fire.append(str(t.name))
                    if "Green" in t.name:
                        print("Voy a poner en GREEN el Movimiento %s" % t.name[-1])
                        g_current.append(t.name[-1])
                    elif "Yel" in t.name:
                        print("Voy a poner en YELLOW el Movimiento %s" % t.name[-1])
                        y_current.append(t.name[-1])
                    elif "Red" in t.name:
                        print("Voy a poner en RED el Movimiento %s" % t.name[-1])
                        r_current.append(t.name[-1])
                    print("[%s] fire: %s, count_fire: %s" % (time_current, t.name, count_fire))
                except:
                    pass

        #print(transitions_fire)
        for i in transitions_fire:
            if "Green" in i:
                l_change = True
                for j in m_lights[int(i[-1])]:
                    lights[j] = "G"
            elif "Yel" in i:
                l_change = True
                for j in m_lights[int(i[-1])]:
                    lights[j] = "y"
            elif "Red" in i:
                l_change = True
                for j in m_lights[int(i[-1])]:
                    lights[j] = "r"

        if l_change:
            print("send: " + "".join(lights))

        # if not green and g_current:
        #     green = g_current
        # if not yellow and y_current:
        #     yellow = y_current
        # if not red and r_current:
        #     red = r_current
        #
        # if len(g_current) or len(y_current) or len(r_current) > 2:
        #     print("error en la net!!! SALIR")
        # elif len(g_current) == 1:
        #     print()
        # elif len(g_current) == 2:
        #     green = g_current
        #     print()
        # elif len(y_current) == 1:
        #     print()
        # elif len(y_current) == 2:
        #     yellow = y_current
        #     print()
        # elif len(r_current) == 1:
        #     print()
        # elif len(r_current) == 2:
        #     red = r_current
        #     print()

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


if __name__ == '__main__':
    # client_intersection: mqtt.Client = mqtt_conf()
    # intersection.run()
    run()
