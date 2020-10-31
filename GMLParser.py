import networkx as nx

from entities.Arcs import Full_Arc, Outbound_Arc, Inbound_Arc
from entities.Node import Node
from entities.Transition import Transition

import JsonParser

network = "Arpanet19723"

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