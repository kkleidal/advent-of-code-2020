import sys


def main():
    input_values = []
    for line in sys.stdin:
        input_values.append(int(line.strip()))

    for i in input_values:
        for j in input_values:
            for k in input_values:
                if i + j + k == 2020:
                    print(i * j * k)
                    return


if __name__ == "__main__":
    main()
