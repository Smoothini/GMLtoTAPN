from JsonParser import JsonParser
import GMLParser as GML

import networkx as nx
import time, os

from entities.Arcs import Full_Arc, Outbound_Arc, Inbound_Arc
from entities.Node import Node
from entities.Transition import Transition

def initialize_network(g, jsonParser):
    nodes_from_routing = jsonParser.unique_ids
    
    routing = jsonParser.full_route
    nodes = GML.parse_nodes(g, nodes_from_routing, "0")
    transitions = GML.parse_transitions(routing)
    
    for node in nodes:
        for t in transitions:
            if t.source == node.id:
                node.transition_count += 1
    return nodes, transitions

def get_node(node_id, nodes):
    return next((x for x in nodes if x.id == node_id), None)

def make_label(x, y, message):
    return "<labels border=\"true\" height=\"90\" positionX=\"{}\" positionY=\"{}\" width=\"180\">{}</labels>".format(x, y, message)

# Complete network configuration component
def full_network(g, network):
    nodes_raw = list(g.nodes(data=True))
    edges_raw = list(g.edges)
    nodes = []
    transitions = []
    xml_str = ""
    for i in nodes_raw:
        n = Node(i[0], "P{}".format(i[0]))
        nodes.append(n)
    for i in edges_raw:
        t = Transition(edges_raw.index(i), i[0], i[1], "T{}_{}".format(i[0], i[1]))
        transitions.append(t)
    xml_str += ("  <net active=\"true\" id=\"{}\" type=\"P/T net\">\n".format(network))
    xml_str += make_label(0, 0, f"Network: {network}\nNode Count: {len(nodes)}\nTransition Count: {len(transitions)}\n\nPress Shift+D followed by Enter")
    for node in nodes:
        xml_str += (node.to_file())
    for transition in transitions:
        xml_str += (transition.to_file())
        
    arcs = []
    for t in transitions:
        a = Full_Arc(get_node(t.source, nodes), get_node(t.target, nodes), t)
        arcs.append(a)
    for arc in arcs:
        xml_str += arc.to_file()
    xml_str += ("  </net>\n")
    return xml_str


# Initial and final network routing
def routing_configuration(network, jsonParser, nodes: list, transitions: list):
    xml_str = ""
    controller = Node(-1, "Controller", "1")
    xml_str += controller.shared_to_file()

    for transition in transitions:
        xml_str += transition.shared_to_file()
    
    xml_str += "  <net active=\"true\" id=\"{}\" type=\"P/T net\">\n".format("Routings")
    xml_str += make_label(0, 0, f"Extract from {network}.\nNode Count: {len(nodes)}\nTransition Count: {len(transitions)}\n\nPress Shift+D followed by Enter")
    xml_str += make_label(200, 0, f"Initial routing: {str(jsonParser.init_route)}\n\nFinal routing: {str(jsonParser.final_route)}")
    for node in nodes:
        xml_str += node.to_file()
    for transition in transitions:
        xml_str += transition.to_file()

    arcs = []
    for t in transitions:
        a = Full_Arc(get_node(t.source, nodes), get_node(t.target, nodes), t)
        arcs.append(a)

    # inject packet
    inject = Transition(-2, nodes[0].id, nodes[1].id, "Inject_packet", "1")
    xml_str += inject.to_file()
    aa = Full_Arc(get_node(inject.source, nodes), get_node(inject.target, nodes), inject)
    arcs.append(aa)

    for arc in arcs:
        xml_str += arc.to_file()

    xml_str += "  </net>\n"
    return xml_str

#Switches
def switches(jsonParser, nodes: list, transitions: list):
    controller = Node(-1, "Controller", "1")
    controller.x = 100
    controller.y = 100
    xml_str = ""

    for node in nodes:
        if node.transition_count == 2:
            u_nodes = []
            u_trans = []
            ut = Transition(f"Update_{node.notation}", controller, None, f"Update_{node.notation}")
            ut.x = 300
            ut.y = 100
            y = 100
            for t in transitions:
                if t.source == node.id:
                    n = Node(f"P{t.source}_{t.target}_active", f"P{t.source}_{t.target}_active", "0")
                    n.x = ut.x + 200
                    n.y = y
                    if([t.source, t.target] in jsonParser.init_route):
                        n.marking = "1"
                    u_nodes.append(n)
                    t.x = n.x + 200
                    t.y = y
                    y += 150
                    u_trans.append(t)

            xml_str += f"  <net active=\"true\" id=\"{node.notation}_Switch\" type=\"P/T net\">\n"
            xml_str += controller.to_file()
            for n in u_nodes:
                xml_str += n.to_file()
            xml_str += ut.to_file()
            for t in u_trans:
                xml_str += t.to_file()
            xml_str += Inbound_Arc(controller, ut, "timed", "1").to_file()
            xml_str += Outbound_Arc(ut, controller).to_file()
            for i in range(len(u_nodes)):
                xml_str += Inbound_Arc(u_nodes[i], u_trans[i], "timed", "1").to_file()
                xml_str += Outbound_Arc(u_trans[i], u_nodes[i]).to_file()
            
            for t in jsonParser.init_route:
                if t[0] == node.id:
                    for n in u_nodes:
                        if n.notation == f"P{t[0]}_{t[1]}_active":
                            xml_str += Inbound_Arc(n, ut, "timed", "1").to_file()

            for t in jsonParser.final_route:
                if t[0] == node.id:
                    for n in u_nodes:
                        if n.notation == f"P{t[0]}_{t[1]}_active":
                            xml_str += Outbound_Arc(ut, n).to_file()

            xml_str += "  </net>\n"
    return xml_str

            

