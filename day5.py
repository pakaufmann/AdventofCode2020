import functools

file = "inputs/day5.txt"


def get_seat_id(input: str):
    row, seat = get_seat(input)

    return row * 8 + seat


def get_seat(input: str):
    # row = functools.reduce(lambda a, b: get_range(a[0], a[1], b == "F"), input[:7], (0, 127))
    # seat = functools.reduce(lambda a, b: get_range(a[0], a[1], b == "L"), input[-3:], (0, 7))
    # return row[0], seat[0]

    row = int(input[:7].replace("F", "0").replace("B", "1"), 2)
    seat = int(input[-3:].replace("L", "0").replace("R", "1"), 2)

    return row, seat


def get_range(lower: int, upper: int, take_lower: bool):
    middle = int((lower + upper) / 2)
    if take_lower:
        return lower, middle
    else:
        return middle + 1, upper


with open(file, "r") as f:
    seat_ids = sorted([get_seat_id(line.replace("\n", "")) for line in f])


def day5_part1():
    print(seat_ids[-1])


def day5_part2():
    for i, seat in enumerate(seat_ids):
        if seat_ids[i + 1] == seat + 2:
            print(seat + 1)
            break
