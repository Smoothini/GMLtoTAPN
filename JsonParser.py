import json
from typing import List
from entities.Node import Node


def get_unique_ids(routing) -> set:
    unique_ids = set()
    for i in routing:
        for j in i:
            unique_ids.add(j)
    return unique_ids

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

unique_ids = set.union(get_unique_ids(init_route), get_unique_ids(final_route))

def item_to_node_id(item: int) -> Node:
    return Node()


def items_to_node_ids(items: list):
    return map(items_to_node_ids(), items)
