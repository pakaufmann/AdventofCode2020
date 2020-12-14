import itertools

with open("inputs/day14.txt", "r") as f:
    lines = [line.replace("\n", "").split(" = ") for line in f]


def day14_part1():
    last_bitmask = None
    memory = dict()

    for line in lines:
        if line[0] == "mask":
            last_bitmask = create_bitmasks(line[1])
        else:
            mem = read_mem_address(line)
            memory[mem] = apply_bitmasks(int(line[1]), last_bitmask)

    print(sum(memory.values()))


def day14_part2():
    initial_mask = 0
    floating_bitmasks = []

    memory = dict()

    for line in lines:
        if line[0] == "mask":
            mask = line[1]
            initial_mask, _ = create_bitmasks(mask)
            floating_bitmasks = [create_bitmasks(floating_mask) for floating_mask in (create_floating_masks(mask))]
        else:
            for floating_bitmask in floating_bitmasks:
                mem_to_write = apply_bitmasks(read_mem_address(line) | initial_mask, floating_bitmask)
                memory[mem_to_write] = int(line[1])

    print(sum(memory.values()))


def create_floating_masks(mask):
    floating_masks: list[str] = [""]
    for n in mask:
        if n == "X":
            floating_masks = list(itertools.chain(*[[mask + "1", mask + "0"] for mask in floating_masks]))
        else:
            floating_masks = [mask + "X" for mask in floating_masks]

    return floating_masks


def apply_bitmasks(num: int, masks: tuple[int, int]) -> int:
    return (num | masks[0]) & masks[1]


def read_mem_address(line):
    return int(line[0].replace("mem[", "").replace("]", ""))


def create_bitmasks(mask) -> tuple[int, int]:
    return int(mask.replace("X", "0"), 2), int(mask.replace("X", "1"), 2)
