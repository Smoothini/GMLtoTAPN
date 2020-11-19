from utils.JsonParser import JsonParser
import utils.GMLParser as GML
import utils.TestNets as TN

import networkx as nx
import time, os

from entities.Arcs import Full_Arc, Outbound_Arc, Inbound_Arc
from entities.Node import Node
from entities.Transition import Transition
import utils.BasicNetworkComponents as BNC
import utils.AdditionalNetworkComponents as ANC

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

    #f.write(BNC.full_network(g, network))

    # Initial state of the network
    xml_reach, reach_query = BNC.routing_configuration(network, jsonParser, nodes, transitions)
    f.write(xml_reach)
    f.write(BNC.switches(nodes, transitions))

    # Other components
    f.write(ANC.visited(nodes, transitions))
    if jsonParser.properties["Waypoint"]:
        xml_wp, wp_query = ANC.waypoint(jsonParser.waypoint["startNode"], jsonParser.waypoint["finalNode"], jsonParser.waypoint["waypoint"])
        f.write(xml_wp)
    if jsonParser.properties["LoopFreedom"]:
        f.write(ANC.loopfreedom(jsonParser.loopfreedom["startNode"]))

    f.write(ANC.combinedQuery(reach_query, wp_query))
    
    
    

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

#write_all_to_file()
#write_to_file("btNorthAmerica")
#write_to_file("Aconet")

TN.write_batch_to_file(1000, 5000, 1000)
#TN.make_shared(100)