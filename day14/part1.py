import sys
import re

assign_pattern = re.compile(r"^mem\[(\d+)\] = (\d+)$")

keep_mask = 1 << 36 - 1
replace_with = 0
memory = {}
for line in sys.stdin:
    line = line.strip()
    if line:
        m_assign = assign_pattern.match(line)
        if line.startswith("mask = "):
            keep_mask = 0
            replace_with = 0
            for c in line[len("mask = ") :]:
                if c == "X":
                    keep_mask |= 1
                elif c == "1":
                    replace_with |= 1
                else:
                    assert c == "0"
                keep_mask <<= 1
                replace_with <<= 1
            keep_mask >>= 1
            replace_with >>= 1
        elif m_assign:
            addr, value = map(int, m_assign.groups())
            value = (value & keep_mask) | replace_with
            memory[addr] = value
            if value == 0:
                del memory[addr]
        else:
            assert False
print(sum(memory.values()))
