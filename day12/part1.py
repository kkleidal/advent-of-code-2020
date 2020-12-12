import sys
import numpy as np

rot90degree_left = np.array([[0, -1], [1, 0]])


def matexp(m, times):
    if times == 0:
        return np.eye(m.shape[0], dtype=m.dtype)
    out = m
    for t in range(1, times):
        out = out @ m
    return out


def rotate_left(vec, deg):
    assert deg % 90 == 0
    times = (deg // 90) % 4
    return (np.reshape(vec, [1, -1]) @ matexp(rot90degree_left, times)).squeeze(0)


def rotate_right(vec, deg):
    return rotate_left(vec, 360 - (deg % 360))


if __name__ == "__main__":
    direction = np.array([0, 1])
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
                position += arg * direction
            elif inst in cardinal:
                position += arg * cardinal[inst]
            elif inst == "R":
                direction = rotate_right(direction, arg)
            elif inst == "L":
                direction = rotate_left(direction, arg)
            else:
                raise NotImplementedError()

    print(position)
    print(np.abs(position).sum())
