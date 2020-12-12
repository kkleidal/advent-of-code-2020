import sys
import numpy as np
from part1 import rotate_left, rotate_right

if __name__ == "__main__":
    wp = np.array([1, 10])
    position = np.array([0, 0])
    cardinal = {
        "N": np.array([1, 0]),
        "E": np.array([0, 1]),
        "S": np.array([-1, 0]),
        "W": np.array([0, -1]),
    }
    for line in sys.stdin:
        line = line.strip()
        if line:
            inst = line[0]
            arg = int(line[1:])

            if inst == "F":
                position += arg * wp
            elif inst in cardinal:
                wp += arg * cardinal[inst]
            elif inst == "R":
                wp = rotate_right(wp, arg)
            elif inst == "L":
                wp = rotate_left(wp, arg)
            else:
                raise NotImplementedError()

    print(position)
    print(np.abs(position).sum())
