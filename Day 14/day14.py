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


class CaveObjects:
    def __init__(self, floor):
        self.objects = {}
        self.floor = floor

    def add_object(self, coord):
        x, y = coord
        if not self.is_in(coord):
            if x in self.objects:
                self.objects[x].append(y)
            else:
                self.objects[x] = [self.floor]
                self.objects[x].append(y)

    def is_in(self, coord):
        x, y = coord
        if y == self.floor:
            return True
        if x in self.objects:
            if y in self.objects[x]:
                return True

        return False


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
    cave_objects = CaveObjects(cave_floor)
    for rock in rocks:
        cave_objects.add_object(rock)

    # caught = True
    # while caught:
    #     falling = True
    #     cur = start
    #     while falling:
    #         step = tuple_add(cur, (0, 1))
    #         if cave_objects.is_in(step):
    #             step = tuple_add(cur, (-1, 1))
    #             if cave_objects.is_in(step):
    #                 step = tuple_add(cur, (1, 1))
    #                 if cave_objects.is_in(step):
    #                     falling = False
    #                     sand.append(cur)
    #                     cave_objects.add_object(cur)
    #                     break
    #         cur = step
    #         if not part2:
    #             if cur[1] >= max_y:
    #                 caught = False
    #                 break
    #     if (500, 0) in sand:
    #         falling = False
    #         caught = False
    #         break

    path = [(500, -1)]
    more_sand = True
    while more_sand:
        for step in [(0, 1), (-1, 1), (1, 1)]:
            next_loc = tuple_add(path[-1], step)
            if not part2:
                if next_loc[1] == cave_floor:
                    more_sand = False
                    break
            if cave_objects.is_in(next_loc):
                continue
            else:
                path.append(next_loc)
                break
        else:
            sand.append(path[-1])
            cave_objects.add_object(path[-1])
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
