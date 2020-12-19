from entities.Node import Node
from entities.Transition import Transition


def parse_nodes(nodes_raw, marking):
    nodes = []
    for i in nodes_raw:
        n = Node(i, f"P{i}", marking)
        nodes.append(n)
    return nodes


def parse_transitions(routing):
    transitions = []
    routing = removeDuplicates(routing)

    for i in routing:
        route_id = len(transitions) + 1
        source = i[0]
        target = i[1]
        label = "T{}_{}".format(source, target)

        t = Transition(route_id, source, target, label)
        transitions.append(t)
    return transitions

def removeDuplicates(lst):
    return [t for t in (set(tuple(i) for i in lst))]


def scale_json(data, scale):
    new_init_route = []
    new_final_route = []

    og_init_route = data["Initial_routing"]
    og_final_route = data["Final_routing"]
    places = {}
    pl = []
    for i in og_init_route:
        pl.append(i[0])
        pl.append(i[1])
    for i in og_final_route:
        pl.append(i[0])
        pl.append(i[1])
    pl = list(dict.fromkeys(pl))
    cnt = 0
    for i in pl:
        places[i] = cnt
        cnt+=1

    for s in range(scale):
        for i in data["Initial_routing"]:
            new_init_route.append([places[i[0]] + s * len(pl), places[i[1]] + s * len(pl)])
        for i in data["Final_routing"]:
            new_final_route.append([places[i[0]] + s * len(pl), places[i[1]] + s * len(pl)])
        
        if s < scale-1:
            first = data["Initial_routing"][-1][1]
            last = data["Initial_routing"][0][0]
            new_init_route.append([places[first] + s * len(pl), places[last] + (s+1) * len(pl)])

            first = data["Final_routing"][-1][1]
            last = data["Final_routing"][0][0]
            new_final_route.append([places[first] + s * len(pl), places[last] + (s+1) * len(pl)])

    inn = data["Properties"]["Reachability"]["startNode"]
    outt = data["Properties"]["Reachability"]["finalNode"]
    wpp = data["Properties"]["Waypoint"]["waypoint"]

    data["Properties"]["Reachability"]["startNode"] = places[inn]
    data["Properties"]["Reachability"]["finalNode"] = places[outt] + (scale-1) * len(pl)
    data["Properties"]["Waypoint"]["startNode"] = places[inn]
    data["Properties"]["Waypoint"]["finalNode"] = places[outt] + (scale-1) * len(pl)
    data["Properties"]["Waypoint"]["waypoint"] = places[wpp] + (scale-1) * len(pl)
    data["Initial_routing"] = new_init_route
    data["Final_routing"] = new_final_route
    data["Properties"]["LoopFreedom"]["startNode"] = places[inn]
    return data