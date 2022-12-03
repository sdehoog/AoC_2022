import numpy as np


def elf_count(file_name, n):
    with open(file_name) as fin:
        elves = fin.read().strip().split('\n\n')
    for i, elf in enumerate(elves):
        elves[i] = elf.split('\n')
    # print(elves)
    totals = np.zeros(len(elves))
    for i, elf in enumerate(elves):
        elf_total = 0
        for item in elf:
            elf_total += int(item)
        totals[i] = elf_total
    ind = np.argpartition(totals, -n)
    top_n = totals[ind[-n:]]
    return top_n.sum()


def main():
    assert elf_count("test.txt", 1) == 24000
    print(elf_count("input.txt", 1))

    assert elf_count("test.txt", 3) == 45000
    print(elf_count("input.txt", 3))

    return


if __name__ == "__main__":
    main()
