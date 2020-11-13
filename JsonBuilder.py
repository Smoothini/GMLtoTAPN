import networkx as nx
import json, time
import random
import os


class Waypoint:

    def __init__(self, u, v, wp):
        self.startNode = u
        self.finalNode = v
        self.waypoint = wp


class LoopFreedom:

    def __init__(self, u):
        self.startNode = u


class Reachability:

    def __init__(self, u, v):
        self.startNode = u
        self.finalNode = v


def isDirected(filepath):
    with open(filepath, 'r') as info:
        for line in info:
            if line.strip() == "directed 1":
                return True
    return False


def makeDirected(filepath):
    with open(filepath, 'r+') as info:
        contents = info.readlines()
        contents.insert(3, "  directed 1\n")
        info.seek(0)
        info.writelines(contents)


# import graph_tool.all as gt
def jsonbuilder(network):
    filepath = "data/gml/" + network + ".gml"

    if not isDirected(filepath):
        makeDirected(filepath)

    start = time.time()
    g = nx.read_gml(filepath, label='id')
    g = nx.DiGraph(g)

    routings = findRoutings(g)

    if routings:
        info = generateJSONInfo(g, routings)
        generateJSONFile(info, network)
        print("Success! Json settings for {} generated! Execution time: {} seconds".format(network,
                                                                                           (str(time.time() - start))[
                                                                                           :5]))
    else:
        print("Failure! No final routing available for {}... Execution time: {} seconds.".format(network,
                                                                                          (str(time.time() - start))[
                                                                                          :5]))


def findRoutings(g):
    nodes_raw = list(g.nodes(data=True))
    length = 0

    for source in range(len(nodes_raw)):
        i = 1
        paths = list(nx.single_source_shortest_path_length(g, source))
        for target in reversed(paths):
            all_paths = list(nx.all_simple_paths(g, source=source, target=target))
            all_paths = sorted(all_paths, key=len, reverse=True)
            if len(all_paths) >= 2:
                if len(all_paths[0]) + len(all_paths[1]) > length:
                    routings = all_paths[:2]
                    length = len(all_paths[0]) + len(all_paths[1])
        i += 1

    if length:
        return routings[:2]
    else:
        return False


def generateJSONFile(info, name):
    myjsondic = json.dumps(info, indent=4)
    f = open(f"data/json/{name}.json", "w")
    f.write(myjsondic)
    f.close()


def generateJSONInfo(g, routings: list):
    mydic = {}
    init_path = routings[0]
    final_path = routings[-1]
    source = init_path[0]
    target = init_path[-1]

    print(f"Nodes in graph: {g.nodes}")
    print(f"Edges in graph: {g.edges}")
    # print(f"Max shortest path: {lmax}, between {s} and {t}")
    print(f"Initial Path: {str(init_path)}")
    # all_paths = list(nx.all_simple_paths(g, source=source, target=target))
    # print(f"Amount of paths: {len(all_paths)}")
    # print(f"Biggest path size: {lmax_path}")
    print(f"Final Path: {str(final_path)}")
    s1 = set(init_path[1:-1])
    s2 = set(final_path[1:-1])
    wps = list(s1.intersection(s2))
    print(f"Common waypoints: {wps}")
    init_route = []
    final_route = []
    for node in range(len(init_path) - 1):
        init_route.append([init_path[node], init_path[node + 1]])
    for node in range(len(final_path) - 1):
        final_route.append([final_path[node], final_path[node + 1]])
    print(f"Init routing: {init_route}")
    print(f"Final routing: {final_route}")

    mydic["Initial_routing"] = init_route
    mydic["Final_routing"] = final_route
    mydic["Properties"] = {}
    if wps:
        mydic["Properties"]["Waypoint"] = Waypoint(source, target, wps[0]).__dict__
    mydic["Properties"]["LoopFreedom"] = LoopFreedom(source).__dict__
    mydic["Properties"]["Reachability"] = Reachability(source, target).__dict__

    return mydic


##in progress, doesn't look very gang gang so far..
def jsonGtBuilder(network):
    start = time.time()
    # g = gt.load_graph(f"data/gml/{network}.gml")
    n = g.num_vertices()

    lmax = 0
    s = -1
    t = -1
    init_path = []

    for source in range(n):
        for target in range(n - 1):
            v, e = gt.shortest_path(g, source, target)
            if len(v) > lmax:
                lmax = len(v)
                s = source
                t = target
                init_path = e

    print(f" source: {s}\n target: {t}\n path: {lmax}")

    print(f"grph_tool time: {str(time.time() - start)[:-4]} seconds")


def build_all():
    not_converted = []
    start = time.time()
    for f in os.listdir("data/gml/"):
        try:
            jsonbuilder(f[:-4])
        except:
            not_converted += f"{f}\n"
            print(f"Failure! {f} not converted..")
            continue
    f = open("not yet supported.txt", "w")
    f.writelines(not_converted)
    f.close()
    print("Operation done in: {} seconds".format((str(time.time() - start))[:5]))


t = 0


def build_not_supported():
    start = time.time()
    f = open("not yet supported.txt", "r")
    not_converted = []
    unsupported = f.readlines()
    cnt = 0
    for net in unsupported:
        try:
            jsonbuilder(net.strip()[:-4])
        except:
            not_converted += f"{net.strip()}\n"
            cnt += 1
            print(f"Failure! {net.strip()} not converted..")
            continue
    f = open("not yet supported.txt", "w")
    f.writelines(not_converted)
    f.close()
    print("Operation done in: {} seconds".format((str(time.time() - start))[:5]))
    print(f"{not_converted}")
    print(f"Not build: {cnt}")


def cleanup():
    ns = open("not yet supported.txt", "w")
    cnt = 0
    for f in os.listdir("data/gml/"):
        found = False
        for g in os.listdir("data/json/"):
            if (f[:-4] == g[:-5]):
                found = True
        if not found:
            ns.write(f"{f}\n")
            cnt += 1
    ns.close()
    print(cnt)


# focus on not yet supported
build_all()
# build_not_supported()
# jsonbuilder("BtEurope")
# jsonbuilder("Colt")
# cleanup()
