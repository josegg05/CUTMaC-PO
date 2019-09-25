import tpn
import pandas as pd
import snakes.plugins
snakes.plugins.load(tpn, "snakes.nets", "snk")
from snk import *


class PetriNetInfo:
    def __init__(self):
        self.places = pd.DataFrame(columns=["name", "color", "x_pos", "y_pos", "M0", "id"])
        self.transitions = pd.DataFrame(
            columns=["name", "color", "x_pos", "y_pos", "time", "arcs_in", "arcs_out", "id"])
        self.arcs = []


def petri_net_intersection_create():
    p_id = 1
    t_id = 1
    petri_net = PetriNetInfo()

    p_ident = ["p1", "p2"]
    p_color_sem = [0, 1]
    p_pos_x_sem = [30, 40]
    p_pos_y_sem = [30, 30]
    m0 = [[dot], []]

    t_ident = ["t1"]
    t_color_sem = [0]
    t_pos_x_sem = [30]
    t_pos_y_sem = [30]
    t_time_sem = [20]

    arcs_in = ["p1"]
    arcs_out = ["p2"]
    for x in range(len(p_ident)):
        petri_net.places = petri_net.places.append(
            {'name': p_ident[x], 'color': p_color_sem[x], "x_pos": p_pos_x_sem[x],
             "y_pos": p_pos_y_sem[x], "M0": m0[x], "id": p_id}, ignore_index=True)
        p_id += 1

    petri_net.transitions = petri_net.transitions.append(
        {'name': t_ident[0], 'color': t_color_sem[0], "x_pos": t_pos_x_sem[0],
         "y_pos": t_pos_y_sem[0], "time": t_time_sem[0], "arcs_in": arcs_in, "arcs_out": arcs_out,
         "id": t_id}, ignore_index=True)
    t_id += 1

    return petri_net


def net_snakes_create(petri_net):
    petri_snake = PetriNet("CUTMaPNet")
    petri_net.places.set_index("name", inplace=True)
    petri_net.transitions.set_index("name", inplace=True)
    for x in list(petri_net.places.index.values):
        petri_snake.add_place(Place(x, petri_net.places.loc[x]["M0"]))
    for x in list(petri_net.transitions.index.values):
        print(x)
        petri_snake.add_transition(Transition(x, min_time=petri_net.transitions.loc[x]["time"]))

        if petri_net.transitions.loc[x]["arcs_in"] != "NaN":
            arcs_in_t = list(petri_net.transitions.loc[x]["arcs_in"])
            for y in range(len(arcs_in_t)):
                petri_snake.add_input(arcs_in_t[y], x, Value(dot))
            arcs_out_t = list(petri_net.transitions.loc[x]["arcs_out"])
            for y in range(len(arcs_out_t)):
                petri_snake.add_output(arcs_out_t[y], x, Value(dot))
    return petri_snake


petri_net_sem = petri_net_intersection_create()
petri_net_snake = net_snakes_create(petri_net_sem)

init = petri_net_snake.get_marking()
print(init)

petri_net_snake.set_marking(init) # Acts like n.reset(), because each transition has a place in its pre-set whose marking is reset, just like for method reset
clock = 0.0
for i in range(3) :
    print(" , ".join("%s[%s,%s]=%s" % (t, t.min_time, t.max_time,
                                       "#" if t.time is None else t.time)
                     for t in petri_net_snake.transition()))
    for j in range(3) :
        delay = petri_net_snake.time()
        print("[%s]" % clock, "delay:", delay)
        if delay:
            clock += delay
    for t in petri_net_snake.transition():
        print("[%s] fire: %s" % (clock, t.name))
        petri_net_snake.transition(t.name).fire(Substitution())