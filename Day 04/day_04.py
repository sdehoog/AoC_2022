def section_compare(filepath, any_overlap=False):
    with open(filepath) as fin:
        lines = fin.readlines()
        elves = [line.strip().split(',') for line in lines]
        elf_sets = [[set(range(int(a.split('-')[0]), int(a.split('-')[1]) + 1)), set(range(int(b.split('-')[0]), int(b.split('-')[1]) + 1))] for a, b in elves]

        contain_count = 0
        if not any_overlap:
            for ea, eb in elf_sets:
                ec = ea & eb
                if ec == ea or ec == eb:
                    contain_count += 1
        else:
            for ea, eb in elf_sets:
                if ea & eb:
                    contain_count += 1

    return contain_count


def main():
    assert section_compare('test.txt') == 2
    print(section_compare('input.txt'))

    assert section_compare('test.txt', True) == 4
    print(section_compare('input.txt', True))


if __name__ == '__main__':
    main()
