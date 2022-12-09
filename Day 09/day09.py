def adjacent(knot1, knot2):
    if abs(knot1.x - knot2.x) <= 1 and abs(knot1.y - knot2.y) <= 1:
        return True
    else:
        return False


class Rope:
    class Knot:
        def __init__(self, pos):
            self.x = pos[0]
            self.y = pos[1]
            self.history = [pos]

        def get_pos(self):
            return self.x, self.y

    def __init__(self, rope_length=2, start_pos=(0, 0)):
        self.knots = [self.Knot(start_pos) for i in range(rope_length)]
        self.head = self.knots[0]
        self.tail = self.knots[-1]
        self.rope_length = rope_length

    def move(self, direction):
        if direction == 'D':
            self.head.y -= 1
        elif direction == 'U':
            self.head.y += 1
        elif direction == 'R':
            self.head.x += 1
        elif direction == 'L':
            self.head.x -= 1
        self.head.history.append(self.head.get_pos())
        for i in range(1,self.rope_length):
            current_knot = self.knots[i]
            prior_knot = self.knots[i-1]
            if adjacent(current_knot, prior_knot):
                current_knot.history.append(current_knot.get_pos())
            else:
                if current_knot.x != prior_knot.x:
                    delta_x = prior_knot.x - current_knot.x
                    current_knot.x += delta_x//abs(delta_x)
                if current_knot.y != prior_knot.y:
                    delta_y = prior_knot.y - current_knot.y
                    current_knot.y += delta_y//abs(delta_y)
                current_knot.history.append(current_knot.get_pos())


def day09(filepath, length=2):
    with open(filepath) as fin:
        lines = [line.split() for line in fin.readlines()]

    rope = Rope(length)
    for line in lines:
        for i in range(int(line[1])):
            rope.move(line[0])

    return len(set(rope.tail.history))


def main():
    assert day09('test09') == 13
    print(day09('input09'))

    assert day09('test09_2', 10) == 36
    print(day09('input09', 10))


if __name__ == '__main__':
    main()
