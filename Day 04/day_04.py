def section_compare(filepath, any_overlap=False):
    with open(filepath) as fin:
        lines = fin.readlines()
        elves = [line.strip().split(',') for line in lines]
        elf_sets = [[set(range(int(a.split('-')[0]), int(a.split('-')[1]) + 1)), set(range(int(b.split('-')[0]), int(b.split('-')[1]) + 1))] for a, b in elves]

        contain_count = 0
        if not any_overlap:
            for ea, eb in elf_sets:
                len_a = len(ea)
                len_b = len(eb)
                len_c = len(ea & eb)
                if len_c == len_a or len_c == len_b:
                    contain_count += 1
        else:
            for ea, eb in elf_sets:
                if len(ea & eb):
                    contain_count += 1

    return contain_count


def main():
    assert section_compare('test.txt') == 2
    print(section_compare('input.txt'))

    assert section_compare('test.txt', True) == 4
    print(section_compare('input.txt', True))


if __name__ == '__main__':
    main()
