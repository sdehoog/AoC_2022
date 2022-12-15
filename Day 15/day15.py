from time import time
from itertools import combinations
import re


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


def man_dist(a: complex, b: complex = 0):
    return int(sum([abs(a.real - b.real), abs(a.imag - b.imag)]))


def valid_pos(x, y, max_x, max_y):
    return 0 <= x <= max_x and 0 <= y <= max_y


@timer_func
def day15(filepath, inspect_row, part2=False):
    with open(filepath) as fin:
        lines = fin.read()

    coord_re = re.compile(r'x=(-?\d+), y=(-?\d+)')
    matches = coord_re.findall(lines)
    sensor_sets = []
    for sensor, beacon in zip(matches[::2], matches[1::2]):
        sensor_sets.append([complex(*[int(x) for x in sensor]), complex(*[int(x) for x in beacon])])

    for s_set in sensor_sets:
        sensor, beacon = s_set
        distance = man_dist(sensor, beacon)
        s_set.append(distance)

    set_of_sensors = set([s for s, b, d in sensor_sets])
    set_of_beacons = set([b for s, b, d in sensor_sets])
    if not part2:
        not_beacon = set()

        for s, b, d in sensor_sets:
            if s.imag - d <= inspect_row <= s.imag + d:
                not_beacon.add(complex(s.real, inspect_row))
                for i in range(abs(int(abs(inspect_row - s.imag) - d))):
                    not_beacon.add(complex(s.real + (i + 1), inspect_row))
                    not_beacon.add(complex(s.real - (i + 1), inspect_row))

        return len(not_beacon) - len(not_beacon.intersection(set_of_beacons))
    else:
        for sen in sensor_sets:
            s, _, d = sen
            d1 = set()
            for dn in range(-(d + 1), d + 2):
                for f in [-1, 1]:
                    step = complex(f * abs(d + 1 - dn), dn)
                    nd1 = step + s
                    if 0 <= nd1.real <= inspect_row * 2 and 0 <= nd1.imag <= inspect_row * 2:
                        d1.add(nd1)
            sen.append(d1)

        possible_points = set()
        for a, b in combinations(sensor_sets, 2):
            sa, _, _, d1a = a
            sb, _, _, d1b = b
            possible_points.update(d1a.intersection(d1b))
        test = 0
        for p in possible_points:
            for s, _, d, _ in sensor_sets:
                if man_dist(p, s) <= d:
                    break
            else:
                return int(4000000 * p.real + p.imag)


def main():
    assert day15('test15', 10) == 26
    print(f"Part 1: {day15('input15', 2000000)}")

    assert day15('test15', 10, True) == 56000011
    print(f"Part 2: {day15('input15', 2000000, True)}")


if __name__ == '__main__':
    main()
