import itertools
import time

with open("inputs/day23.txt", "r") as f:
    starting_cups = [int(i) for i in f.readline()]


class Node(object):
    def __init__(self, data: int, next_node=None, previous_node=None):
        self.data = data
        self.next_node = next_node
        self.previous_node = previous_node

    def get_data(self):
        return self.data

    def remove_self(self):
        self.previous_node.next_node = self.next_node
        self.next_node.previous_node = self.previous_node

        self.next_node = None
        self.previous_node = None
        return self

    def set_next(self, new_next):
        old_next = self.next_node
        self.next_node.previous_node = new_next
        self.next_node = new_next
        new_next.previous_node = self
        new_next.next_node = old_next


def run_game(starting_cups: list[int]):
    num_to_node: dict[int, Node] = dict()
    start_node = None
    previous_node = None

    for cup in starting_cups:
        node = Node(cup, None, previous_node)

        if previous_node is not None:
            previous_node.next_node = node

        if start_node is None:
            start_node = node

        previous_node = node
        num_to_node[cup] = node

    previous_node.next_node = start_node
    start_node.previous_node = previous_node

    current_cup = start_node
    length = len(starting_cups)

    i = 0

    while True:
        take = [current_cup.next_node.remove_self(),
                current_cup.next_node.remove_self(),
                current_cup.next_node.remove_self()]

        destination_num = current_cup.data - 1
        if destination_num < 1:
            destination_num = length

        destination_cup = num_to_node[destination_num]

        while destination_cup.next_node is None:
            destination_num -= 1
            if destination_num < 1:
                destination_num = length
            destination_cup = num_to_node[destination_num]

        for cup in reversed(take):
            destination_cup.set_next(cup)

        current_cup = current_cup.next_node

        yield num_to_node


def day23_part1():
    final_layout = next(itertools.islice(run_game(starting_cups), 99, None))
    index_1 = final_layout[1]
    next_node = index_1.next_node
    output = ""

    while next_node is not index_1:
        output += str(next_node.data)
        next_node = next_node.next_node

    print(output)


def day23_part2():
    rest_nums = list(range(10, 1_000_001))
    start = time.time()
    final_layout = next(itertools.islice(run_game(starting_cups + rest_nums), 10_000_000 - 1, None))
    print(time.time() - start)

    number_1 = final_layout[1]
    num_1 = number_1.next_node.data
    num_2 = number_1.next_node.next_node.data

    print(num_1 * num_2)
