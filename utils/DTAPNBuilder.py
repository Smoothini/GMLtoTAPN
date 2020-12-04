#TODO pass initial place as argument or something
#TODO queries

def build_composed_model(params):
    count, ntype, places, transitions, _, _ = params

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

    print(xml)

def build_query():
    query = ""

    query += "control: "
    query += "mota"
    print(query)