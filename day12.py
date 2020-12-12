from enum import IntEnum


class Direction(IntEnum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


class Ship:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.direction = Direction.EAST

    def move(self, instruction: str, steps: int):
        if instruction == "N":
            self.y -= steps
        elif instruction == "S":
            self.y += steps
        elif instruction == "E":
            self.x += steps
        elif instruction == "W":
            self.x -= steps
        elif instruction == "L":
            new_direction = (int(self.direction) - (steps / 90)) % 4
            self.direction = Direction(new_direction)
        elif instruction == "R":
            new_direction = (int(self.direction) + (steps / 90)) % 4
            self.direction = Direction(new_direction)
        elif instruction == "F":
            if self.direction == Direction.NORTH:
                self.y -= steps
            elif self.direction == Direction.SOUTH:
                self.y += steps
            elif self.direction == Direction.EAST:
                self.x += steps
            elif self.direction == Direction.WEST:
                self.x -= steps


class WaypointShip:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.waypoint_x = 10
        self.waypoint_y = -1

    def move(self, instruction: str, steps: int):
        if instruction == "N":
            self.waypoint_y -= steps
        elif instruction == "S":
            self.waypoint_y += steps
        elif instruction == "E":
            self.waypoint_x += steps
        elif instruction == "W":
            self.waypoint_x -= steps
        elif instruction == "L":
            new_x = self.waypoint_x
            new_y = self.waypoint_y

            for i in range(0, int(steps / 90)):
                tmp = new_x * -1
                new_x = new_y
                new_y = tmp

            self.waypoint_x = new_x
            self.waypoint_y = new_y
        elif instruction == "R":
            new_x = self.waypoint_x
            new_y = self.waypoint_y

            for i in range(0, int(steps / 90)):
                tmp = new_x
                new_x = new_y * -1
                new_y = tmp

            self.waypoint_x = new_x
            self.waypoint_y = new_y

        elif instruction == "F":
            self.x += steps * self.waypoint_x
            self.y += steps * self.waypoint_y


def read_instruction(line: str):
    return line[:1], int(line[1:])


with open("inputs/day12.txt", "r") as f:
    instructions = [read_instruction(line) for line in f]


def day12_part1():
    ship = Ship()

    for instruction, steps in instructions:
        ship.move(instruction, steps)

    print(abs(ship.x + ship.y))


def day12_part2():
    ship = WaypointShip()

    for instruction, steps in instructions:
        ship.move(instruction, steps)

    print(abs(ship.x + ship.y))
