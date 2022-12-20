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


def find_air(current_point: tuple, air_points: set, rock_points, surface_area: int, valid_range):
    air_points.add(current_point)
    for point in get_adjacent(current_point):
        if ((valid_range[0][0] <= point[0] <= valid_range[0][1] and
             valid_range[1][0] <= point[1] <= valid_range[1][1]) and
                valid_range[2][0] <= point[2] <= valid_range[2][1]):
            pass
        else:
            continue
        if point in rock_points:
            surface_area += 1
        elif ((valid_range[0][0] > point[0] > valid_range[0][1] or
              valid_range[1][0] > point[1] > valid_range[1][1]) or
              valid_range[2][0] > point[2] > valid_range[2][1]):
            continue
        elif point in air_points:
            continue
        else:
            air_points, surface_area = find_air(point, air_points, rock_points, surface_area, valid_range)

    return air_points, surface_area


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
        valid_range = [[min(point[0] for point in rock_points) - 1, max(point[0] for point in rock_points) + 1],
                       [min(point[1] for point in rock_points) - 1, max(point[1] for point in rock_points) + 1],
                       [min(point[2] for point in rock_points) - 1, max(point[2] for point in rock_points) + 1]]
        sys.setrecursionlimit(max(1000, prod(x[1] for x in valid_range)))
        _, surface_area = find_air(tuple(x[0] for x in valid_range), set(), rock_points, 0, valid_range)

    return surface_area


def main():
    assert day18('test18') == 64
    print(f"Part 1: {day18('input18')}")

    assert day18('test18', True) == 58
    print(f"Part 2: {day18('input18', True)}")


if __name__ == '__main__':
    main()
