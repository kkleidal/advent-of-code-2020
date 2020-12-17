import sys
from functools import reduce
import itertools


def parse(dims=3):
    active = set()
    for i, line in enumerate(sys.stdin):
        line = line.strip()
        if line:
            for j, c in enumerate(line):
                if c == "#":
                    active.add((i, j) + ((0,) * (dims - 2)))
    return active


def draw(active):
    minimums = [min(p[i] for p in active) for i in range(3)]
    maximums = [max(p[i] for p in active) for i in range(3)]
    for z in range(minimums[2], maximums[2] + 1):
        print(f"z={z}")
        for y in range(minimums[0], maximums[0] + 1):
            for x in range(minimums[1], maximums[1] + 1):
                print("#" if (y, x, z) in active else ".", end="")
            print()
        print()


def find_neighbors_single(point):
    for displacement in itertools.product(*[[-1, 0, 1] for _ in range(len(point))]):
        if all(dx == 0 for dx in displacement):
            continue
        yield tuple(x + dx for x, dx in zip(displacement, point))


def find_neighbors(active):
    return reduce(
        lambda x, y: x | y,
        (set(find_neighbors_single(point)) for point in active),
        set(),
    )


def step(active):
    neighbors = find_neighbors(active)
    inactive = neighbors - active
    count_of_active_neighbors = {
        p1: sum(1 for p2 in find_neighbors_single(p1) if p2 in active)
        for p1 in active | neighbors
    }
    newly_active = {p for p in inactive if count_of_active_neighbors[p] == 3}
    no_longer_active = {
        p for p in active if not (2 <= count_of_active_neighbors[p] <= 3)
    }
    return (active | newly_active) - no_longer_active


def run(dims=3):
    active = parse(dims)
    print(len(active))
    # draw(active)
    for i in range(6):
        active = step(active)
        print(f"After step {i+1}: {len(active)}")
        # draw(active)


if __name__ == "__main__":
    run(dims=3)
