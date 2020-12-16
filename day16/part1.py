import sys
from typing import Dict, List, Tuple, NamedTuple
import tqdm


class PuzzleInput(NamedTuple):
    rules: Dict[str, List[Tuple[int, int]]]
    my_ticket: List[int]
    nearby_tickets: List[List[int]]


def parse_input(fileobj=sys.stdin):
    rules = {}
    my_ticket = None
    nearby_tickets = []
    state = 0
    parse_ticket = lambda line: list(map(int, line.split(",")))
    for line in fileobj:
        line = line.strip()
        if line:
            if state == 0:
                # Parse rule
                class_name, rules_stmt = line.split(": ")
                ranges = [
                    tuple(map(int, rule.split("-")))
                    for rule in rules_stmt.split(" or ")
                ]
                rules[class_name] = ranges
            elif state == 1:
                state += 1
            elif state == 2:
                # Parse your ticket
                my_ticket = parse_ticket(line)
            elif state == 3:
                state += 1
            elif state == 4:
                # Parse nearby ticket
                nearby_tickets.append(parse_ticket(line))
            else:
                assert False
        else:
            state += 1
    return PuzzleInput(rules, my_ticket, nearby_tickets)


def find_invalid_values(ticket, rules):
    assert len(ticket) == len(rules)
    return [
        field
        for field in ticket
        if not any(x <= field <= y for rngs in rules.values() for x, y in rngs)
    ]


if __name__ == "__main__":
    inp = parse_input()

    error_rate = 0
    for ticket in tqdm.tqdm(inp.nearby_tickets):
        error_rate += sum(find_invalid_values(ticket, inp.rules))

    print(error_rate)
