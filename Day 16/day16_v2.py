from time import time
import networkx as nx
import matplotlib.pyplot as plt
from copy import copy
from itertools import combinations


def timer_func(func):
    # This function shows the execution time of
    # the function object passed
    def wrap_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print(f'Function {func.__name__!r} executed in {(t2 - t1):.4f}s')
        return result

    return wrap_func


class Cave:
    def __init__(self, name, flow, connected):
        self.name = name
        self.flow = flow
        self.connected = connected
        self.valve_connect = {}  # path length to caves with valves that can flow

    def __str__(self):
        return f'Cave {self.name}'

    def __repr__(self):
        return f'Cave {self.name}'


def cave_search(start, path, time_rem, flow, valid_paths):
    for cave in start.valve_connect:
        if cave in path or cave == start:
            continue
        elif time_rem - start.valve_connect[cave] <= 0:
            continue
        else:
            new_time_rem = time_rem - start.valve_connect[cave]
            new_flow = flow + new_time_rem * cave.flow
            valid_paths[frozenset(path.union({cave}))] = max(valid_paths.get(frozenset(path.union({cave})), 0), new_flow)
            valid_paths = cave_search(cave, path.union({cave}), new_time_rem, new_flow, valid_paths)
    return valid_paths


@timer_func
def day16(filepath, part2=False):
    with open(filepath) as fin:
        lines = fin.readlines()

    caves = []
    closed_valves = []

    for line in lines:
        cave = line.split()[1]
        flow_rate = int(line.split('=')[-1].split(';')[0])
        if 'valves' in line:
            connected_caves = [entry.strip() for entry in line.split('lead to valves')[-1].split(',')]
        else:
            connected_caves = [line.split('leads to valve')[-1].strip()]
        caves.append(Cave(cave, flow_rate, connected_caves))
        if caves[-1].flow > 0:
            closed_valves.append(caves[-1])
        if caves[-1].name == 'AA':
            start = caves[-1]

    G = nx.Graph()
    for cave in caves:
        for c_cave in cave.connected:
            for cave1 in caves:
                if cave1.name == c_cave:
                    v = cave1
                    break
            G.add_edge(cave, v)

    for cave in closed_valves:
        start.valve_connect[cave] = len(nx.shortest_path(G, start, cave))
        for cave1 in closed_valves:
            if cave1 != cave:
                cave.valve_connect[cave1] = len(nx.shortest_path(G, cave, cave1))

    if not part2:
        valid_paths = cave_search(start, set(), 30, 0, {})

        return max([flow for flow in valid_paths.values()])
    else:
        valid_paths2 = cave_search(start, set(), 26, 0, {})

        return max([f_me + f_e
                    for path_me, f_me in valid_paths2.items()
                    for path_e, f_e in valid_paths2.items()
                    if not path_e.intersection(path_me)])


def main():
    assert day16('test16') == 1651
    print(f"Part 1: {day16('input16')}")

    assert day16('test16', True) == 1707
    print(f"Part 1: {day16('input16', True)}")


if __name__ == '__main__':
    main()
