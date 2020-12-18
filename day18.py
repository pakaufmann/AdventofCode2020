import collections
import queue

sum_to_find = 2020

with open("inputs/day18.txt", "r") as f:
    lines = [line.replace("\n", "").replace("(", "( ").replace(")", " )").split(" ") for line in f]


def is_operator(token: str) -> bool:
    return token == "*" or token == "+"


def run_shunting_yard(tokens: list[str], precedence: dict[str, int]):
    output_queue = queue.SimpleQueue()
    operator_stack = list()

    while tokens:
        next_token = tokens[0]
        tokens = tokens[1:]

        if next_token.isdigit():
            output_queue.put(int(next_token))
        elif is_operator(next_token):
            while operator_stack and \
                    is_operator(operator_stack[-1]) and \
                    precedence[operator_stack[-1]] >= precedence[next_token]:
                output_queue.put(operator_stack.pop())

            operator_stack.append(next_token)
        elif next_token == "(":
            operator_stack.append(next_token)
        elif next_token == ")":
            while operator_stack[-1] != "(":
                output_queue.put(operator_stack.pop())

            if operator_stack[-1] == "(":
                operator_stack.pop()

    while operator_stack:
        output_queue.put(operator_stack.pop())

    return output_queue


def calculate(res) -> int:
    res_stack = list()
    while not res.empty():
        next_token = res.get()

        if next_token == "*":
            res_stack.append(res_stack.pop() * res_stack.pop())
        elif next_token == "+":
            res_stack.append(res_stack.pop() + res_stack.pop())
        else:
            res_stack.append(next_token)

    return res_stack[0]


def day18_part1():
    print(sum(calculate(run_shunting_yard(line, {"+": 0, "*": 0})) for line in lines))


def day18_part2():
    print(sum(calculate(run_shunting_yard(line, {"+": 1, "*": 0})) for line in lines))
