from cutmapnet.petri_nets import tpn
import pandas as pd
import snakes.plugins

snakes.plugins.load(tpn, "snakes.nets", "snk")
from snk import *

def net_snakes_create(petri_net):
    petri_snake = PetriNet("CUTMaPNet")
    # petri_net.places.set_index("name", inplace=True)
    # petri_net.transitions.set_index("name", inplace=True)
    for x in list(petri_net.places.index.values):
        m0 = []
        for y in range(petri_net.places.loc[x]["M0"]):
            m0.append(dot)
        petri_snake.add_place(Place(x, m0))
    for x in list(petri_net.transitions.index.values):
        # print(x)
        petri_snake.add_transition(Transition(x, min_time=petri_net.transitions.loc[x]["time"]))

        if petri_net.transitions.loc[x]["arcs_in"] != "NaN":
            arcs_in_t = list(petri_net.transitions.loc[x]["arcs_in"])
            for y in range(len(arcs_in_t)):
                if "*" not in arcs_in_t[y]:
                    petri_snake.add_input(arcs_in_t[y], x, Value(dot))
            arcs_out_t = list(petri_net.transitions.loc[x]["arcs_out"])
            for y in range(len(arcs_out_t)):
                if "*" not in arcs_out_t[y]:
                    petri_snake.add_output(arcs_out_t[y], x, Value(dot))
    return petri_snake