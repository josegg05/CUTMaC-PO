from snakes.nets import *
n = PetriNet('First net')
n.add_place(Place('p', [0]))
n.add_transition(Transition('t', Expression('x<5')))
n.add_input('p', 't', Variable('x'))
n.add_output('p', 't', Expression('x+1'))

modes = n.transition('t').modes()
print(modes)

n.transition('t').fire(Substitution(x=0))

state = n.get_marking()
print(state)