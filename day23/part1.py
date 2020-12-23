import sys
from tqdm import tqdm


class LLNode:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None

    def __str__(self):
        return "N<%r>" % self.value

    def __repr__(self):
        return str(self)


class LL:
    def __init__(self, iterable=[]):
        self.lookup = {}
        self.current = None
        self.staging = None
        self.staged_values = None
        self.update(iterable)

    def add(self, value):
        self.check_rep()
        assert value not in self.lookup
        node = LLNode(value)
        self.lookup[value] = node
        if not self.current:
            self.current = node
        node.prev = self.current.prev or self.current
        node.next = self.current
        self.current.prev.next = node
        self.current.prev = node
        self.check_rep()

    def check_rep(self):
        if self.current is None:
            return
        prev = None
        for el in self:
            assert el.next
            assert el.prev
            if prev is not None:
                assert el.prev == prev
                assert prev.next == el
        assert el.next == self.current
        assert self.current.prev == el

    def update(self, values):
        for x in values:
            self.add(x)

    def __iter__(self):
        el = self.current
        first = True
        while first or el is not self.current:
            yield el
            first = False
            el = el.next

    def __str__(self):
        return "LL%r" % (list(self),)

    def __repr__(self):
        return str(self)

    def __pickup(self):
        assert self.staging == None
        picked_up = []
        el = self.current
        for _ in range(3):
            el = el.next
            picked_up.append(el)
        picked_up[0].prev.next = picked_up[-1].next
        picked_up[-1].next.prev = picked_up[0].prev
        picked_up[0].prev = None
        picked_up[-1].next = None
        self.staged = picked_up
        self.staged_values = {n.value for n in self.staged}

    def __select_destination(self):
        min_value = min(self.lookup)
        max_value = max(self.lookup)
        v = self.current.value - 1
        while v not in self.lookup or v in self.staged_values:
            if v < min_value:
                v = max_value
            else:
                v -= 1
        return self.lookup[v]

    def shuffle_round(self):
        self.check_rep()
        self.__pickup()
        dest_node = self.__select_destination()

        dest_node.next.prev = self.staged[-1]
        self.staged[-1].next = dest_node.next

        dest_node.next = self.staged[0]
        self.staged[0].prev = dest_node

        self.current = self.current.next
        self.staged = None
        self.staged_values = None
        self.check_rep()

    def result(self):
        start = self.lookup[1]
        el = start.next
        out = []
        while el is not start:
            out.append(el)
            el = el.next
        return "".join(str(n.value) for n in out)


inp = list(map(int, sys.stdin.read().strip()))
print(inp)
ll = LL(inp)
rounds = 100
for i in range(rounds + 1):
    ll.shuffle_round()
print("Part 1:", ll.result())

# ll = LL(inp)
# print("Part 2: creating LL")
# ll.update(tqdm(range(max(inp) + 1, 101)))
# rounds = 101
# print("Part 2: shuffling")
# for i in tqdm(range(rounds + 1)):
#     print(ll)
#     ll.shuffle_round()
