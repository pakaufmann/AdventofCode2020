import functools
import itertools

file = "inputs/day6.txt"


class Group:
    def __init__(self):
        self.people: list[list[str]] = []

    def add_person(self, person: str):
        self.people.append(list(person))

    def number_anyone_answered(self) -> int:
        return len(set(itertools.chain(*self.people)))

    def number_all_answered(self) -> int:
        return len(set(self.people[0]).intersection(*self.people))


with open(file, "r") as f:
    current_group = Group()
    groups = []

    for line in f:
        if line == "\n":
            groups.append(current_group)
            current_group = Group()
        else:
            current_group.add_person(line.replace("\n", ""))

    groups.append(current_group)


def day6_part1():
    print(functools.reduce(lambda a, b: a + b.number_anyone_answered(), groups, 0))


def day6_part2():
    print(functools.reduce(lambda a, b: a + b.number_all_answered(), groups, 0))
