def day05(filepath, cratemover9001=False):
    with open(filepath) as fin:
        lines = fin.readlines()

    crates = []
    moves = []
    crate_id = ''

    for line in lines:
        if line[:4] == 'move':
            moves.append(line[5:])
        elif line[:6] == ' 1   2':
            crate_id = line
        elif line.isspace():
            pass
        else:
            crates.append(line)

    crate_array = []
    for letter in crates[-1]:
        if letter.isalpha():
            crate_array.append([letter])

    for line in crates[-2::-1]:
        for i, letter in enumerate(line):
            if letter.isalpha():
                stack = int(crate_id[i])
                crate_array[stack - 1].append(letter)

    for move in moves:
        number_crates = int(move.split(' from ')[0])
        stack_from = int(move.split(' from ')[1].split(' to ')[0])
        stack_to = int(move.split(' from ')[1].split(' to ')[1])
        if not cratemover9001:
            for i in range(number_crates):
                crate_array[stack_to - 1].append(crate_array[stack_from - 1].pop())
        else:
            crate_array[stack_to - 1].extend(crate_array[stack_from - 1][-number_crates:])
            for i in range(number_crates):
                crate_array[stack_from - 1].pop()

    top_crates = ''
    for stack in crate_array:
        top_crates = top_crates + stack[-1]

    return top_crates


def main():
    assert day05('test05') == 'CMZ'
    print(day05('input05'))

    assert day05('test05', True) == 'MCD'
    print(day05('input05', True))


if __name__ == '__main__':
    main()
