import time, os
import json
from entities.Arcs import Full_Arc, Outbound_Arc, Inbound_Arc
from entities.Node import Node
from entities.Transition import Transition
import utils.BasicNetworkComponents as BNC
import utils.AdditionalNetworkComponents as ANC
import utils.LtLBuilder as Ltl
import utils.DTAPNBuilder as DB

def make_label(x, y, message):
    return "    <labels border=\"true\" height=\"90\" positionX=\"{}\" positionY=\"{}\" width=\"180\">{}</labels>\n\n".format(x, y, message)


def json_maker(ntype, count, init_route, final_route, n0, nn, wp):
    start = time.time()
    mydic = {} # ;^)
    mydic["Initial_routing"] = init_route
    mydic["Final_routing"] = final_route
    mydic["Properties"] = {}
    mydic["Properties"]["Waypoint"] = {}
    mydic["Properties"]["Waypoint"]["startNode"] = n0
    mydic["Properties"]["Waypoint"]["finalNode"] = nn
    mydic["Properties"]["Waypoint"]["waypoint"] = wp
    mydic["Properties"]["LoopFreedom"] = {}
    mydic["Properties"]["LoopFreedom"]["startNode"] = n0
    mydic["Properties"]["Reachability"] = {}
    mydic["Properties"]["Reachability"]["startNode"] = n0
    mydic["Properties"]["Reachability"]["finalNode"] = nn

    
    myjsondic = json.dumps(mydic, indent=4) # ;;^)
    f = open(f"data/json_custom_testcases/{ntype}_{count}.json", "w")
    f.write(myjsondic)
    f.close()

    f = open(f"data/time/{ntype}/{ntype}_{count}_JSON.txt", "w")
    f.write(str(time.time() - start))
    f.close()

    print(f"JSON for {ntype} network of size {count} generated in {time.time()-start} seconds")


def generate_disjoint (count):
    start = time.time()
    #Generating initial and final nodes
    #also path configurations based on size
    acc = count
    count = (int((count - 3) / 4) + 1) * 4 + 3
    init_node = Node(0, "P0")
    final_node = Node(count-1, f"P{count-1}")
    mid_node = Node(count-2, f"P{count-2}")
    path_count = (int((count-3)/4) + 1) * 2 + 1
    node_path_count = (int((count-3)/4)) * 2 
    path1 = []
    path2 = []
    #Creating nodes for the 2 paths 

    for i in range(node_path_count):
        path1.append(Node(i+1, f"P{i+1}"))
        path2.append(Node(i+1+node_path_count, f"P{i+1+node_path_count}"))
    
    init_route = []
    final_route = []

    init_node.init_route = path1[0].id
    init_node.final_route = path2[0].id

    init_route.append([init_node.id,init_node.init_route])
    final_route.append([init_node.id,init_node.final_route])

    for i in range(int(node_path_count/2) -1):
        path1[i].init_route = path1[i+1].id
        init_route.append([path1[i].id, path1[i+1].id])
        path2[i].final_route = path2[i+1].id
        final_route.append([path2[i].id, path2[i+1].id])

    path1[int(node_path_count/2) -1].init_route = mid_node.id
    path2[int(node_path_count/2) -1].final_route = mid_node.id
    init_route.append([path1[int(node_path_count/2) -1].id,mid_node.id])
    final_route.append([path2[int(node_path_count/2) -1].id,mid_node.id])

    mid_node.init_route = path1[int(node_path_count/2)].id
    mid_node.final_route = path2[int(node_path_count/2)].id
    init_route.append([mid_node.id, path1[int(node_path_count/2)].id])
    final_route.append([mid_node.id, path2[int(node_path_count/2)].id])

    for i in range(int(node_path_count/2), node_path_count - 1):
        path1[i].init_route = path1[i+1].id
        path2[i].final_route = path2[i+1].id
        init_route.append([path1[i].id, path1[i+1].id])
        final_route.append([path2[i].id, path2[i+1].id])

    path1[-1].init_route = final_node.id
    path2[-1].final_route = final_node.id
    init_route.append([path1[-1].id, final_node.id])
    final_route.append([path2[-1].id, final_node.id])


    #Making a json file out of the routings
    


    #print(f"Init path: {init_route}")
    #print(f"Final path: {final_route}")
    # verified: waypoint = mid_node.id
    # non verified: waypoint = literally anything else
    wp = 1

    f = open(f"data/time/Disjoint/Disjoint_{acc}_PREP.txt", "w")
    f.write(str(time.time() - start))
    f.close()

    print(f"Prep time Disjoint size {acc}: {time.time()-start} seconds")
    #making the json file
    json_maker("Disjoint", acc, init_route, final_route, init_node.id, final_node.id, wp)
    #making the ltl file
    Ltl.make_ltl("Disjoint", acc)


    #Generating arcs and transitions based on nodes
    nodes = []
    nodes.append(init_node)
    nodes.extend(path1+path2)
    nodes.append(mid_node)
    nodes.append(final_node)
    #for node in nodes:
     #   print(f"P{node.id}  init: {node.init_route}  final: {node.final_route}")
    

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

    
    return count,"Disjoint",nodes,transitions,arcs,wp,acc

