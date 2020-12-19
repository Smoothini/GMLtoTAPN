from utils.JsonParser import JsonParser
import utils.VarOps as varOps

import networkx as nx
import time, os, copy

from entities.Arcs import Full_Arc, Outbound_Arc, Inbound_Arc
from entities.Node import Node
from entities.Transition import Transition
import utils.BasicNetworkComponents as BNC
import utils.AdditionalNetworkComponents as ANC
import utils.DTAPNBuilder as DB

## Used by Zoo Topology
def write_to_file(network, scale=1):
    start = time.time()
    jsonParser = JsonParser(network)
    f = open(f"data/tapn/{network}.tapn", "w")
    f.write("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n")
    f.write("<pnml xmlns=\"http://www.informatik.hu-berlin.de/top/pnml/ptNetb\">\n")

    jsonParser.scale_data(scale)
    nodes, transitions = BNC.initialize_network(jsonParser)
    DB.build_composed_model_zoo(network, nodes, transitions, jsonParser.data, "data/dtapn_gml/")    

    #f.write(BNC.full_network(g, network))

    ### Routings and switches
    ## Switches have a trivial attribute set to False by default which prevents building trivial switches.
    ## Can be disabled by adding trivial=True when calling the method.
    xml_reach, reach_query = BNC.routing_configuration(network, jsonParser, nodes, transitions)
    f.write(xml_reach)
    f.write(BNC.switches(nodes, transitions))
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
    print("Tapaal File for {} generated in {} seconds".format(network, (str(time.time()-start))[:5]))

def find_node(nodes, nid):
    return next((x for x in nodes if x.id == nid), None)

def write_all_to_file():
    start = time.time()
    for f in os.listdir("data/gml/"):
        try:
            write_to_file(f[:-4])
        except:
            print(f"Failure! {f[:-4]} not converted..")
    print("Operation done in: {} seconds".format((str(time.time()-start))[:5]))
