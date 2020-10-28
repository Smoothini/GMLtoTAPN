import networkx as nx
import random
import json
from copy import deepcopy
from entities.Node import Node
from entities.Transition import Transition
from entities.Arcs import Full_Arc, Outbound_Arc, Inbound_Arc
import JsonParser as jsonParser

# Settings
network = "Arpanet19723"
G = nx.read_gml("archive/" + network + '.gml', label='id')
f = open(network + "_v5.tapn", "w")

nodes = []
transitions = []
waypoint_count = 2
waypoints = []

controller = Node(-1, "Controller")


def parse_nodes():
    nodes_raw = list(G.nodes(data=True)

    for i in nodes_raw:
        n = Node(i[0], "P{}".format(i[0]))
        nodes.append(n)


def info_nodes(nodes_list):
    for i in nodes_list:
        i.info()


# Gets a node object by id
def get_node(node_id):
    return next((x for x in nodes if x.id == node_id), None)


def parse_transitions():
    edges_raw = list(G.edges)
    for i in edges_raw:
        t = Transition(edges_raw.index(i), i[0], i[1], "T{}_{}".format(i[0], i[1]))
        transitions.append(t)


def info_transitions(transitions_list):
    for i in transitions_list:
        i.info()


def initialize_network():
    parse_nodes()
    parse_transitions()
    # Info methods can be used for verifications and such
    # but I tested on few networks and had no issues so far
    # info_nodes(nodes)
    # info_transitions(transitions)


# Works
def write_basic_network():
    # Network Contents
    f.write(controller.shared_to_file())
    for transition in transitions:
        f.write(transition.shared_to_file())
    f.write("  <net active=\"true\" id=\"{}\" type=\"P/T net\">\n".format(network))
    f.write(
        "    <labels border=\"true\" height=\"86\" positionX=\"0\" positionY=\"0\" width=\"179\">Network: {}\nNode Count: {}\nTransition Count: {}\n\nPress Shift+D followed by Enter</labels>\n"
        .format(network, len(nodes), len(transitions)))
    for node in nodes:
        f.write(node.to_file())
    for transition in transitions:
        f.write(transition.to_file())

    arcs = []
    for t in transitions:
        a = Full_Arc(get_node(t.source), get_node(t.target), t)
        arcs.append(a)
    for arc in arcs:
        f.write(arc.to_file())
    f.write("  </net>\n")


# Works
def write_waypoints(wp_count):
    waypoints = deepcopy(random.sample(nodes, wp_count))
    for node in waypoints:
        node.notation += "_visited"

        f.write("  <net active=\"true\" id=\"{}\" type=\"P/T net\">\n"
                .format(node.notation))
        f.write(
            "    <place displayName=\"true\" id=\"{}\" initialMarking=\"0\" invariant=\"&lt; inf\" name=\"{}\" nameOffsetX=\"-5.0\" nameOffsetY=\"35.0\" positionX=\"{}\" positionY=\"{}\"/>\n"
            .format(node.notation, node.notation, 100, 100))
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
            f.write(t.to_file())

        wp_arcs = []
        for t in wp_transitions:
            a = Outbound_Arc(t, node)
            wp_arcs.append(a)
        for arc in wp_arcs:
            f.write(arc.to_file())

        f.write("  </net>\n")


# In progress
# Missing only the arcs between the main controller and the partial component controller thingie each place has
# Guess that can be made after we define our Json format
def write_switches():

    for node in nodes:
        f.write("  <net active=\"true\" id=\"{}_Controller\" type=\"P/T net\">\n"
                .format(node.notation))
        f.write("<place displayName=\"true\" id=\"{}\" initialMarking=\"0\" invariant=\"&lt; inf\" name=\"{}\" "
                "nameOffsetX=\"-5.0\" nameOffsetY=\"35.0\" positionX=\"{}\" positionY=\"{}\"/>\n "
                .format(controller.notation, controller.notation, 100, 100))

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
                n = Node("P{}_{}_active".format(t.source, t.target), "P{}_{}_active".format(t.source, t.target))
                n.x = x
                n.y = y
                update_nodes.append(n)

                t.x = x + 100
                t.y = y

                y += 100
                update_transitions.append(t)

        for n in update_nodes:
            f.write(n.to_file())
        f.write(update_transition.to_file())
        for t in update_transitions:
            f.write(t.to_file())

        in_arc = Inbound_Arc(controller, update_transition)
        out_arc = Outbound_Arc(update_transition, controller)
        f.write(in_arc.to_file())
        f.write(out_arc.to_file())

        for i in range(len(update_nodes)):
            in_arc = Inbound_Arc(update_nodes[i], update_transitions[i])
            out_arc = Outbound_Arc(update_transitions[i], update_nodes[i])

            ##Another Inbound or Outbound arc could be generated here based on the JSON for the pathing

            f.write(in_arc.to_file())
            f.write(out_arc.to_file())

        f.write("  </net>\n")


def write_to_file():
    # Start of File
    f.write("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n")
    f.write("<pnml xmlns=\"http://www.informatik.hu-berlin.de/top/pnml/ptNetb\">\n")

    # Initial state of the network
    write_basic_network()

    # Other components
    write_waypoints(waypoint_count)
    write_switches()

    # End of File
    f.write("  <k-bound bound=\"3\"/>\n")
    f.write("</pnml>")
    f.close()
    print("Success")


initialize_network()
write_to_file()
