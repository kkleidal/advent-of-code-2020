from part1 import parse_input, find_invalid_values
import tqdm

inp = parse_input()

remaining_tickets = [
    ticket
    for ticket in inp.nearby_tickets
    if len(find_invalid_values(ticket, inp.rules)) == 0
]
col_possibilities = []
# Dictionaries are ordered in this version of Python, so this is fine:
for col in range(len(remaining_tickets[0])):
    possibilities = set(inp.rules)
    for rule_name in list(possibilities):
        rngs = inp.rules[rule_name]
        if any(
            not any(x <= ticket[col] <= y for x, y in rngs)
            for ticket in remaining_tickets
        ):
            possibilities.remove(rule_name)
    col_possibilities.append(possibilities)


def choose_possibilities(options):
    if len(options) == 0:
        yield {}
    else:
        options = sorted(options, key=lambda x: len(x[1]))
        for option in options[0][1]:
            suboptions = [(col, opt - {option}) for col, opt in options[1:]]
            for subbinding in choose_possibilities(suboptions):
                yield {options[0][0]: option, **subbinding}


options = list(enumerate(col_possibilities))
for possibility in choose_possibilities(options):
    prod = 1
    for col, name in possibility.items():
        if name.startswith("departure"):
            prod *= inp.my_ticket[col]
    print(possibility, prod)
