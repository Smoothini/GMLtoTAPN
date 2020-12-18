import json,os,csv
import time

class Switch:
    def __init__(self, sid, out1 = None, out2 = None):
        self.sid = sid
        self.out1 = None
        self.out2 = None
        if out1:
            self.out1 = out1
        if out2:
            self.out2 = out2
    def info(self):
        if (self.out1 and self.out2):
            return(f"""switch {self.sid} (in{self.sid}s,out{self.sid}s,out{self.sid}s_2) [] {{
 rule in{self.sid}s => out{self.sid}s []
 }}
 final {{
 rule in{self.sid}s => out{self.sid}s_2 []
 }}\n""")
        elif (self.out1):
            return(f"""switch {self.sid} (in{self.sid}s,out{self.sid}s) [] {{
 rule in{self.sid}s => out{self.sid}s []
 }}
 final {{
     
 }}\n""")

        elif (self.out2):
            return(f"""switch {self.sid} (in{self.sid}s,out{self.sid}s_2) [] {{

 }}
 final {{
 rule in{self.sid}s => out{self.sid}s_2 []
 }}\n""")
        else:
            return(f"""switch {self.sid} (in{self.sid}s,out{self.sid}s) [] {{
 rule in{self.sid}s => out{self.sid}s []
 }}
 final {{
 rule in{self.sid}s => out{self.sid}s []
 }}\n""")

    def links(self):
        if (self.out1 and self.out2):
            return (f"link out{self.sid}s => in{self.out1}s []\n" + f"link out{self.sid}s_2 => in{self.out2}s []\n")
        elif self.out1:
            return f"link out{self.sid}s => in{self.out1}s []\n"
        elif self.out2:
            return f"link out{self.sid}s_2 => in{self.out2}s []\n"


def find_switch(switches, sid):
    return next((x for x in switches if x.sid == sid), None)

def make_ltl(ntype,count,path="data/json_custom_testcases"):
    start = time.time()
    cnt_backup = count
    with open(f"data/json_custom_testcases/{ntype}_{count}.json") as f:
        data = json.load(f)

    count = data["Properties"]["Waypoint"]["finalNode"]+1
    switches = []

    for i in range(count):
        switches.append(Switch(i))
    
    init_route = data["Initial_routing"]
    final_route = data["Final_routing"]

    for edge in init_route:
        switch = find_switch(switches,edge[0])
        switch.out1 = edge[1]

    for edge in final_route:
        switch = find_switch(switches,edge[0])
        switch.out2 = edge[1]
    
    switch_init = find_switch(switches, data["Properties"]["Reachability"]["startNode"])
    ltl = ""
    for s in switches:
        ltl += s.info()
    
    ltl += f"link  => in{switch_init.sid}s []\n"

    for s in switches[:-1]:
        ltl += s.links()
    
    ltl += "spec\n"
    inn = data["Properties"]["Reachability"]["startNode"]
    outt = data["Properties"]["Reachability"]["finalNode"]
    wpp = data["Properties"]["Waypoint"]["waypoint"]
    
    init = f"port=in{inn}s"

    #x = outt
    #outt = wpp
    #wpp = x

    reach = f"!(port=out{outt}s)"
    wp = f"((port=in{wpp}s) & (TRUE U (port=out{outt}s)))"
    spec = f"{init} -> ({reach} U {wp})"

    ltl += spec
    #print(spec)
    #port=in0s ->    (! U ( & (U )
    #port=in0s ->    (!(port=out3s) U ((port=in1s) & (TRUE U (port=out3s)))

    #port=in0s ->    (!(port=out3s) U ((port=in1s) & (TRUE U (port=out3s))))
    f = open(f"data/ltl_custom_testcases/{ntype}_{cnt_backup}.ltl", "w")
    f.write(ltl)
    f.close()

    f = open(f"data/time/{ntype}/{ntype}_{cnt_backup}_LTL.txt", "w")
    f.write(str(time.time() - start))
    f.close()

    print(f"LTL for {ntype} network of size {cnt_backup} generated in {time.time()-start} seconds")



