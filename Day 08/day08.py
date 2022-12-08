import numpy as np


def day08(filepath, scenic_score=False):
    trees = np.genfromtxt(filepath, delimiter=1, dtype=int)
    if not scenic_score:
        visible_trees = sum(trees.shape) * 2 - 4
        for index, value in np.ndenumerate(trees):
            if index[0] == 0 or index[1] == 0 or index[0] == trees.shape[0]-1 or index[1] == trees.shape[1]-1:
                continue
            # up
            if trees[:index[0], index[1]].max() < value:
                visible_trees += 1
            # down
            elif trees[index[0]+1:, index[1]].max() < value:
                visible_trees += 1
            # left
            elif trees[index[0], :index[1]].max() < value:
                visible_trees += 1
            # right
            elif trees[index[0], index[1]+1:].max() < value:
                visible_trees += 1

        return visible_trees
    else:
        scenic_score = []
        for index, value in np.ndenumerate(trees):
            if index[0] == 0 or index[1] == 0 or index[0] == trees.shape[0]-1 or index[1] == trees.shape[1]-1:
                continue
            # up
            scenic_score.append(1)
            up_score = 0
            for sub_value in np.flip(trees[:index[0], index[1]]):
                if sub_value < value:
                    up_score += 1
                else:
                    up_score += 1
                    break
            # down
            down_score = 0
            for sub_value in trees[index[0]+1:, index[1]]:
                if sub_value < value:
                    down_score += 1
                else:
                    down_score += 1
                    break
            # left
            left_score = 0
            for sub_value in np.flip(trees[index[0], :index[1]]):
                if sub_value < value:
                    left_score += 1
                else:
                    left_score += 1
                    break
            # right
            right_score = 0
            for sub_value in trees[index[0], index[1]+1:]:
                if sub_value < value:
                    right_score += 1
                else:
                    right_score += 1
                    break

            scenic_score[-1] = up_score * down_score * left_score * right_score

        return max(scenic_score)


def main():
    assert day08('test08') == 21
    print(day08('input08'))

    assert day08('test08', True) == 8
    print(day08('input08', True))


if __name__ == '__main__':
    main()
