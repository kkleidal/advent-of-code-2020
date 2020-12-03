import sys

def main():
    input_values = []
    for line in sys.stdin:
        input_values.append(int(line.strip()))

    for i in input_values:
        for j in input_values:
            if i + j == 2020:
                print(i * j)
                return

if __name__ == "__main__":
    main()
