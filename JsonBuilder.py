import networkx as nx
import json, time
import random
import os
import graph_tool.all as gt

def jsonbuilder(network):
    mydic = {}
    start = time.time()
    g = nx.read_gml("data/gml/" + network + ".gml", label='id')
    g = nx.Graph(g)

    nodes_raw = list(g.nodes(data=True))
    n = len(nodes_raw)
    #
    lmax = 0
    s, t = -1, -1
    init_path = []
    for source in range(n):
        for target in range(n-1):
            l = nx.shortest_path_length(g, source = source, target = target)
            if l > lmax:
                lmax = l
                s, t = source, target
                init_path = list(nx.shortest_path(g, source = source, target = target))
    print(f"Max shortest path: {lmax}, between {s} and {t}")
    print(f"Path: {init_path}")
    all_paths = list(nx.all_simple_paths(g, source = s, target = t))
    lmax_path = 0
    final_path = []
    print(f"Amount of paths: {len(all_paths)}")
    for path in all_paths:
        if len(path) > lmax_path:
            lmax_path = len(path)
            final_path = path
    print(f"Biggest path size: {lmax_path}")
    print(f"Path: {str(final_path)}")    
    s1 = set(init_path[1:-1])
    s2 = set(final_path[1:-1])
    wps = list(s1.intersection(s2))
    print(f"Common waypoints: {wps}")
    init_route = []
    final_route = []
    for t in range(len(init_path) - 1):
        init_route.append([init_path[t], init_path[t+1]])
    for t in range(len(final_path) - 1):
        final_route.append([final_path[t], final_path[t+1]])
    print(f"Init routing: {init_route}")
    print(f"Final routing: {final_route}")
    mydic["Initial_routing"] = init_route
    mydic["Final_routing"] = final_route
    mydic["Properties"] = {}
    if len(wps):
        mydic["Properties"]["Waypointing"] = True
        mydic["Properties"]["WaypointNodeIds"] = wps
    else:
        mydic["Properties"]["Waypointing"] = False
    mydic["Properties"]["LoopFreedom"] = True
    mydic["Properties"]["Reachability"] = init_path[-1]


    myjsondic = json.dumps(mydic, indent = 4)
    f = open(f"data/json/{network}.json", "w")
    f.write(myjsondic)
    f.close()
    print("Success! Json settings for {} generated! Execution time: {} seconds".format(network, (str(time.time()-start))[:5]))

##in progress, doesn't look very gang gang so far..
def jsonGtBuilder(network):
    start = time.time()
    g = gt.load_graph(f"data/gml/{network}.gml")
    n = g.num_vertices()

    lmax = 0
    s = -1
    t = -1
    init_path = []

    for source in range(n):
        for target in range(n-1):
            v, e = gt.shortest_path(g, source, target)
            if len(v) > lmax:
                lmax = len(v)
                s = source
                t = target
                init_path = e

    print(f" source: {s}\n target: {t}\n path: {lmax}")

    print(f"{str(time.time() - start)[:-4]} seconds")


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
    print("Operation done in: {} seconds".format((str(time.time()-start))[:5]))

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
    print("Operation done in: {} seconds".format((str(time.time()-start))[:5]))
    print(f"Not build: {cnt}")


def cleanup():
    ns = open("not yet supported.txt", "w")
    cnt = 0
    for f in os.listdir("data/gml/"):
        found = False
        for g in os.listdir("data/json/"):
            if(f[:-4] == g[:-5]):
                found = True
        if not found:
            ns.write(f"{f}\n")
            cnt+=1
    ns.close()
    print(cnt)


#focus on not yet supported
#build_all()
#build_not_supported()
jsonGtBuilder("Colt")

#cleanup()