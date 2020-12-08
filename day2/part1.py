import sys
from collections import Counter

n_valid = 0
for line in sys.stdin:
    line = line.strip()
    if line:
        policy, password = line.split(": ")
        count_range, letter = policy.split(" ")
        min_count, max_count = map(int, count_range.split("-"))
        counts = Counter(password)
        count = counts.get(letter, 0)
        valid = count >= min_count and count <= max_count
        if valid:
            n_valid += 1
print(n_valid)
