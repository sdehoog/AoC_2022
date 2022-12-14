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
                self.objects[x].add(y)
            else:
                self.objects[x] = {self.floor}
                self.objects[x].add(y)

    def is_in(self, coord):
        x, y = coord
        if y == self.floor:
            return True
        if x in self.objects:
            if y in self.objects[x]:
                return True

        return False

    def fall(self, coord):
        x, y = coord
        if x in self.objects:
            next_highest = self.floor
            for val in self.objects[x]:
                if y < val < next_highest:
                    next_highest = val
            return x, next_highest
        else:
            return x, self.floor


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

    rocks = set()
    for line in lines:
        for a, b in zip(line.split(' -> '), line.split(' -> ')[1:]):
            a = tuple(int(x) for x in a.split(','))
            b = tuple(int(x) for x in b.split(','))
            direction = tuple_direction(a, b)
            while a != b:
                rocks.add(a)
                a = tuple_add(a, direction)
            rocks.add(b)
    sand = set()
    start = (500, 0)
    max_y = max([x for _, x in rocks])
    cave_floor = max_y + 2
    cave_objects = CaveObjects(cave_floor)
    for rock in rocks:
        cave_objects.add_object(rock)

    # dropping from the top everytime
    # caught = True
    # while caught:
    #     falling = True
    #     cur = start
    #     while falling:
    #         step = tuple_add(cur, (0, 1))
    #         if step[1] == cave_floor:
    #             sand.add(cur)
    #             rocks.add(cur)
    #             break
    #         if step in sand or step in rocks:
    #             step = tuple_add(cur, (-1, 1))
    #             if step in sand or step in rocks:
    #                 step = tuple_add(cur, (1, 1))
    #                 if step in sand or step in rocks:
    #                     falling = False
    #                     sand.add(cur)
    #                     rocks.add(cur)
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

    #   DFS
    path = [(500, -1)]
    more_sand = True
    while more_sand:
        cur = path[-1]
        for step in [(0, 1), (-1, 1), (1, 1)]:
            next_loc = tuple_add(cur, step)
            if not part2:
                if next_loc[1] == max_y + 1:
                    more_sand = False
                    break
            if cave_objects.is_in(next_loc):
                continue

            path.append(next_loc)
            break
        else:
            sand.add(cur)
            cave_objects.add_object(cur)
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
