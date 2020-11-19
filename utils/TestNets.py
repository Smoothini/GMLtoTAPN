import time, os

from entities.Arcs import Full_Arc, Outbound_Arc, Inbound_Arc
from entities.Node import Node
from entities.Transition import Transition
import utils.BasicNetworkComponents as BNC
import utils.AdditionalNetworkComponents as ANC

def make_label(x, y, message):
    return "    <labels border=\"true\" height=\"90\" positionX=\"{}\" positionY=\"{}\" width=\"180\">{}</labels>\n\n".format(x, y, message)


def generate_disjoint (count):
    chain_length = int(count/2)
    cup = []
    cdown = []
    for i in range (chain_length):
        cup.append(Node(i, f"P{i}", "0"))
        cdown.append(Node(i+chain_length, f"P{i+chain_length}", "0"))
    
    for i in range (chain_length - 1):
        cup[i].init_route = cup[i+1].id

    cup[0].final_route = cdown[0].id
    cup[chain_length-1].init_route = cdown[-1].id

    for i in range (chain_length - 1):
        cdown[i].final_route = cdown[i+1].id

    tup = []
    tdown = []

    for i in range (chain_length - 1):
        t1 = f"{i}_{i+1}"
        tup.append(Transition(t1, i, i+1, f"T{t1}"))
        t2 = f"{i+chain_length}_{i+1 + chain_length}"
        tdown.append(Transition(t2, i+chain_length, i+1+chain_length, f"T{t2}"))
    
    ut = Transition(f"{0}_{chain_length}", 0, chain_length, f"T{0}_{chain_length}")
    dt = Transition(f"{chain_length-1}_{count-1}", chain_length-1, count-1, f"T{chain_length-1}_{count-1}")
    tup.append(ut)
    tdown.append(dt)

    aup = []
    adown = []

    for i in range (chain_length - 1):
        aup.append(Full_Arc(cup[i], cup[i+1], tup[i]))
        adown.append(Full_Arc(cdown[i], cdown[i+1], tdown[i]))

    ua = Full_Arc(cup[0], cdown[0], ut)
    da = Full_Arc(cup[-1], cdown[-1], dt)
    aup.append(ua)
    adown.append(da)

    nodes = cup + cdown
    transitions = tup + tdown
    arcs = aup + adown
    
    return count,"Disjoint",nodes,transitions,arcs

def generate_shared(count):
    count = (int((count-1)/3)) * 3 + 1

    common_count = int ((count - 4) / 3)
    common = []
    path_count = int ((count - 2 - common_count)/2)
    path1 = []
    path2 = []

    init_node = Node(0, "P0")
    final_node = Node(count-1, f"P{count-1}")

    for i in range(common_count):
        common.append(Node(i+1,f"P{i+1}"))
    
    common.append(final_node)
    
    for i in range(path_count):
        path1.append(Node(i+path_count, f"P{i+path_count}"))
        path1[-1].init_route = common[i].id
        path2.append(Node(i+2*path_count, f"P{i+2*path_count}"))
        path2[-1].final_route = common[i].id

    for i in range(common_count):
        common[i].init_route = path1[i+1].id
        common[i].final_route = path2[i+1].id

    init_node.init_route = path1[0].id
    init_node.final_route = path2[0].id

    nodes = []
    nodes.append(init_node)
    nodes.extend(common[:-1] + path1 + path2)
    nodes.append(final_node)

    #for node in nodes:
     #   print(f"P{node.id}   init {node.init_route}   final {node.final_route}")

    transitions = []
    arcs = []

    for node in nodes:
        if node.init_route:
            t = Transition(f"T{node.id}_{node.init_route}", node.id, node.init_route,f"T{node.id}_{node.init_route}")
            transitions.append(t)
            a = Full_Arc(node, next((x for x in nodes if x.id == node.init_route), None), t)
            arcs.append(a)
        if node.final_route:
            t = Transition(f"T{node.id}_{node.final_route}", node.id, node.final_route,f"T{node.id}_{node.final_route}")
            transitions.append(t)
            a = Full_Arc(node, next((x for x in nodes if x.id == node.final_route), None), t)
            arcs.append(a)

    return count,"Shared",nodes,transitions,arcs




