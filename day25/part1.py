def get_loop_size(subject_number, result):
    loop_size = 1
    value = subject_number
    while value != result:
        value = (value * subject_number) % 20201227
        loop_size += 1
    return loop_size


def transform(subject_number, loop):
    value = subject_number
    for _ in range(loop - 1):
        value = (value * subject_number) % 20201227
    return value


def reverse_pk(pk):
    return get_loop_size(7, pk)


def get_encryption(pk1, pk2):
    loop = reverse_pk(pk1)
    enc = transform(pk2, loop)
    return enc


# print(reverse_pk(5764801))
# print(reverse_pk(17807724))
# print("Part 1 (example):", get_encryption(5764801, 17807724))
print("Part 1:", get_encryption(10212254, 12577395))
