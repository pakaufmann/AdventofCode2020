import itertools

numbers = [int(n) for n in open("inputs/day15.txt", "r").readline().split(",")]


class Speaker:
    def __init__(self, init_numbers: list[int]):
        self.numbers = init_numbers
        self.initial_length = len(self.numbers)
        self.spoken_numbers: dict[int, int] = {}

    def speak_next(self):
        current_index = 0
        spoken_number = 0

        while True:
            previous_index = current_index - 1

            if current_index < self.initial_length:
                if previous_index >= 0:
                    self.spoken_numbers[spoken_number] = previous_index

                spoken_number = self.numbers[current_index]
            elif spoken_number in self.spoken_numbers:
                previous_found = self.spoken_numbers[spoken_number]
                self.spoken_numbers[spoken_number] = previous_index
                spoken_number = previous_index - previous_found
            else:
                self.spoken_numbers[spoken_number] = previous_index
                spoken_number = 0

            current_index += 1
            yield spoken_number


def day15_part1():
    number_to_find = 2020
    print(next(itertools.islice(Speaker(numbers).speak_next(), number_to_find - 1, None)))


def day15_part2():
    number_to_find = 30000000
    print(next(itertools.islice(Speaker(numbers).speak_next(), number_to_find - 1, None)))
