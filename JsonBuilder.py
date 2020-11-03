import networkx as nx
import json, time
import random
import os

def jsonbuilder(network):
    mydic = {} #haha yes ;^)
    # Init
    # Final
    # yes no waypoint
    # yes no loopfree
    # reachability
    start = time.time()
    g = nx.read_gml("data/gml/" + network + '.gml', label='id')
    g = nx.Graph(g)

    nodes_raw = list(g.nodes(data=True))
    n = len(nodes_raw)
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


    #it = 0
    #itt = 0
    #for source in range(n-1):
    #    for target in range(n):
    #        path = list(nx.all_simple_paths(g, source = source, target = target))
    #        it += 1
    #        itt += len(path)
    #for filee in os.listdir("archive"):
    #    f = open(f"archive/{filee}", "r")
    #    contents = f.readlines()
    #    f.close()

    #    contents.insert(2, "  multigraph 1\n")

    #    f = open(f"archive/{filee}", "w")
    #    contents = "".join(contents)
    #    f.write(contents)
    #    f.close()
    #for f in os.listdir("archive"):
        #print(f)
     #   g = nx.read_gml("archive/" + f, label='id')
      #  g = nx.DiGraph(g)
       # if nx.is_directed_acyclic_graph(g):
        #    print(f)
    


    #print(nx.is_directed(g))
    #print(nx.is_directed_acyclic_graph(g))


    myjsondic = json.dumps(mydic, indent = 4)
    f = open(f"net_settings/{network}.json", "w")
    f.write(myjsondic)
    f.close()
    print("Success! Json settings generated! Execution time: {} seconds".format((str(time.time()-start))[:5]))
    #print("{} iterations, {} actual cycles".format(it, itt))
    #print(str(mydic))
    #print(str(myjsondic))