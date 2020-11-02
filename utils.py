import networkx as nx
import time

from entities.Arcs import Full_Arc, Outbound_Arc, Inbound_Arc
from entities.Node import Node
from entities.Transition import Transition

import JsonParser as jsonParser
import json


def parse_nodes(g, routing, marking):
    nodes = []
    nodes_raw = list(g.nodes(data=True))
    controller_node = Node(-1, "Controller", "1")
    nodes.append(controller_node)
    for i in nodes_raw:
        if i[0] in routing:
            n = Node(i[0], "P{}".format(i[0]), marking)
            nodes.append(n)
    return nodes


def info_nodes(nodes_list):
    for i in nodes_list:
        i.info()


def get_node(node_id, nodes):
    return next((x for x in nodes if x.id == node_id), None)


def parse_transitions(routing):
    transitions = []
    routing = removeDuplicates(routing)

    for i in routing:
        route_id = len(transitions) + 1
        source = i[0]
        target = i[1]
        label = "T{}_{}".format(source, target)

        t = Transition(route_id, source, target, label)
        transitions.append(t)
    return transitions


def removeDuplicates(lst):
    return [t for t in (set(tuple(i) for i in lst))]


def info_transitions(transitions_list):
    for i in transitions_list:
        i.info()


def initialize_network(g, initial_routing: str, final_routing: str):
    nodes_from_routing = jsonParser.unique_ids

    routing = jsonParser.final_route
    routing.extend(jsonParser.init_route)

    nodes2 = parse_nodes(g, nodes_from_routing, "0")
    transitions2 = parse_transitions(routing)
    return nodes2, transitions2


# Works
def write_basic_network(network, nodes: list, transitions: list):
    # Network Contents
    controller = Node(-1, "Controller", "1")
    xml_str = ""

    xml_str += controller.shared_to_file()
    for transition in transitions:
        xml_str += transition.shared_to_file()
    xml_str += "  <net active=\"true\" id=\"{}\" type=\"P/T net\">\n".format(network)
    xml_str += f"    <labels border=\"true\" height=\"86\" positionX=\"0\" positionY=\"0\" width=\"179\">Network: {network}\nNode Count: {len(nodes)}\nTransition Count: {len(transitions)}\n\nPress Shift+D followed by Enter</labels>\n"

    for node in nodes:
        xml_str += node.to_file()
    for transition in transitions:
        xml_str += transition.to_file()

    arcs = []
    for t in transitions:
        a = Full_Arc(get_node(t.source, nodes), get_node(t.target, nodes), t)
        arcs.append(a)

    # controller and inject packet
    inject = Transition(-2, nodes[0].id, nodes[1].id, "injectpacket", "1")
    xml_str += inject.to_file()
    aa = Full_Arc(get_node(inject.source, nodes), get_node(inject.target, nodes), inject)
    arcs.append(aa)
    # END

    for arc in arcs:
        xml_str += arc.to_file()

    xml_str += "  </net>\n"
    return xml_str


# Works
def write_waypoints(nodes, transitions: list, waypointlist: list):
    waypoints = []
    xml_str = ""
    for waypoint in waypointlist:
        if get_node(waypoint, nodes):
            waypoints.append(get_node(waypoint, nodes))
    for node in waypoints:

        xml_str += f"  <net active=\"true\" id=\"{node.notation}_waypoint\" type=\"P/T net\">\n"
        node.notation += "_visited"
        xml_str += f"    <place displayName=\"true\" id=\"{node.notation}\" initialMarking=\"0\" invariant=\"&lt; inf\" name=\"{node.notation}\" nameOffsetX=\"-5.0\" nameOffsetY=\"35.0\" positionX=\"{100}\" positionY=\"{100}\"/>\n"
        x = 200
        y = 50
        wp_transitions = []
        for t in transitions:
            if t.target == node.id:
                t.x = x
                t.y = y
                wp_transitions.append(t)
                y += 100
        for t in wp_transitions:
            xml_str += t.to_file()

        wp_arcs = []
        for t in wp_transitions:
            a = Outbound_Arc(t, node)
            wp_arcs.append(a)
        for arc in wp_arcs:
            xml_str += arc.to_file()

        xml_str += "  </net>\n"
    return xml_str