# Waypoint component
def waypoints(nodes, transitions: list, waypointlist: list, final_id):
    xml_str = ""
    waypoints = []
    for waypoint in waypointlist:
        if get_node(waypoint, nodes):
            waypoints.append(get_node(waypoint, nodes))

    for node in waypoints:
        net = f"{node.notation}_waypoint"
        xml_str += f"  <net active=\"true\" id=\"{net}\" type=\"P/T net\">\n"
        node.notation = f"P{node.id}_visited"
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

        for t in wp_transitions:
            xml_str += Outbound_Arc(t, node).to_file()
        xml_str += "  </net>\n"
        q = "AG ({}.{} &gt;= 1 or Routings.P{} = 0)".format(net, node.notation, final_id)

        query = "<query active=\"true\" approximationDenominator=\"2\" capacity=\"5\" discreteInclusion=\"false\" enableOverApproximation=\"false\" enableUnderApproximation=\"false\" extrapolationOption=\"null\" gcd=\"false\" hashTableSize=\"null\" inclusionPlaces=\"*NONE*\" name=\"{}\" overApproximation=\"true\" pTrie=\"true\" query=\"{}\" reduction=\"true\" reductionOption=\"VerifyTAPNdiscreteVerification\" searchOption=\"DFS\" symmetry=\"true\" timeDarts=\"false\" traceOption=\"NONE\" useStubbornReduction=\"true\"/>\n".format(node.notation, q)
    
        xml_str += query
        
        node.notation = f"P{node.id}"
    return xml_str

# Loopfreedom component
def loopfreedom(nodes: list, transitions: list):
    xml_str = ""
    for node in nodes:
        node.notation = f"P{node.id}_loopFree"
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
            xml_str += f"  <net active=\"true\" id=\"{node.notation}\" type=\"P/T net\">\n"
            xml_str += f"    <place displayName=\"true\" id=\"{node.notation}\" initialMarking=\"0\" invariant=\"&lt; " \
                       f"inf\" name=\"{node.notation}\" nameOffsetX=\"-5.0\" nameOffsetY=\"35.0\" positionX=\"{100}\" " \
                       f"positionY=\"{100}\"/>\n"
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
        node.notation = f"P{node.id}"
    return xml_str


def write_to_file(network):
    start = time.time()
    g = nx.read_gml("data/gml/" + network + '.gml', label='id')
    jsonParser = JsonParser(network)
    if type(g) == nx.classes.multigraph.MultiGraph:
        g = nx.Graph(g)
    f = open(f"data/tapn/{network}.tapn", "w")
    f.write("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n")
    f.write("<pnml xmlns=\"http://www.informatik.hu-berlin.de/top/pnml/ptNetb\">\n")

    nodes, transitions = initialize_network(g, jsonParser)

    f.write(full_network(g, network))

    # Initial state of the network
    f.write(routing_configuration(network, jsonParser, nodes, transitions))
    f.write(switches(jsonParser, nodes, transitions))

    # Other components
    if jsonParser.properties["Waypointing"]:
        f.write(waypoints(nodes, transitions, jsonParser.properties["WaypointNodeIds"], jsonParser.init_route[-1][1]))
    if jsonParser.properties["LoopFreedom"]:
        f.write(loopfreedom(nodes, transitions))

    f.write("  <k-bound bound=\"3\"/>\n")
    f.write("  <feature isGame=\"true\" isTimed=\"true\"/>\n")
    f.write("</pnml>")
    f.close()
    
    print("Success! {} converted! Execution time: {} seconds".format(network, (str(time.time()-start))[:5]))

def write_all_to_file():
    start = time.time()
    for f in os.listdir("data/gml/"):
        try:
            write_to_file(f[:-4])
        except:
            print(f"Failure! {f[:-4]} not converted..")
    print("Operation done in: {} seconds".format((str(time.time()-start))[:5]))

write_all_to_file()