from part1 import run, token_pattern


def to_int(x):
    try:
        return int(x)
    except ValueError:
        return x


def eval_expr(tokens):
    # print("Parsing parens")
    i = 0
    while i < len(tokens):
        # print(tokens, i)
        token = tokens[i]
        if token == "(":
            result = eval_expr(tokens[i + 1 :])
            tokens = tokens[:i] + result
        elif token == ")":
            break
        i += 1

    # print("Parsing add")
    i = 0
    while i < len(tokens):
        # print(tokens, i)
        token = tokens[i]
        if token == "+":
            result = tokens[i - 1] + tokens[i + 1]
            tokens = tokens[: i - 1] + [result] + tokens[i + 2 :]
            i -= 1
        elif token == ")":
            break
        i += 1

    # print("Parsing mul")
    i = 0
    while i < len(tokens):
        # print(tokens, i)
        token = tokens[i]
        if token == "*":
            result = tokens[i - 1] * tokens[i + 1]
            tokens = tokens[: i - 1] + [result] + tokens[i + 2 :]
            i -= 1
        elif token == ")":
            break
        i += 1

    if len(tokens) > 1:
        assert tokens[1] == ")"
        tokens = tokens[:1] + tokens[2:]

    return tokens


def evaluate(expr):
    tokens = token_pattern.findall(expr)
    tokens = [to_int(token) for token in tokens]
    tokens = eval_expr(tokens)
    assert len(tokens) == 1
    return tokens[0]


if __name__ == "__main__":
    run(evaluate)
