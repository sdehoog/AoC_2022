from time import time


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


def tuple_add(a, b):
    return tuple(c + d for c, d in zip(a, b))


def tuple_sub(a, b):
    return tuple(c - d for c, d in zip(a, b))


def tuple_direction(a, b):
    return tuple(x // abs(x) if abs(x) > 0 else 0 for x in tuple_sub(b, a))


@timer_func
def day14(filepath, part2=False):
    with open(filepath) as fin:
        lines = fin.readlines()

    rocks = set()
    for line in lines:
        for a, b in zip(line.split(' -> '), line.split(' -> ')[1:]):
            a = tuple([int(x) for x in a.split(',')])
            b = tuple([int(x) for x in b.split(',')])
            direction = tuple_direction(a, b)
            while a != b:
                rocks.add(a)
                a = tuple_add(a, direction)
            rocks.add(b)
    sand = set()
    cave_floor = int(max([x[1] for x in rocks])) + 2
    path = [(500, -1)]
    more_sand = True
    while more_sand:
        cur = path[-1]
        for step in [(0, 1), (-1, 1), (1, 1)]:
            next_loc = tuple_add(cur, step)
            if not part2:
                if next_loc[1] == cave_floor:
                    more_sand = False
                    break
            if next_loc in rocks or next_loc in sand or next_loc[1] == cave_floor:
                continue

            path.append(next_loc)
            break
        else:
            sand.add(cur)
            rocks.add(cur)
            path.pop()
        if (500, 0) in sand:
            break
    return len(sand)


def main():
    assert day14('test14') == 24
    print(f"Part 1: {day14('input14')}")

    assert day14('test14', True) == 93
    print(f"Part 2: {day14('input14', True)}")


if __name__ == '__main__':
    main()
