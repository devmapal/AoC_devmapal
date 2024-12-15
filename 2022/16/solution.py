from dataclasses import dataclass
from itertools import combinations
import math
from pprint import pprint
import re
from typing import FrozenSet, Mapping, Set
import networkx as nx


@dataclass
class NodeProperties:
    rate: int
    open: bool = False


properties_by_name: Mapping[str, NodeProperties] = {}

G = nx.Graph()
with open("input") as a_file:
    line_pattern = re.compile(
        r"Valve (?P<name>[A-Z]{2}).*rate=(?P<rate>\d+).*valves? (?P<valves>.*)"
    )
    while line := a_file.readline():
        line = line.strip()
        if line == "":
            continue

        match = re.search(pattern=line_pattern, string=line)
        name = match.group("name")
        rate = int(match.group("rate"))
        valves = match.group("valves").split(", ")

        G.add_edges_from(((name, valve) for valve in valves))
        properties_by_name[name] = NodeProperties(rate=rate)


@dataclass(frozen=True)
class Key:
    passed_nodes: FrozenSet[str]
    target: str


targets = [node for node in G.nodes() if properties_by_name[node].rate > 0]
target_set = set(targets)

# Klep-Karp Algorithm
start = "AA"
path_values = {}
previous_nodes = {}
path_len = {}

TIME = 30
# k is length of previous paths
for k in range(len(targets)):
    # passed_nodes is the set of nodes previously passed, iterating through all combinations of lenght k
    for passed_nodes in (frozenset(nodes) for nodes in combinations(targets, k)):
        # computing the best path to target ...
        for target in target_set - passed_nodes:
            # ... from the nodes already passed, or start if we haven't passed any yet, taking the best path of those
            best = -math.inf
            previous_node = None
            best_path_len = None
            for starting_node in passed_nodes or {start}:
                key = Key(
                    passed_nodes=passed_nodes - {starting_node},
                    target=starting_node,
                )
                prev_path_len = 0 if key not in path_len else path_len[key]
                path = nx.shortest_path(G, starting_node, target)
                path_value = properties_by_name[target].rate * (
                    TIME - len(path) - prev_path_len
                )

                if passed_nodes - {start}:
                    path_value += path_values[key]

                if path_value > best:
                    best = path_value
                    previous_node = starting_node
                    best_path_len = len(path) + prev_path_len

            key = Key(
                passed_nodes=passed_nodes,
                target=target,
            )
            path_values[key] = best
            previous_nodes[key] = previous_node
            path_len[key] = best_path_len

print(max(path_values.values()))
