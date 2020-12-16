from part1 import get_nth_number_spoken

def tests():
    for seq, exp in [
        ([0,3,6], 175594),
        ([1,3,2], 2578),
        ([2,1,3], 3544142),
        ([1,2,3], 261214),
        ([2,3,1], 6895259),
        ([3,2,1], 18),
        ([3,1,2], 362)
    ]:
        out = get_nth_number_spoken(seq, 30000000)
        print(seq, out, exp)
        assert out == exp

if __name__ == "__main__":
    tests()
    print(get_nth_number_spoken([0,6,1,7,2,19,20], 30000000))
