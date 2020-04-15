def net_romeo_graph(file_name, petri_net):
    file = open(file_name, "a")
    # petri_net.places.set_index("name", inplace=True)
    # petri_net.transitions.set_index("name", inplace=True)
    for x in range(len(petri_net.places) - 1):
        place = [
            ' <place id="%d" identifier="%s" label="%s" initialMarking="%d" eft="0" lft="inf">\n' % (
                petri_net.places[x+1][-1], petri_net.places[x+1][0], petri_net.places[x+1][0], petri_net.places[x+1][4]),
            '    <graphics color="%d">\n' % petri_net.places[x+1][1],
            '       <position x="%d" y="%d"/>\n' % (
                petri_net.places[x+1][2], petri_net.places[x+1][3]),
            '       <deltaLabel deltax="10" deltay="10"/>\n',
            '    </graphics> \n',
            '    <scheduling gamma="0" omega="0"/> \n',
            ' </place> ]\n\n']
        file.writelines(place)
        # print(p_ids_array)

    for x in range(len(petri_net.transitions) - 1):
        transition = [
            ' <transition id="%d" identifier="%s" label="%s"  eft="%d" lft="inf" speed="1" cost="0" unctrl="0" obs="1"  guard="">\n' % (
                petri_net.transitions[x+1][-1], petri_net.transitions[x+1][0],
                petri_net.transitions[x+1][0], petri_net.transitions[x+1][4],
                ),
            '    <graphics color="%d">\n' % petri_net.transitions[x+1][1],
            '       <position x="%d" y="%d"/>\n' % (
                petri_net.transitions[x+1][2], petri_net.transitions[x+1][3]),
            '       <deltaLabel deltax="25" deltay="0"/>\n',
            '       <deltaGuard deltax="20" deltay="-20"/>\n',
            '       <deltaUpdate deltax="20" deltay="10"/>\n',
            '       <deltaSpeed deltax="-20" deltay="5"/>\n',
            '       <deltaCost deltax="-20" deltay="5"/>\n',
            '    </graphics>\n',
            '    <update><![CDATA[]]></update>\n',
            ' </transition>\n\n']
        file.writelines(transition)

        #if petri_net.transitions[x+1][6] != "NaN":
        a_transition = petri_net.transitions[x+1][-1]
        arcs_in_t = list(petri_net.transitions[x+1][6])
        for place_in in arcs_in_t:
            if "*" in place_in:
                place_in = place_in.replace("*", "")
                type = "logicalInhibitor"
            else:
                type = "PlaceTransition"
            for z in petri_net.places:
                if z[0] == place_in:
                    a_place = z[-1]
            arc = [
                '<arc place="%d" transition="%d" type="%s" weight="1" inhibitingCondition ="">\n' % (
                    a_place, a_transition, type),
                ' <nail xnail="0" ynail="0"/>\n',
                ' <graphics color="0">\n',
                ' </graphics>\n',
                '</arc>\n\n\n', ]
            file.writelines(arc)

        arcs_out_t = list(petri_net.transitions[x+1][7])
        for place_out in arcs_out_t:
            for z in petri_net.places:
                if z[0] == place_out:
                    a_place = z[-1]
            arc = [
                '<arc place="%d" transition="%d" type="TransitionPlace" weight="1">\n' % (
                    a_place, a_transition),
                ' <nail xnail="0" ynail="0"/>\n',
                ' <graphics color="0">\n',
                ' </graphics>\n',
                '</arc>\n\n\n', ]
            file.writelines(arc)

    file.close()
    return 0
