import itertools
import time
from functools import cache

Cube3D = tuple[int, int, int]
Cube4D = tuple[int, int, int, int]

starting_active_cubes: set[Cube3D] = set()
starting_active_cubes_4d: set[Cube4D] = set()

with open("inputs/day17.txt", "r") as f:
    for x, line in enumerate(f):
        for y, cube in enumerate(line):
            if cube == "#":
                starting_active_cubes.add((x, y, 0))
                starting_active_cubes_4d.add((x, y, 0, 0))


@cache
def generate_neighbours(cube, dimensions: int) -> set:
    all = set(tuple(sum(x) for x in zip(cube, delta)) for delta in itertools.product(range(-1, 2), repeat=dimensions))
    all.remove(cube)
    return all


def generate_all_to_check(active_cubes: set, dimension: int):
    all_to_check = active_cubes

    for cube in active_cubes:
        all_to_check = all_to_check | generate_neighbours(cube, dimension)

    return all_to_check


def run(active_cubes: set):
    dimensions: int = len(next(iter(active_cubes)))

    while True:
        new_active_cubes = set()
        touched: dict[tuple, int] = {}

        for active_cube in active_cubes:
            active = 0

            for neighbour in generate_neighbours(active_cube, dimensions):
                touched[neighbour] = touched.get(neighbour, 0) + 1
                if neighbour in active_cubes:
                    active += 1

            if active == 2 or active == 3:
                new_active_cubes.add(active_cube)

        active_cubes = new_active_cubes | set(c for c, times in touched.items() if times == 3)

        yield len(active_cubes)


def day17_part1():
    print(next(itertools.islice(run(starting_active_cubes), 6 - 1, None)))


def day17_part2():
    print(next(itertools.islice(run(starting_active_cubes_4d), 6 - 1, None)))
