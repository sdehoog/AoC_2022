from time import time
from z3 import *


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


def monkey_eval(monkey_name, monkey_dict):
    monkey_yell = monkey_dict[monkey_name]
    if isinstance(monkey_yell, int):
        return monkey_yell
    else:
        if monkey_yell[1] == '/':
            return monkey_eval(monkey_yell[0], monkey_dict) / monkey_eval(monkey_yell[2], monkey_dict)
        if monkey_yell[1] == '+':
            return monkey_eval(monkey_yell[0], monkey_dict) + monkey_eval(monkey_yell[2], monkey_dict)
        if monkey_yell[1] == '-':
            return monkey_eval(monkey_yell[0], monkey_dict) - monkey_eval(monkey_yell[2], monkey_dict)
        if monkey_yell[1] == '*':
            return monkey_eval(monkey_yell[0], monkey_dict) * monkey_eval(monkey_yell[2], monkey_dict)
        if monkey_yell[1] == '=':
            return monkey_eval(monkey_yell[0], monkey_dict) == monkey_eval(monkey_yell[2], monkey_dict)


@timer_func
def day21(filepath, part2=False):
    with open(filepath) as fin:
        lines = fin.readlines()

    monkey_dict = {}
    for line in lines:
        monkey_name, monkey_yell = [x.strip() for x in line.split(':')]
        monkey_yell = [x for x in monkey_yell.split()]
        if len(monkey_yell) == 1:
            monkey_yell = int(monkey_yell[0])
        monkey_dict[monkey_name] = monkey_yell

    if not part2:
        return int(monkey_eval('root', monkey_dict))
    else:
        vals = {}
        s = Solver()
        for key in monkey_dict.keys():
            vals[key] = Real(key)
        for key, val in monkey_dict.items():
            if key == 'humn':
                # s.add(vals['humn'] < 3910938071093)
                continue
            elif key == 'root':
                s.add(vals[val[0]] == vals[val[2]])
            else:
                if isinstance(val, int):
                    s.add(vals[key] == val)
                else:
                    a, m, b = val
                    if m == '+':
                        s.add(vals[key] == (vals[a] + vals[b]))
                    elif m == '-':
                        s.add(vals[key] == (vals[a] - vals[b]))
                    elif m == '*':
                        s.add(vals[key] == (vals[a] * vals[b]))
                    elif m == '/':
                        s.add(vals[key] == (vals[a] / vals[b]))

        s.check()
        m = s.model()
        monkey_dict['humn'] = m[vals['humn']].as_long()
        monkey_dict['root'][1] = '='
        print(monkey_eval('root', monkey_dict))
        return m[vals['humn']]


def main():
    assert day21('test21') == 152
    print(f"Part 1: {day21('input21')}")

    assert day21('test21', True) == 301
    print(f"Part 2: {day21('input21', True)}")
    # print(f"Other test: {day21('othertest', True)}")


if __name__ == '__main__':
    main()
