import re

file = "inputs/day4.txt"


class Passport:
    def __init__(self, passport: list[str]):
        self.fields = {}

        for line in passport:
            [self._add_field(field) for field in line.split(" ")]

    def _add_field(self, field: str):
        parts = field.split(":")
        self.fields[parts[0]] = parts[1].replace("\n", "")

    def has_fields(self, fields: list[str]):
        return all((field in self.fields) for field in fields)

    def is_valid(self):
        if not self.has_fields(["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]):
            return False

        if not (1920 <= int(self.fields["byr"]) <= 2002) or \
                not 2010 <= int(self.fields["iyr"]) <= 2020 or \
                not 2020 <= int(self.fields["eyr"]) <= 2030 or \
                not self._has_valid_height() or \
                not self._has_valid_hair_color() or \
                not self._has_valid_eye_color() or \
                not self._has_valid_passport_id():
            return False

        return True

    def _has_valid_eye_color(self):
        valid_colors = {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}
        eye_color = self.fields["ecl"]

        return eye_color in valid_colors

    def _has_valid_hair_color(self):
        hair_color = self.fields["hcl"]

        return re.match("^#[0-9a-f]{6}$", hair_color)

    def _has_valid_height(self):
        height = self.fields["hgt"]

        if height.endswith("cm") and \
                height[:-2].isnumeric() and \
                150 <= int(height[:-2]) <= 193:
            return True

        if height.endswith("in") and \
                height[:-2].isnumeric() and \
                59 <= int(height[:-2]) <= 76:
            return True

        return False

    def _has_valid_passport_id(self):
        passport_id = self.fields["pid"]

        return re.match("^[0-9]{9}$", passport_id)


with open(file, "r") as f:
    lines = []
    passports = []

    for line in f:
        if line == "\n":
            passports.append(Passport(lines))
            lines = []
        else:
            lines.append(line)

    passports.append(Passport(lines))


def day4_part1():
    fields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]

    print(sum(1 for passport in passports if passport.has_fields(fields)))


def day4_part2():
    print(sum(1 for passport in passports if passport.is_valid()))
