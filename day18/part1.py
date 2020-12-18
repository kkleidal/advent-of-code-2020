import re
from collections import deque
import sys

token_pattern = re.compile(r"\b\d+\b|[+*()]")


def add(x, y):
    return x + y


def mul(x, y):
    return x * y


def evaluate(expr):
    tokens = token_pattern.findall(expr)
    stack = deque([0, add])
    for token in tokens:
        # print(stack, token)
        if token == "+":
            ...
        elif token == "*":
            stack.pop()
            stack.append(mul)
        elif token == "(":
            stack.append(0)
            stack.append(add)
        elif token == ")":
            # Pop op:
            stack.pop()
            # Then evaluate:
            right = stack.pop()
            op = stack.pop()
            left = stack.pop()
            result = op(left, right)
            stack.append(result)
            stack.append(add)
        else:
            right = int(token)
            op = stack.pop()
            left = stack.pop()
            result = op(left, right)
            stack.append(result)
            stack.append(add)

    # Pop the op
    stack.pop()
    # Return the value
    return stack.pop()


def run(evaluate):
    print("Examples:")
    print(evaluate("1 + 2 * 3 + 4 * 5 + 6"))
    print(evaluate("1 + (2 * 3) + (4 * (5 + 6))"))
    print(evaluate("2 * 3 + (4 * 5)"))
    print(evaluate("5 + (8 * 3 + 9 + 3 * 4 * 3)"))
    print(evaluate("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"))
    print(evaluate("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"))

    print()
    print("Answer:")

    def get_results():
        for line in sys.stdin:
            line = line.strip()
            if line:
                yield evaluate(line)

    print(sum(get_results()))


if __name__ == "__main__":
    run(evaluate)
