from time import time
from math import prod
import sys


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


def tuple_add(a: tuple, b: tuple) -> tuple:
    return tuple([c + d for c, d in zip(a, b)])


def get_adjacent(x: tuple) -> list[tuple, ...]:
    return [
        tuple_add(x, tuple([
            j if k == y else 0
            for k in range(len(x))
        ]))
        for j in [-1, 1]
        for y in range(len(x))
    ]


@timer_func
def day18(filepath, part2=False):
    with open(filepath) as fin:
        lines = [line.strip() for line in fin.readlines()]

    rock_points = set()
    surface_area = 0
    for line in lines:
        point = tuple(int(x) for x in line.split(','))
        if not part2:
            surface_area += 6
            for adj in get_adjacent(point):
                if adj in rock_points:
                    surface_area -= 2
        rock_points.add(point)
    if part2:
        valid_range = [[min(point[i] for point in rock_points) - 1, max(point[i] for point in rock_points) + 1]
                       for i in range(3)]
        min_point = tuple([valid_range[i][0] for i in range(3)])
        steam_points = set(min_point)
        q = [min_point]
        while q:
            cur = q.pop()
            for adj in get_adjacent(cur):
                if all([valid_range[i][0] <= adj[i] <= valid_range[i][1]
                        for i in range(3)]):
                    pass
                else:
                    continue
                if adj in rock_points:
                    surface_area += 1
                elif adj in steam_points:
                    continue
                else:
                    steam_points.add(adj)
                    q.append(adj)


    return surface_area


def main():
    assert day18('test18') == 64
    print(f"Part 1: {day18('input18')}")

    assert day18('test18', True) == 58
    print(f"Part 2: {day18('input18', True)}")


if __name__ == '__main__':
    main()
