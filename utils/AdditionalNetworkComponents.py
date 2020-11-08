from entities.Arcs import Full_Arc, Outbound_Arc, Inbound_Arc
from entities.Node import Node
from entities.Transition import Transition

def get_node(node_id, nodes):
    return next((x for x in nodes if x.id == node_id), None)            

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
        node.notation = f"P{node.id}"
        query = "<query active=\"true\" approximationDenominator=\"2\" capacity=\"5\" discreteInclusion=\"false\" enableOverApproximation=\"false\" enableUnderApproximation=\"false\" extrapolationOption=\"null\" gcd=\"false\" hashTableSize=\"null\" inclusionPlaces=\"*NONE*\" name=\"Waypoint_{}\" overApproximation=\"true\" pTrie=\"true\" query=\"{}\" reduction=\"true\" reductionOption=\"VerifyTAPNdiscreteVerification\" searchOption=\"DFS\" symmetry=\"true\" timeDarts=\"false\" traceOption=\"NONE\" useStubbornReduction=\"true\"/>\n".format(node.notation, q)
        xml_str += query
        
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