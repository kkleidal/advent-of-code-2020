import sys
import re
from collections import defaultdict


whole_rule = re.compile(r"^([a-z ]+) bags contain (\d+ [a-z ]+ bags?(?:, \d+ [a-z ]+ bags?)*|no other bags)\.$")
pred_part = re.compile(r"^(\d+) ([a-z ]+) bags?$")
def parse_rule(line):
    m = whole_rule.match(line)
    assert m, f"{line} doesn't match whole_rule"
    subject, predicate = m.groups()
    if predicate != "no other bags":
        for item in predicate.split(", "):
            m2 = pred_part.match(item)
            quantity, kind = m2.groups()
            yield (subject, int(quantity), kind)


def get_rules():
    for line in sys.stdin:
        line = line.strip()
        if line:
            yield from parse_rule(line)

def find_all_outer_colors(adjacency, current_color, history):
    for color in adjacency[current_color]:
        if color == current_color or color in history:
            # Prevent infinite recursion
            continue
        yield color
        yield from find_all_outer_colors(adjacency, color, history + (current_color,))


def part1():
    adjacency = defaultdict(set)
    for outer, _, inner in get_rules():
        adjacency[inner].add(outer)
    print(len(set(find_all_outer_colors(adjacency, "shiny gold", ()))))

if __name__ == "__main__":
    part1()
