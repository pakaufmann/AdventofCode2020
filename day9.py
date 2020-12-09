import itertools

file = "inputs/day9.txt"
preamble_length = 25

with open(file, "r") as f:
    numbers = [int(line) for line in f]


def is_valid_number(number: int, preamble: list[int]) -> bool:
    return any(number == combination[0] + combination[1] for combination in itertools.combinations(preamble, 2))


def find_first_invalid_number():
    preamble = numbers[:preamble_length]
    rest = numbers[preamble_length:]
    while is_valid_number(rest[0], preamble):
        preamble = preamble[1:]
        preamble.append(rest[0])
        rest = rest[1:]

    return rest[0]


def day9_part1():
    print(find_first_invalid_number())


def day9_part2():
    invalid_number = find_first_invalid_number()

    for size in range(2, len(numbers)):
        sub_lists = iter(sublist for sublist in (numbers[x:x + size] for x in range(len(numbers) - size + 1)))

        valid_list = next((sublist for sublist in sub_lists if sum(sublist) == invalid_number), None)
        if valid_list is not None:
            break

    print(min(valid_list) + max(valid_list))