def net(params):
    count,ntype,nodes,transitions,arcs = params
    xml_str = ""
    xml_str += "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n"
    xml_str += "<pnml xmlns=\"http://www.informatik.hu-berlin.de/top/pnml/ptNetb\">\n"
    
    controller = Node(-1, "Controller", "1")
    xml_str += controller.shared_to_file()

    for transition in transitions:
        xml_str += transition.shared_to_file()

    xml, reach_query = routing(count, ntype, nodes, transitions, arcs)
    xml_str += xml
    xml_str += BNC.switches(nodes, transitions)
    xml_str += ANC.visited(nodes, transitions)
    xml, wp_query = ANC.waypoint(nodes[0].id, nodes[-1].id, nodes[-1].id)
    xml_str += xml
    xml_str += ANC.loopfreedom(nodes)
    xml_str += ANC.combinedQuery(reach_query, wp_query)

    xml_str += "  <k-bound bound=\"3\"/>\n"
    xml_str += "  <feature isGame=\"true\" isTimed=\"true\"/>\n"
    xml_str += "</pnml>"

    return xml_str




def routing(count, ntype, nodes, transitions, arcs):
    controller = Node(-1, "Controller", "1")
    xml_str = ""
    xml_str += "  <net active=\"true\" id=\"{}\" type=\"P/T net\">\n".format("Routings")
    if ntype == "Shared":
        path_len = int ((count-1)/3*2+1)
    else:
        path_len = int(count/2)
    xml_str += make_label(0, 0, f"{ntype} network with {count} total nodes.\n\n-Initial routing length: {path_len}\n-Final routing length: {path_len}\n\n\nPress Shift+D followed by Enter")
    #xml_str += make_label(200, 0, f"Initial routing: {str(jsonParser.init_route)}\n\nFinal routing: {str(jsonParser.final_route)}")
    for node in nodes:
        xml_str += node.to_file()
    xml_str += controller.to_file()
    for transition in transitions:
        xml_str += transition.to_file()

    # inject packet
    inject = Transition(-2, controller.id, nodes[0].id, "Inject_packet", "1")
    xml_str += inject.to_file()
    aa = Full_Arc(controller, nodes[0], inject)
    arcs.append(aa)

    for arc in arcs:
        xml_str += arc.to_file()
    xml_str += "  </net>\n\n"

    reach_query = "(!(deadlock) or P{}_visited.P{}_visited>=1)".format(nodes[-1].id, nodes[-1].id)
    q = "AG{}".format(reach_query)
    query = "<query active=\"true\" approximationDenominator=\"2\" capacity=\"5\" discreteInclusion=\"false\" enableOverApproximation=\"false\" enableUnderApproximation=\"false\" extrapolationOption=\"null\" gcd=\"false\" hashTableSize=\"null\" inclusionPlaces=\"*NONE*\" name=\"{}\" overApproximation=\"true\" pTrie=\"true\" query=\"{}\" reduction=\"true\" reductionOption=\"VerifyTAPNdiscreteVerification\" searchOption=\"DFS\" symmetry=\"true\" timeDarts=\"false\" traceOption=\"NONE\" useStubbornReduction=\"true\"/>\n\n".format("Reach_P{}".format(nodes[-1].id), q)
    xml_str += query

    return xml_str, reach_query


def make_disjoint(count):
    f = open(f"data/tapn_custom_testcases/Disjoint_{count}.tapn", "w")
    f.write(net(generate_disjoint(count)))
    f.close()
    print(f"Success! Disjoint network of size {count} generated!")

def make_shared(count):
    f = open(f"data/tapn_custom_testcases/Shared_{count}.tapn", "w")
    f.write(net(generate_shared(count)))
    f.close()
    print(f"Success! Shared network of size {count} generated!")

def write_batch_to_file(small,big,step):
    for t in range(small, big+step, step):
        make_disjoint(t)
        make_shared(t)

    
