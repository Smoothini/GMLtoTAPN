import json
from entities.Node import Node

def read_json():
    with open("settings.json") as f:
        data = json.load(f)
        return data

def get_routings(routing):
    tuples = []
    for i in routing:
        tuples.append(tuple(i))
    return tuples

def get_nodes_from_routing(routing):
    result = set()
    for i in routing:
        for j in i:
            result.add(j)
    return result        

data = read_json()

init_route = data["Initial_routing"]
final_route = data["Final_routing"]
properties = data["Properties"]

routings = get_routings(data["Final_routing"])
unique_ids = list(set.union(get_nodes_from_routing(data["Initial_routing"]), get_nodes_from_routing(data["Final_routing"])))

print("init: {}\n final: {}\n props: {}\n routing: {}\n uniqueId: {}".format(init_route, final_route, properties, routings, unique_ids))

#print("init: {}\n final: {}\n props: {}\n routing: {}\n uniqueId: {}".format(data["Initial_routing"], data["Final_routing"], data["Properties"], routings, unique_ids))
