with open("inputs/day10.txt", "r") as f:
    inp = [int(line) for line in f]
    inp.append(0)
    numbers = sorted(inp)


def day10_part1():
    diff_one = (sum(1 for pair in windowed(numbers, 2) if pair[0] + 1 == pair[1]))
    diff_three = (sum(1 for pair in windowed(numbers, 2) if pair[0] + 3 == pair[1])) + 1
    print(diff_one * diff_three)


def day10_part2():
    full_matches = count_full_match(0, numbers[0], numbers[1:])
    print(full_matches)
    pass


already_found = {}


def count_full_match(last_joltage: int, next_joltage: int, rest: list[int]) -> int:
    if last_joltage + 3 < next_joltage:
        return 0

    key = tuple(rest)

    if key in already_found:
        return already_found[key]

    if len(rest) == 0:
        return 1

    result = sum((count_full_match(next_joltage, n, rest[i + 1:]) for i, n in enumerate(rest[:3])))
    already_found[key] = result

    return result


def windowed(to_window: list, size: int):
    return iter(sublist for sublist in (to_window[x:x + size] for x in range(len(to_window) - size + 1)))