def pospath(x):
    return [[x, x+2],[x+2, x+1],[x+1, x+3]]

def generate_worst (count):
    start = time.time()
    #Generating initial and final nodes
    #also path configurations based on size
    acc = count
    count = (int((count-1)/3)) * 3 + 1
    print(count)
    series = int((count-1)/3)
    nodes = []
    init_node = Node(0, "P0")
    init_node.init_route = 1
    final_node = Node(count-1, f"P{count-1}")
    nodes.append(init_node)
    for i in range(count-2):
        nodes.append(Node(i+1,f"P{i+1}"))
        nodes[-1].init_route = i+2
    nodes.append(final_node)
    
    init_route = []
    final_route = []

    for node in nodes[:-1]:
        init_route.append([node.id, node.init_route])

    for i in range(series):
        for t in pospath(i*3):
            node = next((x for x in nodes if x.id == t[0]), None)
            node.final_route = t[1]
        final_route.extend(pospath(i*3))
    
    #first common node
    wp = 1
    print(f"Prep time Worst size {acc}: {time.time()-start} seconds")
    #making the json file
    json_maker("Worst", acc, init_route, final_route, init_node.id, final_node.id, wp)
    #making the ltl file
    Ltl.make_ltl("Worst", acc)


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

    return count,"Worst",nodes,transitions,arcs,wp,acc

def generate_shared(count):
    start = time.time()
    #Generating initial and final nodes
    #also path configurations based on size
    acc = count
    count = (int((count-1)/3)) * 3 + 1
    common_count = int ((count - 4) / 3)
    common = []
    path_count = int ((count - 2 - common_count)/2)
    path1 = []
    path2 = []
    init_node = Node(0, "P0")
    final_node = Node(count-1, f"P{count-1}")
    #Making the common nodes
    for i in range(common_count):
        common.append(Node(i+1,f"P{i+1}"))
    
    
    common.append(final_node)
    #Making the routings
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

    #Making a json file out of the routings
    init_route = []
    final_route = []

    init_route.append([init_node.id, path1[0].id])
    final_route.append([init_node.id, path2[0].id])

    for i in range (path_count -1):
        init_route.append([path1[i].id, path1[i].init_route])
        init_route.append([path1[i].init_route, path1[i+1].id])
        final_route.append([path2[i].id, path2[i].final_route])
        final_route.append([path2[i].final_route, path2[i+1].id])

    init_route.append([path1[-1].id, final_node.id])
    final_route.append([path2[-1].id, final_node.id])

    #first common node
    wp = path_count
    print(f"Prep time Shared size {acc}: {time.time()-start} seconds")
    #making the json file
    json_maker("Shared", acc, init_route, final_route, init_node.id, final_node.id, wp)
    #making the ltl file
    Ltl.make_ltl("Shared", acc)



    #Generating arcs and transitions
    nodes = []
    nodes.append(init_node)
    nodes.extend(common[:-1] + path1 + path2)
    nodes.append(final_node)

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


    return count,"Shared",nodes,transitions,arcs,wp,acc




