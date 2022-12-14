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


def complex_sign(num):
    real = num.real
    imag = num.imag
    if real != 0:
        real = real // abs(real)
    if imag != 0:
        imag = imag // abs(imag)
    return complex(real, imag)

@timer_func
def day14(filepath, part2=False):
    with open(filepath) as fin:
        lines = fin.readlines()

    rocks = set()
    for line in lines:
        for a, b in zip(line.split(' -> '), line.split(' -> ')[1:]):
            a = complex(*[int(x) for x in a.split(',')])
            b = complex(*[int(x) for x in b.split(',')])
            direction = complex_sign(b - a)
            while a != b:
                rocks.add(a)
                a += direction
            rocks.add(b)
    sand = set()
    cave_floor = int(max([x.imag for x in rocks])) + 2
    path = [500-1j]
    more_sand = True
    while more_sand:
        cur = path[-1]
        for step in [0+1j, -1+1j, 1+1j]:
            next_loc = cur + step
            if not part2:
                if next_loc.imag == cave_floor:
                    more_sand = False
                    break
            if next_loc in rocks or next_loc in sand or next_loc.imag == cave_floor:
                continue

            path.append(next_loc)
            break
        else:
            sand.add(cur)
            rocks.add(cur)
            path.pop()
        if 500+0j in sand:
            break
    return len(sand)


def main():
    assert day14('test14') == 24
    print(f"Part 1: {day14('input14')}")

    assert day14('test14', True) == 93
    print(f"Part 2: {day14('input14', True)}")


if __name__ == '__main__':
    main()
