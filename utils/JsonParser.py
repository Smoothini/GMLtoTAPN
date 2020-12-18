import json
from entities.Node import Node
import utils.LtLBuilder as LTL
class JsonParser:
    def __init__(self, network):
        self.network = network
        self.data = self.read_json(network)

        self.init_route = self.data["Initial_routing"]
        self.final_route = self.data["Final_routing"]
        self.full_route = self.data["Initial_routing"].copy()
        self.full_route.extend(self.data["Final_routing"].copy())
        self.properties = self.data["Properties"]
        self.waypoint = self.properties["Waypoint"]
        self.loopfreedom = self.properties["LoopFreedom"]
        self.reachability = self.properties["Reachability"]


        self.routings = self.get_routings(self.data["Final_routing"])
        self.unique_ids = list(set.union(self.get_nodes_from_routing(self.data["Initial_routing"]), self.get_nodes_from_routing(self.data["Final_routing"])))

    def read_json(self, network):
        with open(f"data/json/{network}.json") as f:
            data = json.load(f)
            return data
    
    def scale_data(self, scale):
        self.data = LTL.scale_json(self.data, scale)

    def get_routings(self, routing):
        tuples = []
        for i in routing:
            tuples.append(tuple(i))
        return tuples

    def get_nodes_from_routing(self, routing):
        result = set()
        for i in routing:
            for j in i:
                result.add(j)
        return result
