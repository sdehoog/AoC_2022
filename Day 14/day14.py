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
        lines = [line.strip() for line in fin.readlines()]

    rocks = []
    for line in lines:
        for a, b in zip(line.split(' -> '), line.split(' -> ')[1:]):
            a = tuple(int(x) for x in a.split(','))
            b = tuple(int(x) for x in b.split(','))
            direction = tuple_direction(a, b)
            while a != b:
                rocks.append(a)
                a = tuple_add(a, direction)
            rocks.append(b)
    sand = []
    start = (500, 0)
    max_y = max([x for _, x in rocks])
    cave_floor = max_y + 2

    objects = {}
    for x, y in rocks:
        if x in objects:
            objects[x].append(y)
        else:
            objects[x] = [cave_floor]
            objects[x].append(y)

    caught = True
    while caught:
        falling = True
        cur = start
        while falling:
            step = tuple_add(cur, (0, 1))
            if step in rocks + sand:
                step = tuple_add(cur, (-1, 1))
                if step in rocks + sand:
                    step = tuple_add(cur, (1, 1))
                    if step in rocks + sand:
                        falling = False
                        sand.append(cur)
                        break
            cur = step
            if cur[1] >= max_y:
                caught = False
                break

    return len(sand)


def main():
    assert day14('test14') == 24
    print(f"Part 1: {day14('input14')}")

    assert day14('test14', True) == 93
    print(f"Part 2: {day14('input14', True)}")


if __name__ == '__main__':
    main()
