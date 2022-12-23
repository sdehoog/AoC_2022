from time import time
import re

D = {0: 1, 1: 1j, 2: -1, 3: -1j}
T = {'R': 1, 'L': -1, 'X': 0}


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


@timer_func
def day22(filepath, test, part2=False):
    with open(filepath) as fin:
        board_map, instructions = fin.read().split('\n\n')
    path = re.findall(r'(\d+)([LRX])', instructions)
    b_map = {}
    for y, line in enumerate(board_map.split('\n')):
        for x, c in enumerate(line):
            if c in '.#':
                b_map[complex(x, y)] = c
    cp = 0
    f = 0  # facing
    if test:
        cp = 8  # current point
        for steps, turn in path:
            for _ in range(int(steps)):
                ns = cp + D[f]  # next step
                if ns in b_map:
                    if b_map[ns] == '.':
                        cp = ns
                    elif b_map[ns] == '#':
                        f = (f + T[turn]) % 4
                        break
                else:
                    if f == 0:
                        if 0 <= cp.imag < 4:
                            ns = complex(8, cp.imag)
                        elif 4 <= cp.imag < 8:
                            ns = complex(0, cp.imag)
                        elif 8 <= cp.imag < 12:
                            ns = complex(0, cp.imag)
                    elif f == 1:
                        if 0 <= cp.real < 8:
                            ns = complex(cp.real, 4)
                        elif 8 <= cp.real < 12:
                            ns = complex(cp.real, 0)
                        elif 12 <= cp.real < 16:
                            ns = complex(cp.real, 8)
                    elif f == 2:
                        if 0 <= cp.imag < 8:
                            ns = complex(11, cp.imag)
                        elif 8 <= cp.imag < 12:
                            ns = complex(15, cp.imag)
                    elif f == 3:
                        if 0 <= cp.real < 8:
                            ns = complex(cp.real, 7)
                        elif 8 <= cp.real < 16:
                            ns = complex(cp.real, 11)
                    if b_map[ns] == '.':
                        cp = ns
                    elif b_map[ns] == '#':
                        f = (f + T[turn]) % 4
                        break
            else:
                f = (f + T[turn]) % 4

    else:
        cp = 8  # current point
        for steps, turn in path:
            for _ in range(int(steps)):
                ns = cp + D[f]  # next step
                if ns in b_map:
                    if b_map[ns] == '.':
                        cp = ns
                    elif b_map[ns] == '#':
                        f = (f + T[turn]) % 4
                        break
                else:
                    if f == 0:
                        if 0 <= cp.imag < 100:
                            ns = complex(50, cp.imag)
                        elif 100 <= cp.imag < 200:
                            ns = complex(0, cp.imag)
                    elif f == 1:
                        if 0 <= cp.real < 50:
                            ns = complex(cp.real, 100)
                        elif 50 <= cp.real < 150:
                            ns = complex(cp.real, 0)
                    elif f == 2:
                        if 0 <= cp.imag < 50:
                            ns = complex(149, cp.imag)
                        elif 50 <= cp.imag < 150:
                            ns = complex(99, cp.imag)
                        elif 150 <= cp.imag < 200:
                            ns = complex(49, cp.imag)
                    elif f == 3:
                        if 0 <= cp.real < 50:
                            ns = complex(cp.real, 199)
                        elif 50 <= cp.real < 100:
                            ns = complex(cp.real, 149)
                        elif 100 <= cp.real < 149:
                            ns = complex(cp.real, 49)
                    if b_map[ns] == '.':
                        cp = ns
                    elif b_map[ns] == '#':
                        f = (f + T[turn]) % 4
                        break
            else:
                f = (f + T[turn]) % 4

    password = int(1000 * (cp.imag + 1) + 4 * (cp.real + 1) + f)
    return password


def main():
    assert day22('test22', test=True) == 6032
    print(f"Part 1: {day22('input22', test=False)}")

    # assert day22('test22', test=True, part2=True) == 1
    # print(f"Part 2: {day22('input22', test=False, part2=True)}")


if __name__ == '__main__':
    main()
