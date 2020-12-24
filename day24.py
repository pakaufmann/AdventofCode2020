import itertools


def parse_instructions(line):
    instructions = []
    last = ""

    for c in line:
        if c == "s" or c == "n":
            last = c
        else:
            instructions.append(last + c)
            last = ""

    return instructions


with open("inputs/day24.txt", "r") as f:
    all_instructions = [parse_instructions(line.replace("\n", "")) for line in f]


def run_instructions(instructions: list[str]):
    hexagon = [0, 0, 0]

    for instruction in instructions:
        if instruction == "e":
            hexagon[0] += 1
            hexagon[2] -= 1
        elif instruction == "se":
            hexagon[1] += 1
            hexagon[2] -= 1
        elif instruction == "sw":
            hexagon[0] -= 1
            hexagon[1] += 1
        elif instruction == "w":
            hexagon[0] -= 1
            hexagon[2] += 1
        elif instruction == "nw":
            hexagon[1] -= 1
            hexagon[2] += 1
        elif instruction == "ne":
            hexagon[0] += 1
            hexagon[1] -= 1
        else:
            raise Exception("invalid instruction: ", instruction)

    return tuple(hexagon)


def day24_part1():
    print(len(initial_layout()))


def initial_layout():
    flipped_hexagons = set()
    for instructions in all_instructions:
        hexagon = run_instructions(instructions)

        if hexagon in flipped_hexagons:
            flipped_hexagons.remove(hexagon)
        else:
            flipped_hexagons.add(hexagon)

    return flipped_hexagons


def neighbours(hexagon):
    return [
        (hexagon[0] + 1, hexagon[1] - 1, hexagon[2]),
        (hexagon[0] + 1, hexagon[1], hexagon[2] - 1),
        (hexagon[0], hexagon[1] + 1, hexagon[2] - 1),
        (hexagon[0] - 1, hexagon[1] + 1, hexagon[2]),
        (hexagon[0] - 1, hexagon[1], hexagon[2] + 1),
        (hexagon[0], hexagon[1] - 1, hexagon[2] + 1)
    ]


def run_days(initial):
    current_black_tiles = initial

    while True:
        new_black = set()
        touched: dict[tuple, int] = {}

        for hexagon in current_black_tiles:
            black_neighbours = 0

            for neighbour in neighbours(hexagon):
                touched[neighbour] = touched.get(neighbour, 0) + 1
                if neighbour in current_black_tiles:
                    black_neighbours += 1

            if black_neighbours == 1 or black_neighbours == 2:
                new_black.add(hexagon)

        current_black_tiles = new_black | set(c for c, times in touched.items() if times == 2)
        yield current_black_tiles


def day24_part2():
    current_black_tiles = initial_layout()

    print(len(next((itertools.islice(run_days(current_black_tiles), 99, None)))))
