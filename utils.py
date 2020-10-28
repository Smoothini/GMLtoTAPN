import networkx as nx

import JsonParser as jsonParser
from entities.Arcs import Full_Arc, Outbound_Arc, Inbound_Arc
from entities.Node import Node
from entities.Transition import Transition




def parse_nodes(G, routing):
    nodes = []
    nodes_raw = list(G.nodes(data=True))
    for i in nodes_raw:
        if i[0] in routing:
            n = Node(i[0], "P{}".format(i[0]))
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


def initialize_network(G, initial_routing: str, final_routing: str):
    nodes_from_routing = set.union(
        jsonParser.get_nodes_from_routing(jsonParser.get_initial_routing(initial_routing)),
        jsonParser.get_nodes_from_routing(jsonParser.get_final_routing(final_routing))
    )

    routing = jsonParser.get_routings(jsonParser.final_route)
    routing.extend(jsonParser.get_routings(jsonParser.init_route))

    nodes2 = parse_nodes(G, nodes_from_routing)
    transitions2 = parse_transitions(routing)
    # Info methods can be used for verifications and such
    # but I tested on few networks and had no issues so far
    # info_nodes(nodes)
    # info_transitions(transitions)
    return nodes2, transitions2


# Works
def write_basic_network(network, nodes: list, transitions: list):
    # Network Contents
    controller = Node(-1, "Controller")
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
        node.notation += "_visited"

        xml_str += f"  <net active=\"true\" id=\"{node.notation}\" type=\"P/T net\">\n"
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


def write_switches(nodes: list, transitions: list):
    controller = Node(-1, "Controller")
    xml_str = ""
    for node in nodes:
        xml_str += f"  <net active=\"true\" id=\"{node.notation}_Controller\" type=\"P/T net\">\n"

        xml_str += f"<place displayName=\"true\" id=\"{controller.notation}\" initialMarking=\"0\" invariant=\"&lt; inf\" name=\"{controller.notation}\" nameOffsetX=\"-5.0\" nameOffsetY=\"35.0\" positionX=\"{100}\" positionY=\"{100}\"/>\n "

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

        xml_str += "  </net>\n"
    return xml_str


def write_LoopFreedom(nodes: list, transitions: list):
    xml_str = ""
    for node in nodes:
        node.notation += "_loopFreedom"
        xml_str += f"  <net active=\"true\" id=\"{node.notation}\" type=\"P/T net\">\n"

        xml_str += f"    <place displayName=\"true\" id=\"{node.notation}\" initialMarking=\"0\" invariant=\"&lt; " \
                   f"inf\" name=\"{node.notation}\" nameOffsetX=\"-5.0\" nameOffsetY=\"35.0\" positionX=\"{100}\" " \
                   f"positionY=\"{100}\"/>\n "
        x = 200
        y = 50
        inbound_t = []
        for t in transitions:
            if t.target == node.id:
                t.x = x
                t.y = y
                inbound_t.append(t)
                y += 100
        for t in inbound_t:
            xml_str += t.to_file()
        outbound_t = []
        for t in transitions:
            if node.id == t.source:
                t.x = x
                t.y = y
                outbound_t.append(t)
                y += 100
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


def write_to_file(network, properties):
    # Start of File
    G = nx.read_gml("archive/" + network + '.gml', label='id')
    f = open(network + "_v5.tapn", "w")
    f.write("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n")
    f.write("<pnml xmlns=\"http://www.informatik.hu-berlin.de/top/pnml/ptNetb\">\n")
    nodes2, transitions2 = initialize_network(G, "Initial_routing.json", "Final_routing.json")
    # Initial state of the network
    f.write(write_basic_network(network, nodes2, transitions2))
    print(write_basic_network(network, nodes2, transitions2))
    # Other components
    if len(properties["waypointNodeIds"]) > 0:
        f.write(write_waypoints(nodes2, transitions2, properties["waypointNodeIds"]))
    if properties["LoopFreedom"]:
        f.write(write_LoopFreedom(nodes2, transitions2))
    f.write(write_switches(nodes2, transitions2))
    # End of File
    f.write("  <k-bound bound=\"3\"/>\n")
    f.write("</pnml>")
    f.close()
    print("Success")


write_to_file("Arpanet19723", jsonParser.get_properties("properties.json"))
