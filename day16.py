import functools
import re


class Rule:
    def __init__(self, name, rules: list[tuple[int, int]]):
        self.name = name
        self.rules = rules

    def matches(self, value: int) -> bool:
        return any(rule[0] <= value <= rule[1] for rule in self.rules)


class Ticket:
    def __init__(self, values: list[int]):
        self.values = values

    def completely_invalid_values(self, rules: list[Rule]) -> list[int]:
        return [value for value in self.values if not any(rule.matches(value) for rule in rules)]

    def is_valid(self, rules: list[Rule]) -> bool:
        return not self.completely_invalid_values(rules)

    def col_matches_rule(self, col: int, rule: Rule) -> bool:
        return rule.matches(self.values[col])


all_rules: list[Rule] = []
own_ticket: Ticket
nearby_tickets: list[Ticket] = []

rule_name_regex = re.compile(r'([a-z ]+): (.+)')


def create_rule(rule) -> tuple[int, int]:
    parts = rule.split("-")
    return int(parts[0]), int(parts[1])


def read_ticket(line: str) -> Ticket:
    return Ticket([int(field) for field in line.split(",")])


with open("inputs/day16.txt", "r") as f:
    mode = 0
    for line in f:
        line = line.replace("\n", "")

        if line == "":
            continue
        elif line == "your ticket:":
            mode = 1
            continue
        elif line == "nearby tickets:":
            mode = 2
            continue

        if mode == 0:
            matches = rule_name_regex.match(line)
            rule_name, matched_rules = matches.groups()

            all_rules.append(Rule(rule_name, [create_rule(rule) for rule in matched_rules.split(" or ")]))
        if mode == 1:
            own_ticket = read_ticket(line)
        if mode == 2:
            nearby_tickets.append(read_ticket(line))


def day16_part1():
    print(sum(sum(nearby_ticket.completely_invalid_values(all_rules)) for nearby_ticket in nearby_tickets))


def day16_part2():
    valid_tickets = [nearby_ticket for nearby_ticket in nearby_tickets if nearby_ticket.is_valid(all_rules)]

    remaining_rules = all_rules
    rule_to_col: dict[int, Rule] = {}

    while remaining_rules:
        for col_num in range(0, len(own_ticket.values)):
            matching_rules = []

            for remaining_rule in remaining_rules:
                if all(ticket.col_matches_rule(col_num, remaining_rule) for ticket in valid_tickets):
                    matching_rules.append(remaining_rule)

            if len(matching_rules) == 1:
                rule_to_col[col_num] = matching_rules[0]
                remaining_rules.remove(matching_rules[0])

    values = (own_ticket.values[index] for index, rule in rule_to_col.items() if rule.name.startswith("departure"))
    print(functools.reduce(lambda x, y: x * y, values))
