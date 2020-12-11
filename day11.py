initial_seats: dict[tuple[int, int], bool] = dict()

with open("inputs/day11.txt", "r") as f:
    for y, line in enumerate(f.readlines()):
        for x, position in enumerate(line):
            if position == 'L':
                initial_seats[(x, y)] = False


def day11_part1():
    stable = run_until_stable(number_of_occupied_adjacent_seats, 4)
    print(sum([1 for seat in stable if stable[seat]]))


def day11_part2():
    visibility_map = calculate_visibility_map(set(initial_seats.keys()))

    stable = run_until_stable(number_of_occupied_visible_seats(visibility_map), 5)
    print(sum([1 for seat in stable if stable[seat]]))


def run_until_stable(rule, max_occupied):
    last = initial_seats

    while True:
        new = run_round(last, rule, max_occupied)
        if new == last:
            return last

        last = new


def run_round(seats, rule, max_occupied):
    new_seats = dict()
    for seat in seats:
        count = rule(seat, seats)
        occupied = seats[seat]

        if not occupied and count == 0:
            new_seats[seat] = True
        elif occupied and count >= max_occupied:
            new_seats[seat] = False
        else:
            new_seats[seat] = occupied

    return new_seats


deltas = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def calculate_visibility_map(seats: set[tuple[int, int]]) -> dict[tuple[int, int], set[tuple[int, int]]]:
    visibility_map: dict[tuple[int, int], set[tuple[int, int]]] = dict()
    max_x = max([x for x, y in seats])
    max_y = max([y for x, y in seats])

    for seat in seats:
        nearest_seats = set()
        visibility_map[seat] = nearest_seats

        for delta in deltas:
            next_to_check = (seat[0] + delta[0], seat[1] + delta[1])
            nearest = nearest_in_direction(next_to_check, delta, seats, max_x, max_y)
            if nearest is not None:
                nearest_seats.add(nearest)

    return visibility_map


def nearest_in_direction(pos, delta, seats: set[tuple[int, int]], max_x, max_y):
    if pos[0] < 0 or pos[1] < 0 or pos[0] > max_x or pos[1] > max_y:
        return None
    elif pos in seats:
        return pos
    else:
        return nearest_in_direction((pos[0] + delta[0], pos[1] + delta[1]), delta, seats, max_x, max_y)


def number_of_occupied_visible_seats(visibility_map: dict[tuple[int, int], set[tuple[int, int]]]):
    def calc(seat: tuple[int, int], seats: dict[tuple[int, int], bool]):
        count = 0

        for visibility in visibility_map[seat]:
            if seats[visibility]:
                count += 1

        return count

    return calc


def number_of_occupied_adjacent_seats(seat: tuple[int, int], seats: dict[tuple[int, int], bool]):
    count = 0

    for delta in deltas:
        pos = (seat[0] + delta[0], seat[1] + delta[1])

        if pos in seats and seats[pos]:
            count += 1

    return count
