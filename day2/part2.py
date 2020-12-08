import sys


def exactly_one(iterable):
    return sum(1 if x else 0 for x in iterable) == 1


n_valid = 0
for line in sys.stdin:
    line = line.strip()
    if line:
        policy, password = line.split(": ")
        count_range, letter = policy.split(" ")
        indices = [int(x) - 1 for x in count_range.split("-")]
        valid = exactly_one(password[i] == letter for i in indices)
        if valid:
            n_valid += 1
print(n_valid)
