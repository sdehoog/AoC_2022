from time import time

c_dict = {
    2: "2",
    1: '1',
    0: '0',
    -1: '-',
    -2: '=',
}

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


def snafu_to_dec(snafu: str) -> int:
    if len(snafu) == 0 :
        return 0
    d = 0
    for i, c in enumerate(snafu[::-1]):
        if c == '-':
            d += -1 * (5 ** i)
        elif c == '=':
            d += -2 * (5 ** i)
        else:
            d += int(c) * (5 ** i)
    return d


def dec_to_snafu(dec: int) -> str:
    i = 0
    snafu = ''
    while True:
        max_range = 2 * (5 ** i)
        for j in range(i):
            max_range += 2 * (5 ** j)
        if max_range >= dec:
            break
        i += 1
    other_center = 0
    for n in range(i, -1, -1):
        other_max = sum([2 * (5 ** j) for j in range(n)])
        for c in c_dict.keys():
            center = c * (5 ** n) + other_center
            if n != 0:
                if center - other_max < dec <= center + other_max:
                    snafu += c_dict[c]
                    other_center = center
                    break
            else:
                if center + other_max == dec:
                    snafu += c_dict[c]
                    break

    return snafu


@timer_func
def day25(filepath, part2=False):
    with open(filepath) as fin:
        lines = [line.strip() for line in fin.readlines()]

    decs = [snafu_to_dec(x) for x in lines]
    snafus = [dec_to_snafu(x) for x in decs]
    for a, b, c in zip(decs, snafus, lines):
        print(a, b, c)
    dec_sum = sum(decs)
    snafu_sum = dec_to_snafu(dec_sum)
    return snafu_sum


def main():
    assert day25('test25') == '2=-1=0'
    print(f"Part 1: {day25('input25')}")

    # assert day25('test25', True) == 1
    # print(f"Part 2: {day25('input25', True)}")


if __name__ == '__main__':
    main()
