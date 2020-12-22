import collections

start_stack_1 = collections.deque()
start_stack_2 = collections.deque()


def day22_part1():
    print(run_game(run_round))


def day22_part2():
    print(run_game(run_round_recursive))


with open("inputs/day22.txt", "r") as f:
    f.readline()
    current_stack = start_stack_1

    for line in f:
        if line == "\n":
            continue

        if line.startswith("Player"):
            current_stack = start_stack_2
            continue

        current_stack.append(int(line))


def run_round(stack1, stack2, _1, _2):
    card1 = stack1.popleft()
    card2 = stack2.popleft()

    if card1 > card2:
        stack1.append(card1)
        stack1.append(card2)
    else:
        stack2.append(card2)
        stack2.append(card1)


def run_round_recursive(stack1: collections.deque, stack2: collections.deque, previous1: set, previous2: set):
    tupled_stack_1 = tuple(stack1)
    tupled_stack_2 = tuple(stack2)

    if tupled_stack_1 in previous1 or tupled_stack_2 in previous2:
        stack2.clear()
        return

    card1 = stack1.popleft()
    card2 = stack2.popleft()

    after_stack_1 = tuple(stack1)
    after_stack_2 = tuple(stack2)
    previous1.add(tupled_stack_1)
    previous2.add(tupled_stack_2)

    if len(stack1) >= card1 and len(stack2) >= card2:
        rec_stack_1 = collections.deque(after_stack_1[:card1])
        rec_stack_2 = collections.deque(after_stack_2[:card2])

        seen_1 = set()
        seen_2 = set()
        while rec_stack_1 and rec_stack_2:
            run_round_recursive(rec_stack_1, rec_stack_2, seen_1, seen_2)

        if not rec_stack_2:
            stack1.append(card1)
            stack1.append(card2)
        else:
            stack2.append(card2)
            stack2.append(card1)
    else:
        if card1 > card2:
            stack1.append(card1)
            stack1.append(card2)
        else:
            stack2.append(card2)
            stack2.append(card1)


def count_stack(player_stack):
    total = 0
    i = 0

    while player_stack:
        i += 1
        total += i * player_stack.pop()

    return total


def run_game(mode):
    player1_stack = start_stack_1.copy()
    player2_stack = start_stack_2.copy()
    seen_1 = set()
    seen_2 = set()

    while player1_stack and player2_stack:
        mode(player1_stack, player2_stack, seen_1, seen_2)
    if player1_stack:
        result = count_stack(player1_stack)
    else:
        result = count_stack(player2_stack)
    return result
