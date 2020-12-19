from entities.Node import Node
from entities.Transition import Transition


def parse_nodes(g, routing, marking):
    nodes = []
    nodes_raw = list(g.nodes(data=True))
    controller_node = Node(-1, "Controller", "1")
    nodes.append(controller_node)
    for i in range(len(routing)):
            id = routing[i]
            n = Node(id, "P{}".format(id), marking)
            nodes.append(n)
    return nodes


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