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
            valid_paths[path + tuple([cave])] = {'time': new_time_rem, 'flow': new_flow}
            valid_paths = cave_search(cave, path + tuple([cave]), new_time_rem, new_flow, valid_paths)
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

    valid_paths = cave_search(start, (), 30, 0, {})

    max_flow = max([val['flow'] for val in valid_paths.values()])
    print(f'Part 1: {max_flow}')

    closed_valves_len = len(closed_valves)
    new_valid_paths = {}
    for key, value in valid_paths.items():
        if value['time'] > 4:
            new_valid_paths[key] = value
    flows = []
    for a, b in combinations(new_valid_paths, 2):
        if len(set(a).intersection(b)) > 0:
            continue
        else:
            time_rem = 26 - start.valve_connect[a[0]]
            a_flow = a[0].flow*time_rem
            if len(a) > 1:
                for i, entry in enumerate(a[1:]):
                    time_rem = time_rem - a[i].valve_connect[entry]
                    a_flow += time_rem * entry.flow
            time_rem = 26 - start.valve_connect[b[0]]
            b_flow = b[0].flow * time_rem
            if len(b) > 1:
                for i, entry in enumerate(b[1:]):
                    time_rem = time_rem - b[i].valve_connect[entry]
                    b_flow += time_rem * entry.flow

            flows.append(a_flow + b_flow)

    max_flow = max(flows)
    print(f'Part 2: {max_flow}')


def main():
    day16('test16')

    day16('input16')


if __name__ == '__main__':
    main()
