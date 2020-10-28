import json
from typing import List
from entities.Node import Node


def get_routings(routing) -> List[tuple]:
    tuples = []
    for i in routing:
        tuples.append(tuple(i))
    return tuples


def get_nodes_from_routing(routing) -> set:
    result = set()
    for i in routing:
        for j in i:
            result.add(j)
    return result

def get_initial_routing(json_file: str) -> List[List]:
    routing: list = []
    with open(json_file) as file:
        data = json.load(file)
        for i in data["Initial_routing"]:
            routing.append(i)
    return routing


def get_final_routing(json_file: str) -> List[List]:
    routing: list = []
    with open(json_file) as file:
        data = json.load(file)
        for i in data["Final_routing"]:
            routing.append(i)
    return routing


def get_properties(json_file: str) -> dict:
    properties: dict = {}
    with open(json_file) as file:
        data = json.load(file)
        for key, value in data.items():
            properties.__setitem__(key, value)
    return properties


init_route: List[List] = get_initial_routing("Initial_routing.json")
final_route: List[List] = get_final_routing("Final_routing.json")
properties = get_properties("properties.json")
routings = get_routings(final_route)
unique_ids = set.union(get_nodes_from_routing(init_route), get_nodes_from_routing(final_route))