def make_ltl_zoo(fname):
    start = time.time()
    with open(f"data/json/{fname}.json") as f:
        data = json.load(f)
    sw = []
    for i in data["Initial_routing"]:
        sw.append(i[0])

    for i in data["Final_routing"]:
        sw.append(i[0])
    sw.append(data["Final_routing"][-1][1])

    swnodup = list(dict.fromkeys(sw))
    print(swnodup)
    switches = []

    for i in swnodup:
        switches.append(Switch(i))
    
    init_route = data["Initial_routing"]
    final_route = data["Final_routing"]

    for edge in init_route:
        switch = find_switch(switches,edge[0])
        switch.out1 = edge[1]

    for edge in final_route:
        switch = find_switch(switches,edge[0])
        switch.out2 = edge[1]
    
    switch_init = find_switch(switches, data["Properties"]["Reachability"]["startNode"])
    ltl = ""
    for s in switches:
        ltl += s.info()
    
    ltl += f"link  => in{switch_init.sid}s []\n"

    for s in switches[:-1]:
        ltl += s.links()
    
    ltl += "spec\n"
    inn = data["Properties"]["Reachability"]["startNode"]
    outt = data["Properties"]["Reachability"]["finalNode"]
    wpp = data["Properties"]["Waypoint"]["waypoint"]
    
    init = f"port=in{inn}s"

    #x = outt
    #outt = wpp
    #wpp = x

    reach = f"!(port=out{outt}s)"
    wp = f"((port=in{wpp}s) & (TRUE U (port=out{outt}s)))"
    spec = f"{init} -> ({reach} U {wp})"

    ltl += spec
    #print(spec)
    #port=in0s ->    (! U ( & (U )
    #port=in0s ->    (!(port=out3s) U ((port=in1s) & (TRUE U (port=out3s)))

    #port=in0s ->    (!(port=out3s) U ((port=in1s) & (TRUE U (port=out3s))))
    f = open(f"data/ltl_zoo/{fname}.ltl", "w")
    f.write(ltl)
    f.close()

    f = open(f"data/time/LTLZOO/{fname}_LTL.txt", "w")
    f.write(str(time.time() - start))
    f.close()

    print(f"LTL for {fname} network generated in {time.time()-start} seconds")
    return (len(data["Initial_routing"]) + len(data["Final_routing"]))


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


def make_ltl_zoo_scale(fname, scale):
    start = time.time()
    with open(f"data/json/{fname}.json") as f:
        data = json.load(f)
    data = scale_json(data,scale)
    sw = []
    for i in data["Initial_routing"]:
        sw.append(i[0])

    for i in data["Final_routing"]:
        sw.append(i[0])
    sw.append(data["Final_routing"][-1][1])
    swnodup = list(dict.fromkeys(sw))
    switches = []

    for i in swnodup:
        switches.append(Switch(i))
    
    init_route = data["Initial_routing"]
    final_route = data["Final_routing"]

    for edge in init_route:
        switch = find_switch(switches,edge[0])
        switch.out1 = edge[1]

    for edge in final_route:
        switch = find_switch(switches,edge[0])
        switch.out2 = edge[1]
    
    switch_init = find_switch(switches, data["Properties"]["Reachability"]["startNode"])
    ltl = ""
    for s in switches:
        ltl += s.info()
    
    ltl += f"link  => in{switch_init.sid}s []\n"

    for s in switches[:-1]:
        ltl += s.links()
    
    ltl += "spec\n"
    inn = data["Properties"]["Reachability"]["startNode"]
    outt = data["Properties"]["Reachability"]["finalNode"]
    wpp = data["Properties"]["Waypoint"]["waypoint"]
    
    init = f"port=in{inn}s"

    #x = outt
    #outt = wpp
    #wpp = x

    reach = f"!(port=out{outt}s)"
    wp = f"((port=in{wpp}s) & (TRUE U (port=out{outt}s)))"
    spec = f"{init} -> ({reach} U {wp})"

    ltl += spec
    #print(spec)
    #port=in0s ->    (! U ( & (U )
    #port=in0s ->    (!(port=out3s) U ((port=in1s) & (TRUE U (port=out3s)))

    #port=in0s ->    (!(port=out3s) U ((port=in1s) & (TRUE U (port=out3s))))
    f = open(f"data/ltl_zoo_scale/{fname}.ltl", "w")
    f.write(ltl)
    f.close()

    f = open(f"data/time/LTLZOOSCALE/{fname}_LTL.txt", "w")
    f.write(str(time.time() - start))
    f.close()

    print(f"LTL for {fname} network generated in {time.time()-start} seconds")
    return (len(data["Initial_routing"]) + len(data["Final_routing"]))

def make_all():
    for i in range(10,110,10):
        make_ltl("Disjoint", i)
        make_ltl("Shared", i)
        make_ltl("Worst", i)
    for i in range(100,1100,100):
        make_ltl("Disjoint", i)
        make_ltl("Shared", i)
        make_ltl("Worst", i)
    #for i in range(2000,6000,1000):
     #   make_ltl("Disjoint", i)
      #  make_ltl("Shared", i)

def make_all_zoo():
    with open(f"zoosize.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Net", "Node count"])
        for f in os.listdir("data/gml/"):
            try:
                lenn = make_ltl_zoo(f[:-4])
                writer.writerow([f[:-4], lenn])
            except:
                print(f"Failure! {f[:-4]} not converted..")
        file.close()

def make_all_zoo_scale(scale):
    with open(f"zoo_scale_size.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Net", "Node count"])
        for f in os.listdir("data/gml/"):
            try:
                lenn = make_ltl_zoo_scale(f[:-4], scale)
                writer.writerow([f[:-4], lenn])
            except:
                print(f"Failure! {f[:-4]} not converted..")
        file.close()

