#from snakes.nets import *

import snakes.plugins
snakes.plugins.load("gv", "snakes.nets", "nets")
from nets import *

n = PetriNet('First net')
n.add_place(Place('p', [0]))
n.add_transition(Transition('t', Expression('x<5')))
n.add_input('p', 't', Variable('x'))
n.add_output('p', 't', Expression('x+1'))

modes = n.transition('t').modes()
print(modes)
#n.draw("value-0.png")

n.transition('t').fire(Substitution(x=0))
state = n.get_marking()
print(state)

#for engine in ('neato', 'dot', 'circo', 'twopi', 'fdp'):
#    n.draw(',test-gv-%s.png' % engine, engine=engine)

# Draw the PN and the state graph
n.draw("value-1.png")
s = StateGraph(n)
s.build()
s.draw('test-gv-graph.png')

