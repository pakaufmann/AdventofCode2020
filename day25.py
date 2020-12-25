import itertools

modulo = 20201227

with open("inputs/day25.txt", "r") as f:
    card_public_key = int(f.readline())
    door_public_key = int(f.readline())


def transform(subject_number: int = 7) -> tuple[int, int]:
    value = 1
    for i in itertools.count(1):
        value = (value * subject_number) % modulo
        yield value, i


def day25_part1():
    card_loop_size = next(loop_size for num, loop_size in transform() if num == card_public_key)
    print(next(itertools.islice(transform(door_public_key), card_loop_size - 1, None)))


def day25_part2():
    pass