#no bueno
def write_switches(nodes: list, transitions: list):
    controller = Node(-1, "Controller", "1")
    xml_str = ""
    i = 0

    for node in nodes:
        update_transition = Transition("Update_{}".format(node.notation), controller, None,
                                       "Update_{}".format(node.notation))
        update_transition.x = 200
        update_transition.y = 100
        update_nodes = []
        update_transitions = []

        x = 300
        y = 100

        for t in transitions:
            if t.source == node.id:
                n = Node("P{}_{}_active".format(t.source, t.target), "P{}_{}_active".format(t.source, t.target),
                             "0")
                n.x = x
                n.y = y
                update_nodes.append(n)
                t.x = x + 100
                t.y = y
                y += 100
                update_transitions.append(t)

        # ensuring obsolete controller components won't be written to file
        if len(update_nodes) > 1:

            xml_str += f"  <net active=\"true\" id=\"{node.notation}_Switch\" type=\"P/T net\">\n"

            xml_str += f"<place displayName=\"true\" id=\"{controller.notation}\" initialMarking=\"1\" invariant=\"&lt; inf\" name=\"{controller.notation}\" nameOffsetX=\"-5.0\" nameOffsetY=\"35.0\" positionX=\"{100}\" positionY=\"{100}\"/>\n "

            for n in update_nodes:
                xml_str += n.to_file()
            xml_str += update_transition.to_file()
            for t in update_transitions:
                xml_str += t.to_file()

            in_arc = Inbound_Arc(controller, update_transition, "timed", "1")
            out_arc = Outbound_Arc(update_transition, controller)
            xml_str += in_arc.to_file()
            xml_str += out_arc.to_file()

            for i in range(len(update_nodes)):
                in_arc = Inbound_Arc(update_nodes[i], update_transitions[i], "timed", "1")
                out_arc = Outbound_Arc(update_transitions[i], update_nodes[i])

                ##Another Inbound or Outbound arc could be generated here based on the JSON for the pathing

                xml_str += in_arc.to_file()
                xml_str += out_arc.to_file()
                # f.write(controller_route.to_file())
            ir = jsonParser.init_route
            for i in range(len(ir)):
                if ir[i][0] == node.id:
                    init_route = Outbound_Arc(update_transition, n)
                    xml_str += (init_route.to_file())

            fr = jsonParser.final_route
            for i in range(len(fr)):
                if fr[i][0] == node.id:
                    final_route = Inbound_Arc(update_nodes[0], update_transition, "timed", "1")
                    xml_str += final_route.to_file()

            xml_str += "  </net>\n"
    return xml_str

#todo
def write_loopfreedom(nodes: list, transitions: list):
    xml_str = ""
    for node in nodes:
        x = 200
        y = 50
        inbound_t = []
        for t in transitions:
            if t.target == node.id:
                t.x = x
                t.y = y
                inbound_t.append(t)
                y += 100
        outbound_t = []
        for t in transitions:
            if node.id == t.source:
                t.x = x
                t.y = y
                outbound_t.append(t)
                y += 100

        if (len(inbound_t) > 0 and len(outbound_t) > 0):

            xml_str += f"  <net active=\"true\" id=\"{node.notation}_loopFree\" type=\"P/T net\">\n"

            xml_str += f"    <place displayName=\"true\" id=\"{node.notation}\" initialMarking=\"0\" invariant=\"&lt; " \
                       f"inf\" name=\"{node.notation}\" nameOffsetX=\"-5.0\" nameOffsetY=\"35.0\" positionX=\"{100}\" " \
                       f"positionY=\"{100}\"/>\n "
            for t in inbound_t:
                xml_str += t.to_file()
            for t in outbound_t:
                xml_str += t.to_file()
            # This for loop maps arcs from place to transitions
            inbound_arcs = []
            for t in inbound_t:
                a = Outbound_Arc(t, node)
                inbound_arcs.append(a)
            for arc in inbound_arcs:
                xml_str += arc.to_file()
            # this for loop maps arcs from transition to places.
            outbound_arcs = []
            for t in outbound_t:
                a = Inbound_Arc(node, t, "tapnInhibitor", "2")
                outbound_arcs.append(a)
            for arc in outbound_arcs:
                xml_str += arc.to_file()
            xml_str += "  </net>\n"
    return xml_str

#todo
def write_to_file(network, properties):
    # Start of File
    g = nx.read_gml("archive/" + network + '.gml', label='id')
    f = open(network + "_v6.tapn", "w")
    f.write("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n")
    f.write("<pnml xmlns=\"http://www.informatik.hu-berlin.de/top/pnml/ptNetb\">\n")
    nodes, transitions = initialize_network(g, jsonParser.init_route, jsonParser.final_route)
    # Initial state of the network
    #f.write(write_switches(nodes, transitions))
    f.write(write_basic_network(network, nodes, transitions))
    #print(write_basic_network(network, nodes, transitions))
    # Other components
    if len(properties["waypointNodeIds"]) > 0:
        f.write(write_waypoints(nodes, transitions, properties["waypointNodeIds"]))
    if properties["LoopFreedom"]:
        f.write(write_loopfreedom(nodes, transitions))

    # End of File
    f.write("  <k-bound bound=\"3\"/>\n")
    f.write("  <feature isGame=\"true\" isTimed=\"true\"/>")
    f.write("</pnml>")
    f.close()

start = time.time()
network = "Arpanet19723"
write_to_file(network, jsonParser.properties)
print("Success! {} converted! Execution time: {} seconds".format(network, (str(time.time()-start))[:5]))