from cutmapnet.petri_nets import tpn
import snakes.plugins

snakes.plugins.load(tpn, "snakes.nets", "snk")
from snk import *

def net_snakes_create(petri_net):
    petri_snake = PetriNet("CUTMaPNet")
    # petri_net.places.set_index("name", inplace=True)
    # petri_net.transitions.set_index("name", inplace=True)
    for x in range(len(petri_net.places) - 1):
        m0 = []
        for y in range(petri_net.places[x+1][4]):   # "M0"
            m0.append(dot)
        petri_snake.add_place(Place(petri_net.places[x+1][0], m0))
    for x in range(len(petri_net.transitions) - 1):
        # print(x)
        petri_snake.add_transition(Transition(petri_net.transitions[x+1][0], min_time=petri_net.transitions[x+1][4]))   # "time"

        if petri_net.transitions[x+1][5] != "NaN":  # "arcs_in"
            arcs_in_t = list(petri_net.transitions[x+1][5])     # "arcs_in"
            for y in range(len(arcs_in_t)):
                if "*" not in arcs_in_t[y]:
                    petri_snake.add_input(arcs_in_t[y], petri_net.transitions[x+1][0], Value(dot))
            arcs_out_t = list(petri_net.transitions[x+1][6])    # "arcs_out"
            for y in range(len(arcs_out_t)):
                if "*" not in arcs_out_t[y]:
                    petri_snake.add_output(arcs_out_t[y], petri_net.transitions[x+1][0], Value(dot))
    return petri_snake