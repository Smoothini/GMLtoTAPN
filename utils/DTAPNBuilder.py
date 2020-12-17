#TODO pass initial place as argument or something
#TODO queries
import json, time

def build_composed_model(params, path, negative = False):
    start = time.time()
    count, ntype, places, transitions, _, _, acc = params
    count = acc
    path = path
    with open(f"data/json_custom_testcases/{ntype}_{count}.json") as f:
        json_params = json.load(f)

    switches = []
    ctrl = "Controller"
    inject = "Inject_packet"
    clock = "Clock"
    
    xml = ""
    xml += "<pnml>\n"
    xml += "<net id=\"ComposedModel\" type=\"P/T net\">\n"

    ## Places part
    xml += f"<place id=\"{ctrl}\" name=\"{ctrl}\" invariant=\"&lt; inf\" initialMarking=\"1\" />\n"
    for place in places:
        xml += f"<place id=\"{place.notation}\" name=\"{place.notation}\" invariant=\"&lt; inf\" initialMarking=\"0\" />\n"
    xml += f"<place id=\"{clock}\" name=\"{clock}\" invariant=\"&lt;= 0\" initialMarking=\"1\" />\n"
    xml += "<place id=\"P_u_visited\" name=\"P_u_visited\" invariant=\"&lt; inf\" initialMarking=\"0\" />\n"
    for place in places:
        if place.init_route and place.final_route:
            if place.init_route != place.final_route:
                xml += f"<place id=\"{place.notation}_initial\" name=\"{place.notation}_initial\" invariant=\"&lt; inf\" initialMarking=\"1\" />\n"
                xml += f"<place id=\"{place.notation}_final\" name=\"{place.notation}_final\" invariant=\"&lt; inf\" initialMarking=\"0\" />\n"
                switches.append(place)
    for place in places:
        xml += f"<place id=\"{place.notation}_visited\" name=\"{place.notation}_visited\" invariant=\"&lt; inf\" initialMarking=\"0\" />\n"

    ## Transitions part
    for t in transitions:
        xml += f"<transition player=\"0\" id=\"{t.notation}\" name=\"{t.notation}\" urgent=\"false\"/>\n"
    xml += f"<transition player=\"1\" id=\"{inject}\" name=\"{inject}\" urgent=\"false\"/>\n"
    for t in switches:
        xml += f"<transition player=\"0\" id=\"Update_{t.notation}\" name=\"Update_{t.notation}\" urgent=\"false\"/>\n"

    ## Input arcs part
    for t in transitions:
        xml += f"<inputArc inscription=\"[0,inf)\" source=\"P{t.source}\" target=\"{t.notation}\" />\n"
    xml += f"<inputArc inscription=\"[0,inf)\" source=\"{ctrl}\" target=\"{inject}\" />\n"
    for t in switches:
        xml += f"<inputArc inscription=\"[0,inf)\" source=\"{ctrl}\" target=\"Update_{t.notation}\" />\n"
        xml += f"<inputArc inscription=\"[0,inf)\" source=\"{t.notation}_initial\" target=\"Update_{t.notation}\" />\n"
        xml += f"<inputArc inscription=\"[0,inf)\" source=\"{t.notation}_initial\" target=\"T{t.id}_{t.init_route}\" />\n"
        xml += f"<inputArc inscription=\"[0,inf)\" source=\"{t.notation}_final\" target=\"T{t.id}_{t.final_route}\" />\n"

    ## Output arcs part
    for t in transitions:
        xml += f"<outputArc inscription=\"1\" source=\"{t.notation}\" target=\"P{t.target}\" />\n"
    xml += f"<outputArc inscription=\"1\" source=\"{inject}\" target=\"P{places[0].id}\" />\n"
    xml += f"<outputArc inscription=\"1\" source=\"{inject}\" target=\"P_u_visited\" />\n"
    for t in switches:
        xml += f"<outputArc inscription=\"1\" source=\"Update_{t.notation}\" target=\"{ctrl}\" />\n"
        xml += f"<outputArc inscription=\"1\" source=\"Update_{t.notation}\" target=\"{t.notation}_final\" />\n"
        xml += f"<outputArc inscription=\"1\" source=\"T{t.id}_{t.init_route}\" target=\"{t.notation}_initial\" />\n"
        xml += f"<outputArc inscription=\"1\" source=\"T{t.id}_{t.final_route}\" target=\"{t.notation}_final\" />\n"
    for place in places:
        for t in transitions:
            if t.target == place.id:
                xml += f"<outputArc inscription=\"1\" source=\"{t.notation}\" target=\"{place.notation}_visited\" />\n"

    ## Inhibitor arcs part
    if places[0].init_route != places[0].final_route:
        xml += f"<inhibitorArc inscription=\"[0,inf)\" source=\"P_u_visited\" target=\"T{places[0].id}_{places[0].init_route}\" weight=\"2\"/>\n"
        xml += f"<inhibitorArc inscription=\"[0,inf)\" source=\"P_u_visited\" target=\"T{places[0].id}_{places[0].final_route}\" weight=\"2\"/>\n"
    else:
        xml += f"<inhibitorArc inscription=\"[0,inf)\" source=\"P_u_visited\" target=\"T{places[0].id}_{places[0].init_route}\" weight=\"2\"/>\n"
    for place in places:
        if place.init_route:
            xml += f"<inhibitorArc inscription=\"[0,inf)\" source=\"{place.notation}_visited\" target=\"T{place.id}_{place.init_route}\" weight=\"2\"/>\n"
        if place.final_route:
            xml += f"<inhibitorArc inscription=\"[0,inf)\" source=\"{place.notation}_visited\" target=\"T{place.id}_{place.final_route}\" weight=\"2\"/>\n"
        
    xml += "</net>\n"
    xml += "</pnml>"
    f = open(f"{path}/{ntype}_{count}.xml", "w")
    f.write(xml)
    f.close

    f = open(f"data/time/{ntype}/{ntype}_{count}_DXML.txt", "w")
    f.write(str(time.time() - start))
    f.close()

    print(f"DTAPN XML for {ntype} network of size {count} generated in {time.time()-start} seconds")

    start = time.time()
    reach = json_params["Properties"]["Reachability"]["finalNode"]
    waypoint = json_params["Properties"]["Waypoint"]["waypoint"]
    

    f = open(f"{path}/{ntype}_{count}.q", "w")
    f.write(build_query(reach=reach, waypoint=waypoint, negative=negative))
    f.close

    f = open(f"data/time/{ntype}/{ntype}_{count}_DQuery.txt", "w")
    f.write(str(time.time() - start))
    f.close()

    print(f"DTAPN Query file for {ntype} network of size {count} generated in {time.time()-start} seconds")

