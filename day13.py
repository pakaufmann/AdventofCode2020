import itertools
from math import ceil

with open("inputs/day13.txt", "r") as f:
    lines = f.readlines()
    earliest = int(lines[0])
    buses = [int(bus) for bus in lines[1].split(",") if bus != "x"]

    schedules: list[tuple[int, int]] = []
    delay = 0

    for bus in lines[1].split(","):
        if bus != "x":
            schedules.append((int(bus), delay))
        delay += 1


def day13_part1():
    next_departure = [(ceil(earliest / bus) * bus, bus) for bus in buses]
    next_bus = min(next_departure, key=lambda x: x[0])
    diff = next_bus[0] - earliest

    print(diff * next_bus[1])


def day13_part2():
    step = 1
    n = 0

    for bus, offset in schedules:
        n = next(time for time in itertools.count(n, step) if (time + offset) % bus == 0)
        step *= bus

    print(n)