def net(params):
    count,ntype,nodes,transitions,arcs,wp,_ = params
    xml_str = ""
    xml_str += "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n"
    xml_str += "<pnml xmlns=\"http://www.informatik.hu-berlin.de/top/pnml/ptNetb\">\n"
    
    controller = Node(-1, "Controller", "1")
    xml_str += controller.shared_to_file()

    for transition in transitions:
        xml_str += transition.shared_to_file()

    xml, reach_query = routing(count, ntype, nodes, transitions, arcs)
    xml_str += xml
    xml, switch_count = BNC.switches_v2(nodes, transitions)
    xml_str += xml
    xml_str += ANC.visited(nodes, transitions)

    xml, wp_query = ANC.waypoint(nodes[0].id, nodes[-1].id, wp)
    xml_str += xml

    xml, loop_query = ANC.loopfreedom(nodes)
    xml_str+= xml
    xml_str += ANC.combinedQuery(reach_query, wp_query, loop_query)

    xml_str += "  <k-bound bound=\"3\"/>\n"
    xml_str += "  <feature isGame=\"true\" isTimed=\"true\"/>\n"
    xml_str += "</pnml>"

    return xml_str




def routing(count, ntype, nodes, transitions, arcs):
    cap = len(nodes) * 10
    controller = Node(-1, "Controller", "1")
    xml_str = ""
    xml_str += "  <net active=\"true\" id=\"{}\" type=\"P/T net\">\n".format("Routings")
    if ntype == "Shared":
        path_len = int ((count-1)/3*2+1)
    elif ntype == "Disjoint":
        path_len = (int((count-3)/4) + 1) * 2 + 1
    else:
        path_len = count
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

    xml_str += "<place displayName=\"true\" id=\"Clock\" initialMarking=\"1\" invariant=\"&lt;= 0\" name=\"Clock\" nameOffsetX=\"0\" nameOffsetY=\"0\" positionX=\"285\" positionY=\"45\"/>"
    injectpv = Node("P_u_visited", "P_u_visited", "1")
    xml_str += "<place displayName=\"true\" id=\"P_u_visited\" initialMarking=\"0\" invariant=\"&lt; inf\" name=\"P_u_visited\" nameOffsetX=\"0\" nameOffsetY=\"0\" positionX=\"285\" positionY=\"180\"/>"
    xml_str += Outbound_Arc(inject, injectpv).to_file() 
    for t in transitions:
        if t.source == nodes[0].id:
            xml_str += Inbound_Arc(injectpv, t, "tapnInhibitor", 2).to_file()
    xml_str += "  </net>\n\n"

    reach_query = "(!(deadlock) or P{}_visited.P{}_visited>=1)".format(nodes[-1].id, nodes[-1].id)
    q = "AG{}".format(reach_query)
    query = "<query active=\"true\" approximationDenominator=\"2\" capacity=\"{}\" discreteInclusion=\"false\" enableOverApproximation=\"false\" enableUnderApproximation=\"false\" extrapolationOption=\"null\" gcd=\"false\" hashTableSize=\"null\" inclusionPlaces=\"*NONE*\" name=\"{}\" overApproximation=\"true\" pTrie=\"true\" query=\"{}\" reduction=\"true\" reductionOption=\"VerifyTAPNdiscreteVerification\" searchOption=\"DFS\" symmetry=\"true\" timeDarts=\"false\" traceOption=\"NONE\" useStubbornReduction=\"true\"/>\n\n".format(cap,"Reach_P{}".format(nodes[-1].id), q)
    xml_str += query

    return xml_str, reach_query


def make_disjoint(count):
    f = open(f"data/tapn_custom_testcases/Disjoint_{count}.tapn", "w")
    f.write(net(generate_disjoint(count)))
    f.close()
    print(f"TAPN for Disjoint network of size {count} generated")

def make_shared(count):
    f = open(f"data/tapn_custom_testcases/Shared_{count}.tapn", "w")
    f.write(net(generate_shared(count)))
    f.close()
    print(f"TAPN for Shared network of size {count} generated")

def make_worst(count):
    f = open(f"data/tapn_custom_testcases/Worst_{count}.tapn", "w")
    f.write(net(generate_worst(count)))
    f.close()
    print(f"TAPN for Worst network of size {count} generated")

def write_batch_to_file(small,big,step):
    for t in range(small, big+step, step):
        make_disjoint(t)
        make_shared(t)
        make_worst(t)