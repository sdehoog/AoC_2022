elf_dict = {
    'A': 1,
    'B': 2,
    'C': 3,
}

me_dict = {
    'X': 1,
    'Y': 2,
    'Z': 3,
}

outcome_dict = {
    'X': 0,
    'Y': 3,
    'Z': 6,
}

outcome_delta = {
    'X': -1,
    'Y': 0,
    'Z': 1,
}


def score_game(elf_hand, me_hand):
    hand_diff = me_dict[me_hand] - elf_dict[elf_hand]
    if hand_diff == 0:
        return 3
    elif hand_diff == 1 or hand_diff == -2:
        return 6
    elif hand_diff == -1 or hand_diff == 2:
        return 0


def rps_score(file_path, outcome=False):
    with open(file_path) as fin:
        rounds = fin.read().strip().split('\n')

    score = 0
    if not outcome:
        for rps_round in rounds:
            elf, me = rps_round.split()
            score += me_dict[me]
            score += score_game(elf, me)

        return score
    else:
        shape_score = [1, 2, 3]
        for rps_round in rounds:
            elf, me = rps_round.split()
            score += outcome_dict[me]
            delta = outcome_delta[me]
            hand_score = shape_score[(elf_dict[elf] - 1 + delta) % 3]
            score += hand_score
        return score


def main():
    assert rps_score('test.txt') == 15
    print(rps_score('input.txt'))

    assert rps_score('test.txt', True) == 12
    print(rps_score('input.txt', True))


if __name__ == '__main__':
    main()
