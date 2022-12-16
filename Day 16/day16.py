from time import time
import networkx as nx
import matplotlib.pyplot as plt
from copy import copy


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

    def __str__(self):
        return f'Cave {self.name}'

    def __repr__(self):
        return f'Cave {self.name}'


def cave_walk(time_rem, G, start, closed_valves):
    if len(closed_valves) == 0:
        return 0
    total_flows = []
    for valve in closed_valves:
        result = nx.shortest_path(G, start, valve)
        time_used = len(result)
        if time_rem - time_used <= 0:
            total_flows.append(0)
            continue
        total_flow = valve.flow * (time_rem - time_used)
        rem_closed_valves = copy(closed_valves)
        rem_closed_valves.pop(rem_closed_valves.index(valve))
        other_flow = cave_walk(time_rem - time_used, G, valve, rem_closed_valves)
        total_flows.append(total_flow + other_flow)
    return max(total_flows)


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
    # nx.draw_networkx(G)
    # plt.show()

    time_remaining = 30
    max_flow = cave_walk(time_remaining, G, start, closed_valves)
    return max_flow


def main():
    assert day16('test16') == 1651
    print(f"Part 1: {day16('input16')}")

    # assert day16('test16', True) == 1
    # print(f"Part 2: {day16('input16', True)}")


if __name__ == '__main__':
    main()
