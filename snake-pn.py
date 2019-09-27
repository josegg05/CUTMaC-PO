import tpn
import intersection
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


# petri_net_inter = petri_net_intersection_create()
movements = [0, 1, 2, 3, 4, 5, 6, 7]
phases = [[0, 4], [0, 5], [1, 4], [1, 5], [2, 6], [2, 7], [3, 6], [3, 7]]
cycles = pd.Series(data=[[1, 2, 3, 4, 5, 6, 7, 0],
                         [2, 2, 3, 4, 5, 2, 2, 2],
                         [1, 5, 0, 0, 0, 7, 0, 0],
                         [1, 3, 1, 4, 6, 1, 1, 1],
                         [2, 0, 6, 0, 0, 0, 7, 0]],
                   index=["Normal", "AccA", "AccB", "AccC", "AccD"])
petri_net_inter, place_id, transition_id = intersection.net_create(movements, phases, cycles)
petri_net_snake = net_snakes_create(petri_net_inter)

init = petri_net_snake.get_marking()
print(init)

petri_net_snake.set_marking(init)  # Acts like n.reset(), because each transition has a place in its pre-set whose marking is reset, just like for method reset
clock = 0.0
for i in range(100):
    print(" , ".join("%s[%s,%s]=%s" % (t, t.min_time, t.max_time,
                                       "#" if t.time is None else t.time)
                     for t in petri_net_snake.transition()))
    for j in range(1):
        delay = petri_net_snake.time()
        print("[%s]" % clock, "delay:", delay)
        if delay:
            clock += delay
    for t in petri_net_snake.transition():
        try:
            petri_net_snake.transition(t.name).fire(Substitution())
            print("[%s] fire: %s" % (clock, t.name))
        except:
            h = 0
            #print("Unexpected error:", sys.exc_info()[0])
