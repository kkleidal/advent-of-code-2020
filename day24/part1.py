import sys
from collections import defaultdict

seqs = []
for line in sys.stdin:
    line = line.strip()
    if line:
        i = 0
        seq = []
        while i < len(line):
            c = line[i]
            if c in ("s", "n"):
                second = line[i + 1]
                seq.append(line[i : i + 2])
                i += 2
            elif c in ("e", "w"):
                seq.append(c)
                i += 1
            else:
                assert False, c
        seqs.append(seq)

add_vec = lambda x, y: tuple(sum(els) for els in zip(x, y))

directions = {
    "w": (0, -2),
    "e": (0, 2),
    "nw": (-1, -1),
    "ne": (-1, 1),
    "sw": (1, -1),
    "se": (1, 1),
}
memory = defaultdict(bool)

for seq in seqs:
    pos = (0, 0)
    for inst in seq:
        vec = directions[inst]
        new_pos = add_vec(vec, pos)
        pos = new_pos
    memory[pos] = not memory[pos]
    if not memory[pos]:
        # GC:
        del memory[pos]

count = lambda memory: sum(1 if v else 0 for v in memory.values())

print("Part 1:", count(memory))


def count_adjacent(pos, occupied):
    occupied_neighbors = 0
    for vec in directions.values():
        npos = add_vec(vec, pos)
        if npos in occupied:
            occupied_neighbors += 1
    return occupied_neighbors


for day in range(100):
    occupied = set()
    neighbors_of_occupied = set()
    for pos, is_black in memory.items():
        assert is_black
        occupied.add(pos)
        for vec in directions.values():
            neighbors_of_occupied.add(add_vec(vec, pos))
    unoccupied_neighbors_of_occupied = neighbors_of_occupied - occupied

    new_memory = dict(memory)
    for pos in occupied:
        occupied_neighbors = count_adjacent(pos, occupied)
        if occupied_neighbors == 0 or occupied_neighbors > 2:
            # Flip white
            del new_memory[pos]

    for pos in unoccupied_neighbors_of_occupied:
        occupied_neighbors = count_adjacent(pos, occupied)
        if occupied_neighbors == 2:
            # Flip black
            new_memory[pos] = True
    memory = new_memory

    print(f"Day {day + 1}: {count(memory)}")
