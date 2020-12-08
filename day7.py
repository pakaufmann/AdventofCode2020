import functools
import itertools

file = "inputs/day7.txt"

bags: dict[str, dict[str, int]] = {}


def get_bag_with_amount(contains_bag):
    parts = contains_bag.strip().replace(".", "").split(" ", 1)

    return str(parts[1].replace("bags", "").replace("bag", "").strip()), int(parts[0])


def get_bag(bag):
    parts = bag.split(" contain ")
    bag_name = str(parts[0])
    contains_bags = parts[1].split(",")

    if contains_bags[0] == "no other bags.":
        contains = dict()
    else:
        contains = dict([get_bag_with_amount(contains_bag) for contains_bag in contains_bags])

    return bag_name.replace(" bags", ""), contains


with open(file, "r") as f:
    for bag in [get_bag(line.replace("\n", "")) for line in f]:
        bags[bag[0]] = bag[1]


def bag_can_contain(container_bag: str, search_bag: str):
    can_contain_bags = bags.get(container_bag)

    if search_bag in can_contain_bags:
        return True

    for contains_bag in can_contain_bags:
        if bag_can_contain(contains_bag, search_bag):
            return True

    return False


def bag_contains_count(search_bag: str) -> int:
    bag_count = 0
    for contains_bag, count in bags.get(search_bag).items():
        bag_count += count
        bag_count += count * bag_contains_count(contains_bag)

    return bag_count


def day7_part1():
    num_of_bags_contain_gold = sum(1 for bag in bags if bag_can_contain(bag, 'shiny gold'))
    print(num_of_bags_contain_gold)


def day7_part2():
    number_of_bags_in_gold = bag_contains_count('shiny gold')
    print(number_of_bags_in_gold)
