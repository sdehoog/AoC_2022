from time import time
from json import loads


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


def insertion_sort(A):
    for k in range(1, len(A)):
        cur = A[k]
        j = k
        while j > 0 and compare_packet(cur, A[j-1]):
            A[j] = A[j-1]
            j -= 1
            A[j] = cur


def compare_packet(left: list, right: list):
    for left_val, right_val in zip(left, right):
        if isinstance(left_val, int) and isinstance(right_val, int):
            if left_val < right_val:
                return True
            elif left_val > right_val:
                return False
            else:
                continue
        else:
            if isinstance(left_val, int):
                left_val = [left_val]
            elif isinstance(right_val, int):
                right_val = [right_val]
            temp = compare_packet(left_val, right_val)
            if temp is None:
                continue
            else:
                return temp
    if len(left) < len(right):
        return True
    elif len(left) > len(right):
        return False
    return None


@timer_func
def day13(filepath, sort=False):
    with open(filepath) as fin:
        packet_pairs = fin.read().split('\n\n')

    if not sort:
        correct_packets = []
        for i, pair in enumerate(packet_pairs):
            left_p, right_p = pair.split('\n')
            if compare_packet(loads(left_p), loads(right_p)):
                correct_packets.append(i)
        return sum(correct_packets) + len(correct_packets)

    else:
        packets = [loads(packet) for pair in packet_pairs for packet in pair.split('\n')] + [[[2]], [[6]]]
        insertion_sort(packets)
        return (packets.index([[2]]) + 1) * (packets.index([[6]]) + 1)


def main():
    assert day13('test13') == 13
    print(f"Part 1: {day13('input13')}")

    assert day13('test13', True) == 140
    print(f"Part 2: {day13('input13', True)}")


if __name__ == '__main__':
    main()
