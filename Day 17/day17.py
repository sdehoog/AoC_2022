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


class Rock:
    def __init__(self, rock_type, height=0):
        self.rock_type = rock_type
        self.points = []
        self.generate_points(height)

    def generate_points(self, height):
        height = int(height)
        if self.rock_type == '-':
            for j in [-1j, 0, 1j, 2j]:
                self.points.append(height + j)
        elif self.rock_type == '+':
            for i in range(height, height + 3):
                self.points.append(i)
            for j in [-1j, 1j]:
                self.points.append(height + 1 + j)
        elif self.rock_type == 'l':
            for i in [-1j, 0, 1j]:
                self.points.append(height + i)
                if i == 1j:
                    for j in [1, 2]:
                        self.points.append(height + j + i)
        elif self.rock_type == '|':
            for i in range(height, height + 4):
                self.points.append(i - 1j)
        elif self.rock_type == 's':
            for i in [-1j, 0]:
                for j in [height, height + 1]:
                    self.points.append(i + j)
        elif self.rock_type == 'floor':
            self.points = [-2j, -1j, 0, 1j, 2j]

    def at_left_wall(self):
        for point in self.points:
            if point.imag == -3:
                return True
        return False

    def at_right_wall(self):
        for point in self.points:
            if point.imag == 3:
                return True
        return False

    def move_down(self):
        self.points = [point - 1 for point in self.points]

    def move_left(self):
        if not self.at_left_wall():
            self.points = [point - 1j for point in self.points]

    def move_right(self):
        if not self.at_right_wall():
            self.points = [point + 1j for point in self.points]

    def top(self):
        return max([point.real for point in self.points])


class RockGame:
    def __init__(self, jet_pattern):
        self.max_height = None
        self.rocks = None
        self.jet_counter = None
        self.rock_counter = None
        self.jet_pattern = jet_pattern
        self.jet_pattern_len = len(jet_pattern)
        self.rock_types = ['-', '+', 'l', '|', 's']
        self.rock_pattern_len = len(self.rock_types)
        self.tower = set()

    def run(self, rock_limit):
        self.max_height = 0
        self.jet_counter = 0
        self.rock_counter = 0
        self.rocks = [Rock('floor')]
        self.tower.clear()
        for i in range(rock_limit):
            self.rocks.append(Rock(self.rock_types[i % self.rock_pattern_len], self.max_height + 4))
            cur_down_moves = 0
            while True:
                jet_move = self.jet_pattern[self.jet_counter % self.jet_pattern_len]
                self.jet_counter += 1
                if jet_move == '<':
                    if self.can_move_left(self.rocks[-1]):
                        self.rocks[-1].move_left()
                elif jet_move == '>':
                    if self.can_move_right(self.rocks[-1]):
                        self.rocks[-1].move_right()
                if cur_down_moves < 3:
                    self.rocks[-1].move_down()
                    cur_down_moves += 1
                    continue
                else:
                    if self.can_move_down(self.rocks[-1]):
                        self.rocks[-1].move_down()
                    else:
                        self.max_height = max(self.max_height, self.rocks[-1].top())
                        for point in self.rocks[-1].points:
                            self.tower.add(point)
                        break

    def can_move_right(self, rock: Rock):
        for point in rock.points:
            if point.imag == 3:
                return False
        for point in [point + 1j for point in rock.points]:
            if point in self.tower:
                return False
        return True

    def can_move_left(self, rock: Rock):
        for point in rock.points:
            if point.imag == -3:
                return False
        for point in [point - 1j for point in rock.points]:
            if point in self.tower:
                return False
        return True

    def can_move_down(self, rock: Rock):
        for point in [point - 1 for point in rock.points]:
            if point.real <= 0:
                return False
            if point in self.tower:
                return False
        return True


@timer_func
def day17(filepath, part2=False):
    with open(filepath) as fin:
        line = fin.read().strip()

    rock_game = RockGame(line)
    rock_game.run(2022)

    return int(rock_game.max_height)


def main():
    assert day17('test17') == 3068
    print(f"Part 1: {day17('input17')}")

    assert day17('test17', True) == 1
    print(f"Part 2: {day17('input17', True)}")


if __name__ == '__main__':
    main()
