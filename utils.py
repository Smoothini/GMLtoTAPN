import networkx as nx
import random

from copy import deepcopy
from entities.Node import Node
from entities.Transition import Transition
from entities.Arcs import Full_Arc, Outbound_Arc, Inbound_Arc
import JsonParser as jsonParser
import json

# Settings
network = "Arpanet19723"
G = nx.read_gml("archive/" + network + '.gml', label='id')
f = open(network + "_v5.tapn", "w")

nodes = []
transitions = []
waypoint_count = 2
waypoints = []

controller = Node(-1, "Controller")


def parse_nodes(routing):
    nodes_raw = list(G.nodes(data=True))
    for i in nodes_raw:
        if i[0] in routing:
            n = Node(i[0], "P{}".format(i[0]))
            nodes.append(n)


def info_nodes(nodes_list):
    for i in nodes_list:
        i.info()


# Gets a node object by id
def get_node(node_id):
    return next((x for x in nodes if x.id == node_id), None)


def parse_transitions(routing):
    #edges_raw = list(G.edges)

    #routing = lambda route: [route for route in (set(tuple(i) for i in routing))]
    routing = removeDuplicates(routing)

    for i in routing:
        route_id = len(transitions) + 1
        source = i[0]
        target = i[1]
        label = "T{}_{}".format(source, target)

        t = Transition(route_id, source, target, label)
        transitions.append(t)


def removeDuplicates(lst):
    return [t for t in (set(tuple(i) for i in lst))]

def info_transitions(transitions_list):
    for i in transitions_list:
        i.info()


def initialize_network():
    nodes_from_routing = set.union(
        jsonParser.get_nodes_from_routing(jsonParser.init_route),
        jsonParser.get_nodes_from_routing(jsonParser.final_route)
    )

    routing = jsonParser.get_routings(jsonParser.final_route)
    routing.extend(jsonParser.get_routings(jsonParser.init_route))

    parse_nodes(nodes_from_routing)
    parse_transitions(routing)
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

        in_arc = Inbound_Arc(controller, update_transition,"timed", "1")
        out_arc = Outbound_Arc(update_transition, controller)
        f.write(in_arc.to_file())
        f.write(out_arc.to_file())

        for i in range(len(update_nodes)):
            in_arc = Inbound_Arc(update_nodes[i], update_transitions[i], "timed", "1")
            out_arc = Outbound_Arc(update_transitions[i], update_nodes[i])

            ## Another Inbound or Outbound arc could be generated here based on the JSON for the pathing

            f.write(in_arc.to_file())
            f.write(out_arc.to_file())
            #f.write(controller_route.to_file())
        ir = jsonParser.init_route
        for i in range(len(ir)):
            if ir[i][0] == node.id:
                init_route = Inbound_Arc(n, update_transition, "timed", "1")
                f.write(init_route.to_file())
                print("init" + init_route.to_file())

        fr = jsonParser.final_route
        for i in range(len(fr)):
            if fr[i][0] == node.id:
                final_route = Outbound_Arc(update_transition, update_nodes[0])
                f.write(final_route.to_file())
                print("final" + final_route.to_file())
            # controller_route = Inbound_Arc(n, update_transition, "timed", "1")

        f.write("  </net>\n")

def write_LoopFreedom():
    for node in nodes:
        node.notation += "_loopFreedom"
        f.write("  <net active=\"true\" id=\"{}\" type=\"P/T net\">\n"
                .format(node.notation))
        f.write(
            "    <place displayName=\"true\" id=\"{}\" initialMarking=\"0\" invariant=\"&lt; inf\" name=\"{}\" nameOffsetX=\"-5.0\" nameOffsetY=\"35.0\" positionX=\"{}\" positionY=\"{}\"/>\n"
                .format(node.notation, node.notation, 100, 100))
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
            f.write(t.to_file())
        outbound_t = []
        for t in transitions:
            if node.id == t.source:
                t.x = x
                t.y = y
                outbound_t.append(t)
                y += 100
        for t in outbound_t:
            f.write(t.to_file())
        # This for loop maps arcs from place to transitions
        inbound_arcs = []
        for t in inbound_t:
            a = Outbound_Arc(t, node)
            inbound_arcs.append(a)
        for arc in inbound_arcs:
            f.write(arc.to_file())
        # this for loop maps arcs from transition to places.
        outbound_arcs = []
        for t in outbound_t:
            a = Inbound_Arc(node, t, "tapnInhibitor", "2")
            outbound_arcs.append(a)
        for arc in outbound_arcs:
            f.write(arc.to_file())
        f.write("  </net>\n")
def parse_query():
    with open('query.json') as json_file:
        query = json.load(json_file)

    query_string = "{} (!({}.{} {} {}) {} {}.{} {} {})".format(query["query"]['query type'], query["query"]['network_1'], query["query"]['place_1'], query["query"]['predicate_1'], query["query"]['tokens_1'], query["query"]['logic'], query["query"]['network_2'], query["query"]['place_2'], query["query"]['predicate_2'], query["query"]['tokens_2'])
    return query_string

def write_query():
    #load json file
    query_input = parse_query()
    print(query_input)
    f.write("  <query active=\"true\" approximationDenominator=\"2\" capacity=\"4\" discreteInclusion=\"false\" enableOverApproximation=\"false\" enableUnderApproximation=\"false\" "
           "extrapolationOption=\"AUTOMATIC\" gcd=\"false\" hashTableSize=\"MB_16\" inclusionPlaces=\"*NONE*\" name=\"Properties\" overApproximation=\"true\" pTrie=\"true\" "
          "query=\"{}\"" "reduction=\"true\" reductionOption=\"VerifyTAPNdiscreteVerification\" searchOption=\"DFS\" symmetry=\"true\" timeDarts=\"false\" traceOption=\"NONE\" "
            "useStubbornReduction=\"true\"/>\n".format(query_input))

def write_to_file():
    # Start of File
    f.write("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n")
    f.write("<pnml xmlns=\"http://www.informatik.hu-berlin.de/top/pnml/ptNetb\">\n")

    # Initial state of the network
    write_basic_network()

    # Other components
    write_waypoints(waypoint_count)
    write_switches()
    write_LoopFreedom()
    #write_query()
    # End of File
    f.write("  <k-bound bound=\"3\"/>\n")
    f.write("</pnml>")
    f.close()
    print("Success")


initialize_network()
write_to_file()
