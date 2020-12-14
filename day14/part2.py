import sys
import re

assign_pattern = re.compile(r"^mem\[(\d+)\] = (\d+)$")


def get_possible_addresses(addr, floating_mask, bits=36):
    if bits == 0:
        yield addr
    else:
        if floating_mask & 1:
            addr = addr & ~1
            for subaddr in get_possible_addresses(
                addr >> 1, floating_mask >> 1, bits=bits - 1
            ):
                yield (subaddr << 1) | 0
                yield (subaddr << 1) | 1
        else:
            for subaddr in get_possible_addresses(
                addr >> 1, floating_mask >> 1, bits=bits - 1
            ):
                yield (subaddr << 1) | (addr & 1)


memory = {}
for line in sys.stdin:
    line = line.strip()
    if line:
        m_assign = assign_pattern.match(line)
        if line.startswith("mask = "):
            floating_mask = 0
            replace_with = 0
            for c in line[len("mask = ") :]:
                if c == "1":
                    replace_with |= 1
                elif c == "X":
                    assert c == "X"
                    floating_mask |= 1
                else:
                    assert c == "0"
                replace_with <<= 1
                floating_mask <<= 1
            replace_with >>= 1
            floating_mask >>= 1
        elif m_assign:
            addr, value = map(int, m_assign.groups())
            addr |= replace_with
            addrs = set(get_possible_addresses(addr, floating_mask))
            # print(sorted(addrs), value)
            for addr in addrs:
                memory[addr] = value
                if value == 0:
                    del memory[addr]
        else:
            assert False
print(sum(memory.values()))
