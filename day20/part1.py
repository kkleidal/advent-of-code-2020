import sys
import numpy as np
import scipy.signal
from collections import defaultdict
from functools import reduce


def load_tiles():
    state = 0
    tiles = {}
    rows = []
    for line in sys.stdin:
        line = line.strip()
        if state == 0:
            assert line.startswith("Tile")
            tile_id = int(line[len("Tile ") : -1])
            state = 1
        elif state == 1:
            if line != "":
                rows.append(np.array([c == "#" for c in line]))
            else:
                # End of tile
                tile = np.stack(rows, axis=0)
                tiles[tile_id] = tile
                rows = []
                state = 0
    if rows:
        tile = np.stack(rows, axis=0)
        tiles[tile_id] = tile
        rows = []
    return tiles


def to_binary(arr):
    out = 0
    for x in arr:
        out |= 1 if x else 0
        out <<= 1
    out >>= 1
    return out


def rotate_right(x):
    return x[:, ::-1].T


tiles = load_tiles()
top_edges = defaultdict(set)
right_edges = defaultdict(set)
bottom_edges = defaultdict(set)
left_edges = defaultdict(set)
tile_to_edges = {}
tile_id_to_image = {}
for tile_id, tile in tiles.items():
    found = {}
    images = {}
    for vflip in [False, True]:
        for hflip in [False, True]:
            for rot in [0, 1, 2, 3]:
                new_tile = tile.copy()
                if vflip:
                    new_tile = new_tile[::-1, :]
                if hflip:
                    new_tile = new_tile[:, ::-1]
                for _ in range(rot):
                    new_tile = rotate_right(new_tile)
                edges = (
                    to_binary(new_tile[0, :]),
                    to_binary(new_tile[:, -1]),
                    to_binary(new_tile[-1, :]),
                    to_binary(new_tile[:, 0]),
                )
                if edges not in found:
                    found[edges] = (vflip, hflip, rot)
                    images[edges] = new_tile
    for (top, right, bottom, left), (vflip, hflip, rot) in found.items():
        tile_identifier = (tile_id, (vflip, hflip, rot))
        top_edges[top].add(tile_identifier)
        right_edges[right].add(tile_identifier)
        bottom_edges[bottom].add(tile_identifier)
        left_edges[left].add(tile_identifier)
        tile_to_edges[tile_identifier] = (top, right, bottom, left)
        tile_id_to_image[tile_identifier] = images[(top, right, bottom, left)]
edges = [top_edges, right_edges, bottom_edges, left_edges]


def add_vec(x, dx):
    return tuple(i + j for i, j in zip(x, dx))


def reverse(d):
    return tuple(-i for i in d)


def to_grid(puzzle):
    min_y = min(p[0] for p in puzzle)
    min_x = min(p[1] for p in puzzle)
    max_y = max(p[0] for p in puzzle)
    max_x = max(p[1] for p in puzzle)
    grid = np.ones((max_y - min_y + 1, max_x - min_x + 1), dtype=np.int32) * -1
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if (y, x) in puzzle:
                grid[y - min_y, x - min_x] = puzzle[(y, x)][0]
    return grid


directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
puzzle = {(0, 0): (next(iter(tiles)), (False, False, 0))}


def solve_puzzle(puzzle):
    remaining_tiles = set(tiles) - {v[0] for v in puzzle.values()}
    if len(remaining_tiles) == 0:
        return puzzle

    possible_extensions = set()
    for p in puzzle:
        for direction in directions:
            np = add_vec(p, direction)
            if np not in puzzle:
                possible_extensions.add(np)

    constraints = {}
    for np in possible_extensions:
        c = []
        for i, direction in enumerate(directions):
            p = add_vec(np, direction)
            if p in puzzle:
                p_direction = directions.index(reverse(direction))
                c.append(tile_to_edges[puzzle[p]][p_direction])
            else:
                c.append(None)
        constraints[np] = c

    # Find if any meet the constraints:
    possible_plays = {}
    for np, const in constraints.items():
        possible_tiles = None
        for i, v in enumerate(const):
            if v is not None:
                local_tiles = edges[i][v]
                local_tiles = {t for t in local_tiles if t[0] in remaining_tiles}
                if local_tiles:
                    if possible_tiles is None:
                        possible_tiles = local_tiles
                    possible_tiles &= local_tiles
        if possible_tiles is not None and len(possible_tiles) > 0:
            possible_plays[np] = possible_tiles

    possible_plays = sorted(possible_plays.items(), key=lambda kvp: len(kvp[1]))
    for loc, possible_tiles in possible_plays:
        for tile in possible_tiles:
            new_puzzle = puzzle.copy()
            new_puzzle[loc] = tile
            solved = solve_puzzle(new_puzzle)
            if solved:
                return solved
    return None


def corners_prod(puzzle):
    puzzle = to_grid(puzzle)
    return (
        puzzle[0, 0].item()
        * puzzle[0, -1].item()
        * puzzle[-1, -1].item()
        * puzzle[-1, 0].item()
    )


def stitch(puzzle):
    min_y = min(p[0] for p in puzzle)
    min_x = min(p[1] for p in puzzle)
    max_y = max(p[0] for p in puzzle)
    max_x = max(p[1] for p in puzzle)
    rows = []
    for y in range(min_y, max_y + 1):
        row = []
        for x in range(min_x, max_x + 1):
            assert (y, x) in puzzle
            tile_identifier = puzzle[y, x]
            # Strip border
            img = tile_id_to_image[tile_identifier][1:-1, 1:-1]
            row.append(img)
        row = np.concatenate(row, axis=1)
        rows.append(row)
    return np.concatenate(rows, axis=0)


seamonster_str = """                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """

seamonster = []
for line in seamonster_str.split("\n"):
    row = []
    for c in line:
        row.append(c == "#")
    seamonster.append(row)
seamonster = np.stack(seamonster, axis=0)


if __name__ == "__main__":
    solved = solve_puzzle(puzzle)
    print("Part 1:", corners_prod(solved))
    img = stitch(solved)
    counts = []
    for vflip in [False, True]:
        for hflip in [False, True]:
            for rot in [0, 1, 2, 3]:
                new_img = img.copy()
                if vflip:
                    new_img = new_img[::-1, :]
                if hflip:
                    new_img = new_img[:, ::-1]
                for _ in range(rot):
                    new_img = rotate_right(new_img)
                detection = scipy.signal.convolve2d(
                    new_img.astype(np.uint8), seamonster.astype(np.uint8), mode="same"
                )
                centers = detection == np.count_nonzero(seamonster)
                seamonster_count = np.count_nonzero(centers)
                if seamonster_count:
                    counts.append(
                        np.count_nonzero(img)
                        - seamonster_count * np.count_nonzero(seamonster)
                    )

    print("Part 2:", counts[0])
