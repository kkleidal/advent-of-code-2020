import sys


def get_seat_ids():
    for line in sys.stdin:
        line = line.strip()
        if line:
            line = line.replace("F", "0")
            line = line.replace("B", "1")
            line = line.replace("L", "0")
            line = line.replace("R", "1")
            yield int(line, 2)


print(max(get_seat_ids()))
