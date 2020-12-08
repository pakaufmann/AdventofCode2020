file = "inputs/day8.txt"


class Instruction:
    def __init__(self, line="", name: str = "", number: int = 0):
        parts = line.split(" ")
        if line != "":
            self.name = parts[0]
            self.number = int(parts[1])
        else:
            self.name = name
            self.number = number


class Machine:
    def __init__(self, lines: list[str], instructions: list[Instruction]):
        self.accumulator = 0
        self.ip = 0

        if len(instructions) == 0:
            self.instructions = [Instruction(line) for line in lines]
        else:
            self.instructions = instructions

    def replace_instruction(self, index, with_instruction):
        new_instructions = self.instructions.copy()
        new_instructions[index] = Instruction("", with_instruction, new_instructions[index].number)

        return Machine("", new_instructions)

    def run(self):
        while True:
            if self.ip >= len(self.instructions):
                break

            instruction = self.instructions[self.ip]

            if instruction.name == "nop":
                self.ip += 1
            elif instruction.name == "acc":
                self.accumulator += instruction.number
                self.ip += 1
            elif instruction.name == "jmp":
                self.ip += instruction.number
            else:
                raise Exception("no valid instruction: ", instruction.name)

            yield self.ip, self.accumulator


with open(file, "r") as f:
    machine = Machine(f.readlines(), list())


def day8_part1():
    endless, result = runs_endless(machine)
    print(result[1])


def day8_part2():
    for index, instruction in enumerate(machine.instructions):
        if instruction.name == "nop":
            new_machine = machine.replace_instruction(index, "jmp")
        elif instruction.name == "jmp":
            new_machine = machine.replace_instruction(index, "nop")
        else:
            continue

        endless, result = runs_endless(new_machine)
        if not endless:
            print(result[1])
            break

    pass


def runs_endless(machine: Machine) -> (bool, tuple[int, int]):
    run_ips = set()
    last_i = 0

    for i in machine.run():
        last_i = i
        new_ip = i[0]
        if new_ip in run_ips:
            return True, i

        run_ips.add(new_ip)

    return False, last_i
