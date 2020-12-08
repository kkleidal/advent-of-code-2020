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


def find_my_seat():
    seat_ids = list(get_seat_ids())
    arr = [False for _ in range(max(seat_ids) + 1)]
    for seat_id in seat_ids:
        arr[seat_id] = True
    for i in range(1, len(arr) - 1):
        if not arr[i] and arr[i - 1] and arr[i + 1]:
            return i


print(find_my_seat())
