import math
import re
import time
from functools import cache


class Tile:
    def __init__(self, id: int, rows: list[list[str]]):
        self.bottom_rows = []
        self.right_rows = []
        self.id = id
        self.rows = rows

    @cache
    def rotate_right(self):
        return Tile(self.id, list(zip(*self.rows[::-1])))

    def flip(self):
        return Tile(self.id, self.rows[::-1])

    def __repr__(self):
        return "\n".join(["".join(row) for row in self.rows])

    def add_neighbours(self, combinations):
        bottom = self.rows[-1]
        rotated = self.rotate_right()
        right = rotated.rows[-1]

        for tile in combinations:
            if tile.id == self.id:
                continue

            tile_rotated = tile.rotate_right()

            if tile.rows[0] == bottom:
                self.bottom_rows.append(tile)

            if tile_rotated.rows[0] == right:
                self.right_rows.append(tile)


class Match:
    def __init__(self, regex: str):
        self.regex = re.compile(regex)
        self.replace = [i for i, x in enumerate(regex) if x == "#"]

    def match(self, input: str):
        return self.regex.match(input)

    def replace_with_O(self, x, input: str) -> str:
        line_2 = list(input)
        for replace in self.replace:
            line_2[x + replace] = "O"
        return "".join(line_2)


monster_line_1 = Match("..................#.")
monster_line_2 = Match("#....##....##....###")
monster_line_3 = Match(".#..#..#..#..#..#...")


class Picture:
    def __init__(self, tiles, picture: list[str] = None):
        if picture is not None:
            self.picture = picture
        else:
            picture_rows: dict[int, str] = dict()

            for (x, y), tile in tiles.items():
                for row_x, row in enumerate(tile.rows):
                    if row_x == 0 or row_x == len(tile.rows) - 1:
                        continue

                    picture_rows[x * 10 + row_x] = picture_rows.get(x * 10 + row_x, "") + "".join(row[1:-1])

            self.picture: list[str] = list(picture_rows.values())

    def mark_sea_monsters(self) -> bool:
        has_sea_monsters = False

        for i in range(0, len(self.picture) - 2):
            for x in range(0, len(self.picture) - 20):
                matches_1 = self.picture[i][x:x + 20]
                matches_2 = self.picture[i + 1][x:x + 20]
                matches_3 = self.picture[i + 2][x:x + 20]

                if monster_line_1.match(matches_1) and \
                        monster_line_2.match(matches_2) and \
                        monster_line_3.match(matches_3):
                    self.picture[i] = monster_line_1.replace_with_O(x, self.picture[i])
                    self.picture[i + 1] = monster_line_2.replace_with_O(x, self.picture[i + 1])
                    self.picture[i + 2] = monster_line_3.replace_with_O(x, self.picture[i + 2])
                    has_sea_monsters = True
        return has_sea_monsters

    def count_hash(self) -> int:
        return sum([line.count("#") for line in self.picture])

    def rotate_right(self):
        foo = ["".join(t) for t in list(zip(*self.picture[::-1]))]
        return Picture(None, picture=foo)

    def flip(self):
        return Picture(None, picture=self.picture[::-1])


tiles: list[Tile] = []

with open("inputs/day20.txt", "r") as f:
    rows: list[str] = []

    for line in f:
        line = line.replace("\n", "")

        if line.startswith("Tile"):
            rows = []
            id = int(line.replace("Tile ", "").replace(":", ""))
        elif line == "":
            tiles.append(Tile(id, [list(row) for row in rows]))
        else:
            rows.append(line)

    tiles.append(Tile(id, [list(row) for row in rows]))


def day20_part1():
    picture_tiles, square_size = find_picture()
    print(picture_tiles[(0, 0)].id *
          picture_tiles[(0, square_size - 1)].id *
          picture_tiles[(square_size - 1, 0)].id *
          picture_tiles[(square_size - 1, square_size - 1)].id)


def day20_part2():
    picture_tiles, _ = find_picture()
    picture = Picture(picture_tiles)
    flipped_picture = picture.flip()

    for i in range(0, 3):
        if picture.mark_sea_monsters():
            print(picture.count_hash())

        if flipped_picture.mark_sea_monsters():
            print(flipped_picture.count_hash())

        picture = picture.rotate_right()
        flipped_picture = flipped_picture.rotate_right()


def find_picture():
    all_combinations = list()
    for tile in tiles:
        flipped = tile.flip()

        all_combinations.append(tile)
        all_combinations.append(flipped)
        all_combinations.append(tile.rotate_right())
        all_combinations.append(tile.rotate_right().rotate_right())
        all_combinations.append(tile.rotate_right().rotate_right().rotate_right())
        all_combinations.append(flipped.rotate_right())
        all_combinations.append(flipped.rotate_right().rotate_right())
        all_combinations.append(flipped.rotate_right().rotate_right().rotate_right())

    for combination in all_combinations:
        combination.add_neighbours(all_combinations)

    square_size = int(math.sqrt(len(tiles)))
    picture = find_match(all_combinations, square_size)
    return picture, square_size


def find_match(all_combinations, square_size):
    for combination in all_combinations:
        picture = dict()
        picture[(0, 0)] = combination

        bottom = [combination]
        for i in range(0, square_size):
            if bottom:
                picture[(i, 0)] = bottom[0]

                to_right(picture, bottom[0].right_rows, square_size, i)
                bottom = bottom[0].bottom_rows

        if len(picture.items()) == len(tiles):
            return picture


def to_right(picture, right, square_size, x):
    for i in range(1, square_size):
        if right:
            picture[(x, i)] = right[0]
            right = right[0].right_rows