def build_query(ntype=None, reach=None, waypoint=None, negative=False):
    if negative:
        x = reach
        reach = waypoint
        waypoint = x
    query = "control: "
    #((!(deadlock) or P10_visited >= 1) and (P9_visited >= 1 or P10 = 0))
    r0,s0 = magnisep(reach)
    w0,s1 = magnisep(waypoint)
    q = f"AG ((!(deadlock) or P{r0}_visitedxxx{s0} >= 1) and (P{w0}_visitedxxx{s1} >= 1 or P{r0}xxx{s0} = 0))"
    query += q
    return query

def magnisep(data):
    val, magni = data.split("xxx")
    return val,magni

def build_composed_model_gml(fname, places, transitions, path, negative = False, uber = False, wp=None, pn=None):
    start = time.time()
    path = path
    with open(f"data/json/{fname}.json") as f:
        json_params = json.load(f)

    switches = []
    ctrl = "Controller"
    inject = "Inject_packet"
    clock = "Clock"
    
    xml = ""
    xml += "<pnml>\n"
    xml += "<net id=\"ComposedModel\" type=\"P/T net\">\n"

    ## Places part
    xml += f"<place id=\"{ctrl}\" name=\"{ctrl}\" invariant=\"&lt; inf\" initialMarking=\"1\" />\n"
    for place in places:
        xml += f"<place id=\"{place.notation}\" name=\"{place.notation}\" invariant=\"&lt; inf\" initialMarking=\"0\" />\n"
    xml += f"<place id=\"{clock}\" name=\"{clock}\" invariant=\"&lt;= 0\" initialMarking=\"1\" />\n"
    xml += "<place id=\"P_u_visited\" name=\"P_u_visited\" invariant=\"&lt; inf\" initialMarking=\"0\" />\n"
    for place in places:
        if place.init_route and place.final_route:
            if place.init_route != place.final_route:
                v0,m0 = magnisep(place.notation)
                xml += f"<place id=\"{v0}_initialxxx{m0}\" name=\"{v0}_initialxxx{m0}\" invariant=\"&lt; inf\" initialMarking=\"1\" />\n"
                xml += f"<place id=\"{v0}_finalxxx{m0}\" name=\"{v0}_finalxxx{m0}\" invariant=\"&lt; inf\" initialMarking=\"0\" />\n"
                switches.append(place)
    for place in places:
        v0,m0 = magnisep(place.notation)
        xml += f"<place id=\"{v0}_visitedxxx{m0}\" name=\"{v0}_visitedxxx{m0}\" invariant=\"&lt; inf\" initialMarking=\"0\" />\n"

    ## Transitions part
    for t in transitions:
        xml += f"<transition player=\"0\" id=\"{t.notation}\" name=\"{t.notation}\" urgent=\"false\"/>\n"
    xml += f"<transition player=\"1\" id=\"{inject}\" name=\"{inject}\" urgent=\"false\"/>\n"
    for t in switches:
        xml += f"<transition player=\"0\" id=\"Update_{t.notation}\" name=\"Update_{t.notation}\" urgent=\"false\"/>\n"
    
    ## Input arcs part
    for t in transitions:
        #print(f"   ID: {t.id}   S: {t.source} T: {t.target}  N: {t.notation}")
        xml += f"<inputArc inscription=\"[0,inf)\" source=\"P{t.source}\" target=\"{t.notation}\" />\n"
    xml += f"<inputArc inscription=\"[0,inf)\" source=\"{ctrl}\" target=\"{inject}\" />\n"
    for t in switches:
        xml += f"<inputArc inscription=\"[0,inf)\" source=\"{ctrl}\" target=\"Update_{t.notation}\" />\n"
        v0, m0 = magnisep(t.notation)
        xml += f"<inputArc inscription=\"[0,inf)\" source=\"{v0}_initialxxx{m0}\" target=\"Update_{t.notation}\" />\n"
        if uber:
            v0,m0 = magnisep(t.id)
            v1,m1 = magnisep(t.init_route)
            v2,m2 = magnisep(t.final_route)
            v3,m3 = magnisep(t.notation)
            xml += f"<inputArc inscription=\"[0,inf)\" source=\"{v3}_initialxxx{m0}\" target=\"T{v0}_{v1}xxx{m0}\" />\n"
            xml += f"<inputArc inscription=\"[0,inf)\" source=\"{v3}_finalxxx{m0}\" target=\"T{v0}_{v2}xxx{m0}\" />\n"
        else:
            xml += f"<inputArc inscription=\"[0,inf)\" source=\"{t.notation}_initial\" target=\"T{t.id}_{t.init_route}\" />\n"
            xml += f"<inputArc inscription=\"[0,inf)\" source=\"{t.notation}_final\" target=\"T{t.id}_{t.final_route}\" />\n"
    
    ## Output arcs part
    for t in transitions:
        xml += f"<outputArc inscription=\"1\" source=\"{t.notation}\" target=\"P{t.target}\" />\n"
    xml += f"<outputArc inscription=\"1\" source=\"{inject}\" target=\"P{places[0].id}\" />\n"
    xml += f"<outputArc inscription=\"1\" source=\"{inject}\" target=\"P_u_visited\" />\n"
    for t in switches:
        v0,m0 = magnisep(t.notation)
        xml += f"<outputArc inscription=\"1\" source=\"Update_{t.notation}\" target=\"{ctrl}\" />\n"
        xml += f"<outputArc inscription=\"1\" source=\"Update_{t.notation}\" target=\"{v0}_finalxxx{m0}\" />\n"
        if uber:
            v0,m0 = magnisep(t.id)
            v1,m1 = magnisep(t.init_route)
            v2,m2 = magnisep(t.final_route)
            v3,m3 = magnisep(t.notation)
            xml += f"<outputArc inscription=\"1\" source=\"T{v0}_{v1}xxx{m0}\" target=\"{v3}_initialxxx{m0}\" />\n"
            xml += f"<outputArc inscription=\"1\" source=\"T{v0}_{v2}xxx{m0}\" target=\"{v3}_finalxxx{m0}\" />\n"
        else:
            xml += f"<outputArc inscription=\"1\" source=\"T{t.id}_{t.init_route}\" target=\"{t.notation}_initial\" />\n"
            xml += f"<outputArc inscription=\"1\" source=\"T{t.id}_{t.final_route}\" target=\"{t.notation}_final\" />\n"
    for place in places:
        for t in transitions:
            if t.target == place.id:
                v0, m0 = magnisep(place.notation)
                xml += f"<outputArc inscription=\"1\" source=\"{t.notation}\" target=\"{v0}_visitedxxx{m0}\" />\n"

    ## Inhibitor arcs part
    if uber:
        v0,m0 = magnisep(places[0].id)
        v1,m1 = magnisep(places[0].init_route)
        v2,m2 = magnisep(places[0].final_route)
        if places[0].init_route != places[0].final_route:
            print(v0, v1, v2)
            xml += f"<inhibitorArc inscription=\"[0,inf)\" source=\"P_u_visited\" target=\"T{v0}_{v1}xxx{m0}\" weight=\"2\"/>\n"
            xml += f"<inhibitorArc inscription=\"[0,inf)\" source=\"P_u_visited\" target=\"T{v0}_{v2}xxx{m0}\" weight=\"2\"/>\n"
        else:
            print(v0, v1, v2)
            xml += f"<inhibitorArc inscription=\"[0,inf)\" source=\"P_u_visited\" target=\"T{v0}_{v1}xxx{m0}\" weight=\"2\"/>\n"
    else:    
        if places[0].init_route != places[0].final_route:
            xml += f"<inhibitorArc inscription=\"[0,inf)\" source=\"P_u_visited\" target=\"T{places[0].id}_{places[0].init_route}\" weight=\"2\"/>\n"
            xml += f"<inhibitorArc inscription=\"[0,inf)\" source=\"P_u_visited\" target=\"T{places[0].id}_{places[0].final_route}\" weight=\"2\"/>\n"
        else:
            xml += f"<inhibitorArc inscription=\"[0,inf)\" source=\"P_u_visited\" target=\"T{places[0].id}_{places[0].init_route}\" weight=\"2\"/>\n"
    

    for place in places:
        if uber:
            v0,m0 = magnisep(place.id)
            v3,m3 = magnisep(place.notation)
            #print(f"{place.id} {place.init_route} {place.final_route}")
            if place.init_route != None:
                v1,m1 = magnisep(place.init_route)
                xml += f"<inhibitorArc inscription=\"[0,inf)\" source=\"{v3}_visitedxxx{m0}\" target=\"T{v0}_{v1}xxx{m0}\" weight=\"2\"/>\n"
            if place.final_route != None:
                v2,m2 = magnisep(place.final_route)
                xml += f"<inhibitorArc inscription=\"[0,inf)\" source=\"{v3}_visitedxxx{m0}\" target=\"T{v0}_{v2}xxx{m0}\" weight=\"2\"/>\n"
        else:    
            if place.init_route:
                xml += f"<inhibitorArc inscription=\"[0,inf)\" source=\"{place.notation}_visited\" target=\"T{place.id}_{place.init_route}\" weight=\"2\"/>\n"
            if place.final_route:
                xml += f"<inhibitorArc inscription=\"[0,inf)\" source=\"{place.notation}_visited\" target=\"T{place.id}_{place.final_route}\" weight=\"2\"/>\n"
                
    xml += "</net>\n"
    xml += "</pnml>"
    f = open(f"{path}{fname}.xml", "w")
    f.write(xml)
    f.close

    f = open(f"data/time/ZOO/{fname}_DXML.txt", "w")
    f.write(str(time.time() - start))
    f.close()

    print(f"DTAPN XML for {fname} network generated in {time.time()-start} seconds")

    start = time.time()
    if uber == True:
        reach = pn
        waypoint = wp
    else:
        reach = json_params["Properties"]["Reachability"]["finalNode"]
        waypoint = json_params["Properties"]["Waypoint"]["waypoint"]
    

    f = open(f"{path}{fname}.q", "w")
    f.write(build_query(reach=reach, waypoint=waypoint, negative=negative))
    f.close

    f = open(f"data/time/ZOO/{fname}_DQuery.txt", "w")
    f.write(str(time.time() - start))
    f.close()

    print(f"DTAPN Query file for {fname} network generated in {time.time()-start} seconds")