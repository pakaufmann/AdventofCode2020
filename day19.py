import copy
import re


class Rule:
    def __init__(self, number: int, rule: str):
        self.number = number
        self.recursive = False
        self.build_parts(rule)

    def build_parts(self, rule):
        self.parts = []
        current: list[str] = []
        for part in rule.split(" "):
            if part == "|":
                self.parts.append(current)
                current = []
            else:
                current.append(part.replace("\"", ""))
        self.parts.append(current)

    def finished(self):
        return all(all(not p.isnumeric() or int(p) == self.number for p in part) for part in self.parts)

    def to_rule_string(self, depth: int = 10):
        rule_string = "("

        for i, part in enumerate(self.parts):
            if i > 0:
                rule_string += "|"

            if self.recursive and str(self.number) in part:
                if depth > 0:
                    rule_string += "".join(part)
                    foo = self.to_rule_string(depth - 1)
                    rule_string = rule_string.replace(str(self.number), "(" + foo + ")")
                else:
                    rule_string = rule_string[:-1]
            else:
                rule_string += "".join(part)

        return rule_string + ")"

    def replace_with(self, finished_rules: dict):
        for part in self.parts:
            for i, p in enumerate(part):
                if p.isnumeric() and int(p) in finished_rules:
                    part[i] = finished_rules[int(p)].to_rule_string()


rules: list[Rule] = []
messages = []

with open("inputs/day19.txt", "r") as f:
    state = 0
    for line in f:
        if line == "\n":
            state = 1
            continue

        if state == 0:
            parts = line.split(":")
            rules.append(Rule(int(parts[0]), parts[1].replace("\n", "").strip()))
        else:
            messages.append(line)


def day19_part1():
    unfinished_rules = list(copy.deepcopy(rules))
    finished_rules: dict = dict(map(lambda x: (x.number, x), list(filter(lambda x: x.finished(), unfinished_rules))))

    while unfinished_rules:
        for unfinished_rule in unfinished_rules:
            unfinished_rule.replace_with(finished_rules)

            if unfinished_rule.finished():
                unfinished_rules.remove(unfinished_rule)
                finished_rules[unfinished_rule.number] = unfinished_rule

    final_rule = re.compile("^" + finished_rules[0].to_rule_string() + "$")
    matching_count = sum(1 for message in messages if final_rule.match(message))

    print(matching_count)


def day19_part2():
    unfinished_rules = list(copy.deepcopy(rules))
    for unfinished_rule in unfinished_rules:
        if unfinished_rule.number == 8:
            unfinished_rule.build_parts("42 | 42 8")
            unfinished_rule.recursive = True

        if unfinished_rule.number == 11:
            unfinished_rule.build_parts("42 31 | 42 11 31")
            unfinished_rule.recursive = True

    finished_rules: dict = dict(map(lambda x: (x.number, x), list(filter(lambda x: x.finished(), unfinished_rules))))

    while unfinished_rules:
        for unfinished_rule in unfinished_rules:
            unfinished_rule.replace_with(finished_rules)

            if unfinished_rule.finished():
                unfinished_rules.remove(unfinished_rule)
                finished_rules[unfinished_rule.number] = unfinished_rule

    final_rule = re.compile("^" + finished_rules[0].to_rule_string() + "$")

    matching_count = sum(1 for message in messages if final_rule.match(message))

    print(matching_count)
