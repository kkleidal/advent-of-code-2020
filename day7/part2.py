from part1 import get_rules
from collections import defaultdict

def count_bags_inside(adjacency, color):
    total = 0
    for other_color, quantity in adjacency[color].items():
        total += quantity * (1 + count_bags_inside(adjacency, other_color))
    return total
        

def part2():
    adjacency = defaultdict(lambda: defaultdict(int))
    for outer, quantity, inner in get_rules():
        adjacency[outer][inner] += quantity
    print(count_bags_inside(adjacency, "shiny gold"))

if __name__ == "__main__":
    part2()
