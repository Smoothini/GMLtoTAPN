import json

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

def make_ltl(ntype,count):
    cnt_backup = count
    with open(f"data/json_custom_testcases/{ntype}_{count}.json") as f:
        data = json.load(f)

    count = data["Properties"]["Reachability"]["finalNode"]+1
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
    
    reach = f"(port=in{inn}s -> !(port=out{outt}s))"
    wp = f"(port=in{wpp}s) & (TRUE U (port=out{outt}s))"
    ltl += f"({reach} U {wp})"
#(port=in5s -> !(port=out16s) U ((port=in10s) & (TRUE U (port=out16s))))
    f = open(f"data/ltl_custom_testcases/{ntype}_{cnt_backup}.ltl", "w")
    f.write(ltl)
    f.close()

    print(f"LTL for {ntype} network of size {cnt_backup} generated")


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