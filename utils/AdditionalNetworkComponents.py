from entities.Arcs import Full_Arc, Outbound_Arc, Inbound_Arc
from entities.Node import Node
from entities.Transition import Transition
import random

def get_node(node_id, nodes):
    return next((x for x in nodes if x.id == node_id), None)            

# Waypoint query
def waypoint(u, v, w):

    cap = v * 10
    xml_str = ""

    w = f"P{w}_visited"
    v = f"P{v}"
    
    wp_query = "({}.{} &gt;= 1 or Routings.{} = 0)".format(w, w, v)
    q = "AG {}".format(wp_query)
    query = "<query active=\"true\" approximationDenominator=\"2\" capacity=\"{}\" discreteInclusion=\"false\" enableOverApproximation=\"false\" enableUnderApproximation=\"false\" extrapolationOption=\"null\" gcd=\"false\" hashTableSize=\"null\" inclusionPlaces=\"*NONE*\" name=\"Waypoint_{}\" overApproximation=\"true\" pTrie=\"true\" query=\"{}\" reduction=\"true\" reductionOption=\"VerifyTAPNdiscreteVerification\" searchOption=\"DFS\" symmetry=\"true\" timeDarts=\"false\" traceOption=\"NONE\" useStubbornReduction=\"true\"/>\n".format(cap, w, q)
    xml_str += query
        
    return xml_str, wp_query

#Visited components
def visited(nodes, transitions):
    xml_str = ""
    for node in nodes:
        node.notation = f"P{node.id}_visited"
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


# Loopfreedom query
def loopfreedom(nodes):
    cap = len(nodes) * 10
    xml_str = ""
    loop_query = "("
    for node in nodes:
        loop_query += f"P{node.id}_visited.P{node.id}_visited &lt; 2 and "

    loop_query += f"P{nodes[-1].id}_visited.P{nodes[-1].id}_visited &lt; 2)"
    q = "AG{}".format(loop_query)
    query = "<query active=\"true\" approximationDenominator=\"2\" capacity=\"{}\" discreteInclusion=\"false\" enableOverApproximation=\"false\" enableUnderApproximation=\"false\" extrapolationOption=\"null\" gcd=\"false\" hashTableSize=\"null\" inclusionPlaces=\"*NONE*\" name=\"LoopFree\" overApproximation=\"true\" pTrie=\"true\" query=\"{}\" reduction=\"true\" reductionOption=\"VerifyTAPNdiscreteVerification\" searchOption=\"DFS\" symmetry=\"true\" timeDarts=\"false\" traceOption=\"NONE\" useStubbornReduction=\"true\"/>\n".format(cap, q)
    xml_str += query
        
    return xml_str, loop_query

def combinedQuery(reach_query, wp_query, loop_query = None):
    big_query = f"AG({reach_query} and {wp_query} and {loop_query})"
    return "<query active=\"true\" approximationDenominator=\"2\" capacity=\"10000\" discreteInclusion=\"false\" enableOverApproximation=\"false\" enableUnderApproximation=\"false\" extrapolationOption=\"null\" gcd=\"false\" hashTableSize=\"null\" inclusionPlaces=\"*NONE*\" name=\"All3\" overApproximation=\"true\" pTrie=\"true\" query=\"{}\" reduction=\"true\" reductionOption=\"VerifyTAPNdiscreteVerification\" searchOption=\"DFS\" symmetry=\"true\" timeDarts=\"false\" traceOption=\"NONE\" useStubbornReduction=\"true\"/>\n".format(big_query)
    


#def all_props_query()