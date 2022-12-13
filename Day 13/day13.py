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
    return A


def compare_packet(left: list, right: list):
    try:
        for i in range(len(left)):
            left_val = left[i]
            right_val = right[i]
            if isinstance(left_val, int) and isinstance(right_val, int):
                if left_val < right_val:
                    return True
                elif left_val > right_val:
                    return False
                else:
                    continue
            elif isinstance(left_val, list) and isinstance(right_val, int):
                if compare_packet(left_val, [right_val]) is None:
                    continue
                else:
                    return compare_packet(left_val, [right_val])
            elif isinstance(left_val, int) and isinstance(right_val, list):
                if compare_packet([left_val], right_val) is None:
                    continue
                else:
                    return compare_packet([left_val], right_val)
            else:
                if compare_packet(left_val, right_val) is None:
                    continue
                else:
                    return compare_packet(left_val, right_val)
        if len(left) < len(right):
            return True
        return None
    except IndexError:
        return False


@timer_func
def day13(filepath, sort=False):
    with open(filepath) as fin:
        packet_pairs = fin.read().split('\n\n')

    if not sort:
        correct_packets = []
        for i, pair in enumerate(packet_pairs):
            left_p, right_p = pair.split('\n')
            left_p = loads(left_p)
            right_p = loads(right_p)
            if compare_packet(left_p, right_p):
                correct_packets.append(i)

        return sum(correct_packets) + len(correct_packets)
    else:
        packets = [loads(packet) for pair in packet_pairs for packet in pair.split('\n')]
        packets.append([[2]])
        packets.append([[6]])
        packets_sorted = insertion_sort(packets)
        return (packets_sorted.index([[2]]) + 1) * (packets_sorted.index([[6]]) + 1)


def main():
    assert day13('test13') == 13
    print(day13('input13'))

    assert day13('test13', True) == 140
    print(day13('input13', True))


if __name__ == '__main__':
    main()