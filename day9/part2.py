import sys


def cumsum(x):
    summ = 0
    yield summ
    for y in x:
        summ += y
        yield summ


target_number = 556543474
inputs = [int(x) for x in sys.stdin]
sums = list(cumsum(inputs))
for i in range(0, len(sums) - 1):
    for j in range(i + 2, len(inputs) + 1):
        c = sums[j] - sums[i]
        # assert c == sum(inputs[i:j])
        if c == target_number:
            print(min(inputs[i:j]) + max(inputs[i:j]))
            break
