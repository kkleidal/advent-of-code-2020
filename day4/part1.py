import sys

def load_passports(fileobj):
    kvps = {}
    for line in fileobj:
        line = line.strip()
        if line == "":
            yield kvps
            kvps = {}
        else:
            parts = line.split(" ")
            for part in parts:
                key, value = part.split(":")
                kvps[key] = value
    if len(kvps) > 0:
        yield kvps

required_fields = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}
def is_passport_valid(passport):
    return required_fields.issubset(set(passport.keys()))

def count_true(lst):
    return sum(1 if x else 0 for x in lst)

def main(is_passport_valid=is_passport_valid):
    passports = load_passports(sys.stdin)
    passport_is_valid = map(is_passport_valid, passports)
    number_valid = count_true(passport_is_valid)
    print(number_valid)

if __name__ == "__main__":
    main()
