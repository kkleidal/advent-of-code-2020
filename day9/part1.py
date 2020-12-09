import sys
from collections import defaultdict, deque


class SumTracker:
    def __init__(self, max_len):
        self.__deque = deque()
        self.__max_len = max_len
        self.sums = defaultdict(set)

    def add(self, inp):
        self.__deque.append(inp)
        if len(self.__deque) > self.__max_len:
            self.__deque.popleft()
        self.sums.clear()
        for i in range(len(self.__deque)):
            for j in range(i + 1, len(self.__deque)):
                x = self.__deque[i]
                y = self.__deque[j]
                self.sums[(x + y)].add((x, y))


preamble_length = 25
tracker = SumTracker(preamble_length)
for pos, line in enumerate(sys.stdin):
    line = line.strip()
    if line:
        line = int(line)
        if pos >= preamble_length:
            if line not in tracker.sums:
                print(line)
                break
        tracker.add(line)
