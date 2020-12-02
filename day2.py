class Password:
    def __init__(self, pw: str):
        parts = pw.split(":")
        self._create_rule(parts[0])
        self.password = parts[1].strip(" ")

    def is_valid(self):
        char_count = self.password.count(self.char)
        return self.min <= char_count <= self.max

    def is_valid_2(self):
        first = self.password[self.min - 1] == self.char
        second = self.password[self.max - 1] == self.char
        return first != second

    def _create_rule(self, rule: str):
        parts = rule.split(" ")
        minMax = parts[0].split("-")
        self.min = int(minMax[0])
        self.max = int(minMax[1])
        self.char = parts[1]


with open("inputs/day2.txt", "r") as f:
    passwords = [Password(line) for line in f]


def day2_part1():
    valid_pws = sum(1 for pw in passwords if pw.is_valid())
    print(valid_pws)


def day2_part2():
    valid_pws = sum(1 for pw in passwords if pw.is_valid_2())
    print(valid_pws)
