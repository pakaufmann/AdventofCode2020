import math


def read_trees(line: str):
    return set([i for i in range(len(line)) if line[i] == "#"])


file = "inputs/day3.txt"

with open(file, "r") as f:
    trees = [read_trees(line) for line in f]
    height = len(trees)

with open(file, "r") as f:
    width = len(f.readline()) - 1


def day3_part1():
    print(hit_trees_for_slope(3, 1))


def day3_part2():
    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    print(math.prod([hit_trees_for_slope(right, down) for (right, down) in slopes]))


def hit_trees_for_slope(right, down):
    x = 0
    y = 0
    num_trees = 0

    while y + down < height:
        x = (x + right) % width
        y += down
        num_trees += 1 if x in trees[y] else 0

    return num_trees
