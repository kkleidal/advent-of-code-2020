def get_nth_number_spoken(seq, n):
    memory = {}

    t = 0
    last_spoken = None

    def speak(x):
        nonlocal last_spoken
        if x not in memory:
            memory[x] = t
        ago = t - memory[x]
        # print(f"{x} was spoken {ago} timesteps ago")
        memory[x] = t
        last_spoken = x
        return ago

    while t < n:
        if t < len(seq):
            last_time_spoken = speak(seq[t])
        else:
            last_time_spoken = speak(last_time_spoken)
        t += 1
    return last_spoken

def tests():
    for seq, exp in [
        ([0,3,6], 436),
        ([1,3,2], 1),
        ([2,1,3], 10),
        ([1,2,3], 27),
        ([2,3,1], 78),
        ([3,2,1], 438),
        ([3,1,2], 1836)
    ]:
        out = get_nth_number_spoken(seq, 2020)
        print(seq, out, exp)
        assert out == exp

if __name__ == "__main__":
    tests()
    print(get_nth_number_spoken([0,6,1,7,2,19,20], 2020))
