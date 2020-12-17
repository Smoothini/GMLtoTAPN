from utils.JsonParser import JsonParser
import utils.GMLParser as GML

import networkx as nx
import time, os, copy

from entities.Arcs import Full_Arc, Outbound_Arc, Inbound_Arc
from entities.Node import Node
from entities.Transition import Transition
import utils.BasicNetworkComponents as BNC
import utils.AdditionalNetworkComponents as ANC
import utils.DTAPNBuilder as DB

def write_to_file(network):
    start = time.time()
    #combined queries maybe???
    g = nx.read_gml("data/gml/" + network + '.gml', label='id')
    jsonParser = JsonParser(network)
    if type(g) == nx.classes.multigraph.MultiGraph:
        g = nx.DiGraph(g)
    f = open(f"data/tapn/{network}.tapn", "w")
    f.write("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n")
    f.write("<pnml xmlns=\"http://www.informatik.hu-berlin.de/top/pnml/ptNetb\">\n")

    nodes, transitions = BNC.initialize_network(g, jsonParser)

    DB.build_composed_model_gml(network, nodes[1:], transitions, "data/dtapn_gml/")
    

    #f.write(BNC.full_network(g, network))

    # Initial state of the network
    xml_reach, reach_query = BNC.routing_configuration(network, jsonParser, nodes, transitions)
    f.write(xml_reach)
    xml_switch, switch_count = BNC.switches(nodes[1:], transitions)
    f.write(xml_switch)

    # Other components
    f.write(ANC.visited(nodes[1:], transitions))
    if jsonParser.properties["Waypoint"]:
        xml_wp, wp_query = ANC.waypoint(jsonParser.waypoint["startNode"], jsonParser.waypoint["finalNode"], jsonParser.waypoint["waypoint"])
        f.write(xml_wp)
    if jsonParser.properties["LoopFreedom"]:
        xml_loop, loop_query = ANC.loopfreedom(nodes[1:])
        f.write(xml_loop)

    f.write(ANC.combinedQuery(reach_query, wp_query, loop_query))
    
    
    

    f.write("  <k-bound bound=\"3\"/>\n")
    f.write("  <feature isGame=\"true\" isTimed=\"true\"/>\n")
    f.write("</pnml>")
    f.close()
    print("Success! {} converted! Execution time: {} seconds".format(network, (str(time.time()-start))[:5]))
    return switch_count

def find_node(nodes, nid):
    return next((x for x in nodes if x.id == nid), None)


def write_zoo_to_file(network, magni):
    g = nx.read_gml("data/gml/" + network + '.gml', label='id')
    jsonParser = JsonParser(network)
    if type(g) == nx.classes.multigraph.MultiGraph:
        g = nx.DiGraph(g)

    nodes, transitions = BNC.initialize_network(g, jsonParser)

    ubernodes = []
    ubertransitions = []

    start = jsonParser.waypoint["startNode"]
    end = jsonParser.waypoint["finalNode"]
    wp = jsonParser.waypoint["waypoint"]

    for i in range(magni):
        for node in nodes[1:]:
            n = copy.deepcopy(node)
            n.id = f"{n.id}xxx{i}"
            n.notation = f"{n.notation}xxx{i}"
            if n.init_route != None:
                n.init_route = f"{n.init_route}xxx{i}"
            if n.final_route != None:
                n.final_route = f"{n.final_route}xxx{i}"
            ubernodes.append(n)
        
        for t in transitions:
            tt = copy.deepcopy(t)
            tt.id = f"{tt.id}xxx{i}"
            tt.notation = f"{tt.notation}xxx{i}"
            if tt.source != None:
                tt.source = f"{tt.source}xxx{i}"
            if tt.target != None:
                tt.target = f"{tt.target}xxx{i}"
            ubertransitions.append(tt)

    
    
    for i in range(magni-1):
        tt = Transition(f"Linkerxxx{i}", f"{end}xxx{i}", f"{start}xxx{i+1}", f"Linkerxxx{i}")
        m0 = find_node(ubernodes, f"{end}xxx{i}")
        m0.init_route = f"{start}xxx{i+1}"
        m0.final_route = f"{start}xxx{i+1}"
        ubertransitions.append(tt)
        

    #for node in ubernodes:
        #print(f"{node.id} {node.notation} {node.init_route} {node.final_route}")

    #print(len(ubernodes), len(ubertransitions))
    DB.build_composed_model_gml(network, ubernodes, ubertransitions, "data/uberdtapn/", uber=True, wp=f"{wp}xxx{magni-1}", pn=f"{end}xxx{magni-1}")


def write_all_to_file(magni):
    start = time.time()
    for f in os.listdir("data/gml/"):
        try:
            write_zoo_to_file(f[:-4], magni)
        except:
            print(f"Failure! {f[:-4]} not converted..")
    print("Operation done in: {} seconds".format((str(time.time()-start))[:5]))
