from utils.JsonParser import JsonParser
import utils.GMLParser as GML

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
                if [t.source, t.target] in jsonParser.init_route and [t.source, t.target] in jsonParser.final_route:
                    #print(f"In both {t.source} {t.target}")
                    node.init_route = t.target
                    node.final_route = t.target
                elif [t.source, t.target] in jsonParser.init_route:
                    node.init_route = t.target
                    #print(f"In init {t.source} {t.target}")
                elif [t.source, t.target] in jsonParser.final_route:
                    node.final_route = t.target
                    #print(f"In final {t.source} {t.target}")

    #for node in nodes:
        #print(f"Node {node.id}      initial: {node.init_route}     final: {node.final_route}")

    return nodes, transitions

def get_node(node_id, nodes):
    return next((x for x in nodes if x.id == node_id), None)

def make_label(x, y, message):
    return "    <labels border=\"true\" height=\"90\" positionX=\"{}\" positionY=\"{}\" width=\"180\">{}</labels>\n\n".format(x, y, message)


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
    xml_str += ("  <net active=\"false\" id=\"{}\" type=\"P/T net\">\n".format(network))
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
    xml_str += ("  </net>\n\n")
    return xml_str


# Initial and final network routing
def routing_configuration(network, jsonParser, nodes: list, transitions: list):
    xml_str = ""
    controller = Node(-1, "Controller", "1")
    xml_str += controller.shared_to_file()

    for transition in transitions:
        xml_str += transition.shared_to_file()
    
    xml_str += "  <net active=\"true\" id=\"{}\" type=\"P/T net\">\n".format("Routings")
    xml_str += make_label(0, 0, f"Extract from {network}.\n-Node Count: {len(nodes) - 1}\n-Transition Count: {len(transitions)}\n\n-Initial routing length: {len(jsonParser.init_route)}\n-Final routing length: {len(jsonParser.final_route)}\n\n\nPress Shift+D followed by Enter")
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
    inject = Transition(-2, nodes[0].id, jsonParser.init_route[0][0], "Inject_packet", "1")
    xml_str += inject.to_file()
    aa = Full_Arc(get_node(inject.source, nodes), get_node(inject.target, nodes), inject)
    arcs.append(aa)

    for arc in arcs:
        xml_str += arc.to_file()

    xml_str += "  </net>\n\n"

    #AG(!(deadlock)∨Pv′≥1)
    
    #q = "AG ({}.{} &gt;= 1 or Routings.P{} = 0)".format(net, node.notation, final_id)
    q = "AG (!(deadlock) or Routings.P{}>=1)".format(jsonParser.properties["Reachability"])
    query = "<query active=\"true\" approximationDenominator=\"2\" capacity=\"5\" discreteInclusion=\"false\" enableOverApproximation=\"false\" enableUnderApproximation=\"false\" extrapolationOption=\"null\" gcd=\"false\" hashTableSize=\"null\" inclusionPlaces=\"*NONE*\" name=\"{}\" overApproximation=\"true\" pTrie=\"true\" query=\"{}\" reduction=\"true\" reductionOption=\"VerifyTAPNdiscreteVerification\" searchOption=\"DFS\" symmetry=\"true\" timeDarts=\"false\" traceOption=\"NONE\" useStubbornReduction=\"true\"/>\n\n".format("Reach_P{}".format(jsonParser.properties["Reachability"]), q)
    xml_str += query
    return xml_str

# Switches
def switches(nodes, transitions):
    controller = Node(-1, "Controller", "1")
    controller.x = 100
    controller.y = 100
    xml_str = ""
    switch_nodes = []
    for node in nodes:
        if node.init_route != node.final_route:
            switch_nodes.append(node)
            #if node.init_route and node.final_route:
             #   print(f"Node {node.id}: Full switch")
            #elif node.init_route and not node.final_route:
             #   print(f"Node {node.id}: Half initial switch")
            #elif not node.init_route and node.final_route:
             #   print(f"Node {node.id}: Half final switch")

    for node in switch_nodes:
        #print(node.notation)
        update_transition = Transition(f"Update_{node.notation}", controller, None, f"Update_{node.notation}")
        update_transition.x , update_transition.y = 300, 100

        initial_place = Node(f"P{node.id}_initial", f"P{node.id}_initial", "1")
        initial_place.x, initial_place.y = 500, 100

        final_place = Node(f"P{node.id}_final", f"P{node.id}_final")
        final_place.x, final_place.y = 500, 300

        initial_transition, final_transition = None, None
        if node.init_route != None:
            initial_transition = next((x for x in transitions if x.source == node.id and x.target == node.init_route), None)
            initial_transition.x, initial_transition.y = 700, 100
        if node.final_route != None:
            final_transition = next((x for x in transitions if x.source == node.id and x.target == node.final_route), None)
            final_transition.x, final_transition.y = 700, 300
        
        xml_str += f"  <net active=\"true\" id=\"{node.notation}_Switch\" type=\"P/T net\">\n"
        xml_str += controller.to_file()
        xml_str += update_transition.to_file()

        xml_str += Inbound_Arc(controller, update_transition, "timed", "1").to_file()
        xml_str += Outbound_Arc(update_transition, controller).to_file()

        xml_str += initial_place.to_file()
        xml_str += final_place.to_file()
        xml_str += Inbound_Arc(initial_place, update_transition, "timed", "1").to_file()
        xml_str += Outbound_Arc(update_transition, final_place).to_file()

        if initial_transition:
            xml_str += initial_transition.to_file()
            xml_str += Inbound_Arc(initial_place, initial_transition, "timed", "1").to_file()
            xml_str += Outbound_Arc(initial_transition, initial_place).to_file()

        if final_transition:
            xml_str += final_transition.to_file()
            xml_str += Inbound_Arc(final_place, final_transition, "timed", "1").to_file()
            xml_str += Outbound_Arc(final_transition, final_place).to_file()


        xml_str += "  </net>\n\n"

    return xml_str 