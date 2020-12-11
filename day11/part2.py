import sys
import numpy as np
from collections import defaultdict
import itertools

grid = []

for line in sys.stdin:
    row = []
    line = line.strip()
    if line:
        for c in line:
            if c == "#":
                row.append(2)
            elif c == "L":
                row.append(1)
            elif c == ".":
                row.append(0)
    grid.append(row)

grid = np.array(grid)


def get_edges_raw(grid):
    last_row_index = np.zeros(grid.shape[1], dtype=np.int64)
    present = np.zeros(grid.shape[1], dtype=np.bool)
    for y in range(grid.shape[0]):
        row = grid[y]
        for x in range(grid.shape[1]):
            if row[x]:
                if present[x]:
                    edge = ((y, x), (last_row_index[x].item(), x))
                    yield edge
                present[x] = True
                last_row_index[x] = y


def get_edges_down(grid):
    yield from get_edges_raw(grid)


def get_edges_left(grid):
    adapt = lambda yx: (yx[1], yx[0])
    for p1, p2 in get_edges_down(grid.T):
        yield adapt(p1), adapt(p2)


def find_diags(grid, y, x, dy, dx):
    last = None
    while y < grid.shape[0] and x < grid.shape[1] and y >= 0 and x >= 0:
        p = (y, x)
        if grid[p]:
            if last is not None:
                yield (last, p)
            last = p
        y += dy
        x += dx


def get_edges_diag1(grid):
    dy = 1
    dx = 1

    for start_y in range(0, grid.shape[0]):
        y = start_y
        x = 0
        yield from find_diags(grid, y, x, dy, dx)

    for start_x in range(0, grid.shape[1]):
        x = start_x
        y = 0
        yield from find_diags(grid, y, x, dy, dx)


def get_edges_diag2(grid):
    dy = 1
    dx = -1

    for start_y in range(0, grid.shape[0]):
        y = start_y
        x = grid.shape[1] - 1
        yield from find_diags(grid, y, x, dy, dx)

    for start_x in range(0, grid.shape[1]):
        x = start_x
        y = 0
        yield from find_diags(grid, y, x, dy, dx)


seats = set()
full_seats = set()
for y in range(grid.shape[0]):
    for x in range(grid.shape[1]):
        p = (y, x)
        if grid[p] > 0:
            seats.add(p)
        if grid[p] == 2:
            full_seats.add(p)

adjacency = defaultdict(set)
for p1, p2 in itertools.chain(
    get_edges_down(grid),
    get_edges_left(grid),
    get_edges_diag1(grid),
    get_edges_diag2(grid),
):
    assert p1 in seats
    assert p2 in seats
    # Undirected graph:
    adjacency[p1].add(p2)
    adjacency[p2].add(p1)


def draw():
    for y in range(grid.shape[0]):
        line = ""
        for x in range(grid.shape[1]):
            is_seat = (y, x) in seats
            is_full = (y, x) in full_seats
            c = "."
            if is_seat:
                c = "#" if is_full else "L"
            line += c
        print(line)
    print()


while True:
    # draw()
    left_seats = set()
    newly_occupied_seats = set()
    for seat in seats:
        # Count adjacent:
        adjacent = 0
        for neighbor in adjacency[seat]:
            if neighbor in full_seats:
                adjacent += 1
        if adjacent >= 5 and seat in full_seats:
            left_seats.add(seat)
        elif adjacent == 0 and seat not in full_seats:
            newly_occupied_seats.add(seat)
    new_full_seats = (full_seats | newly_occupied_seats) - left_seats
    if new_full_seats == full_seats:
        break
    full_seats = new_full_seats

print(len(full_seats))
