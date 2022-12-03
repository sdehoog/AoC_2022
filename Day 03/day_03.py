def priority_score(ltr: str):
    if ltr.isupper():
        return ord(ltr) - 38
    else:
        return ord(ltr) - 96


def rucksack_inspection(filepath, group=False):
    with open(filepath) as fin:
        rucksacks = fin.readlines()

    score = 0
    if not group:
        for rucksack in rucksacks:
            for item in rucksack[:len(rucksack)//2]:
                if item in rucksack[len(rucksack)//2:]:
                    score += priority_score(item)
                    break
    else:
        for a, b, c in zip(*[iter(rucksacks)] * 3):
            for item in a:
                if item in b and item in c:
                    score += priority_score(item)
                    break

    return score


def main():
    assert rucksack_inspection('test.txt') == 157
    print(rucksack_inspection('input.txt'))

    assert rucksack_inspection('test.txt', True) == 70
    print(rucksack_inspection('input.txt', True))


if __name__ == '__main__':
    main()
