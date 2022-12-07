def day06(filepath, unique_length):
    with open(filepath) as fin:
        line = fin.readline()

    for i in range(len(line)):
        if len(set(line[i:i+unique_length])) == unique_length:
            return i + unique_length


def main():
    assert day06('test06', 4) == 7
    print(day06('input06', 4))

    assert day06('test06', 14) == 19
    print(day06('input06', 14))


if __name__ == '__main__':
    main()
