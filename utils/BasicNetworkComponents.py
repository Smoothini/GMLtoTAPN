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
    xml_str += make_label(0, 0, f"Extract from {network}.\nNode Count: {len(nodes) - 1}\nTransition Count: {len(transitions)}\n\nPress Shift+D followed by Enter")
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
                        n.id = f"P{t.source}_initial"
                        n.notation = f"P{t.source}_initial"
                    else:
                        n.id = f"P{t.source}_final"
                        n.notation = f"P{t.source}_final"

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
                        if n.notation == f"P{t[0]}_initial":
                            xml_str += Inbound_Arc(n, ut, "timed", "1").to_file()

            for t in jsonParser.final_route:
                if t[0] == node.id:
                    for n in u_nodes:
                        if n.notation == f"P{t[0]}_final":
                            xml_str += Outbound_Arc(ut, n).to_file()

            xml_str += "  </net>\n\n"
    return xml_str