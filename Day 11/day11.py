from time import time
from math import prod


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


class Monkey:
    def __init__(self, monkey_start):
        self.inspection_count = 0
        lines = [line.strip() for line in monkey_start.split('\n')]
        self.items = [int(val.strip()) for val in lines[1].split(':')[1].split(',')]
        self.operation = lines[2].split('=')[-1]
        self.test_divisor = int(lines[3].split()[-1])
        self.monkey_true = int(lines[4].split()[-1])
        self.monkey_false = int(lines[5].split()[-1])
        self.thrown_items = []

    def inspect_items(self, worry_lower):
        self.thrown_items.clear()
        for old in self.items:
            self.inspection_count += 1
            new = eval(self.operation)
            if worry_lower != 1:
                new = new // worry_lower
            if new % self.test_divisor == 0:
                self.thrown_items.append([self.monkey_true, new])
            else:
                self.thrown_items.append([self.monkey_false, new])
        self.items.clear()

    def catch_item(self, item):
        self.items.append(item)


class MonkeyRing:
    def __init__(self, monkeys, worry_lower):
        self.monkeys = []
        self.worry_lower = worry_lower
        for monkey in monkeys:
            self.monkeys.append(Monkey(monkey))
        self.mod_factor = prod([monkey.test_divisor for monkey in self.monkeys])

    def throw_items(self, monkey):
        for monkey_ID, item in monkey.thrown_items:
            self.monkeys[monkey_ID].catch_item(item % self.mod_factor)

    def do_a_round(self):
        for monkey in self.monkeys:
            monkey.inspect_items(self.worry_lower)
            self.throw_items(monkey)

    def monkey_business_level(self):
        monkey_activity = [monkey.inspection_count for monkey in self.monkeys]
        monkey_activity.sort()
        return monkey_activity[-1] * monkey_activity[-2]


@timer_func
def day11(filepath, rounds=20, worry_lower=3):
    with open(filepath) as fin:
        monkeys = fin.read().split('\n\n')

    monkeyring = MonkeyRing(monkeys, worry_lower)

    for _ in range(rounds):
        monkeyring.do_a_round()

    return monkeyring.monkey_business_level()


def main():
    assert day11('test11') == 10605
    print(day11('input11'))

    assert day11('test11', 10000, 1) == 2713310158
    print(day11('input11', 10000, 1))


if __name__ == '__main__':
    main()
