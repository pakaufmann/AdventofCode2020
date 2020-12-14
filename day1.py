sum_to_find = 2020

with open("inputs/day1.txt", "r") as f:
    numbers = [int(line) for line in f]


def day1_part1():
    first, second = find_total(numbers, sum_to_find)
    print(first * second)


def day1_part2():
    first = next(x for x in numbers if find_total(numbers, sum_to_find - x) is not None)
    second, third = find_total(numbers, sum_to_find - first)
    print(first * second * third)


def find_total(numbers: list[int], total: int):
    first = next((n for n in numbers if (total - n) in numbers), None)

    if first is not None:
        second = total - first
        return first, second
    else:
        return None
