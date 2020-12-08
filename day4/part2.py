import re
from abc import ABC, abstractmethod
from part1 import main, is_passport_valid as old_is_passport_valid


class Rule(ABC):
    @abstractmethod
    def accepts(self, ctx, value: str) -> bool:
        ...


class MatchesRegex(Rule):
    def __init__(self, pattern: str):
        self.__pattern = re.compile(pattern)

    def accepts(self, ctx, value: str) -> bool:
        m = self.__pattern.match(value)
        ctx.pattern_match = m
        return m is not None


class InRange(Rule):
    def __init__(self, low, high):
        self.low = low
        self.high = high

    def accepts(self, ctx, value: str) -> bool:
        return self.low <= int(value) <= self.high


class CustomHeightRule(Rule):
    def accepts(self, ctx, value: str) -> bool:
        hgt, unit = ctx.pattern_match.groups()
        hgt = int(hgt)
        if unit == "in" and not (59 <= hgt <= 76):
            return False
        if unit == "cm" and not (150 <= hgt <= 193):
            return False
        return True


year_is_valid = MatchesRegex("^\d{4}$")
rules = {
    "byr": [year_is_valid, InRange(1920, 2002)],
    "iyr": [year_is_valid, InRange(2010, 2020)],
    "eyr": [year_is_valid, InRange(2020, 2030)],
    "hgt": [MatchesRegex("^(\d{2,3})(in|cm)$"), CustomHeightRule()],
    "hcl": [MatchesRegex("^#[a-f0-9]{6}$")],
    "ecl": [MatchesRegex("^(amb|blu|brn|gry|grn|hzl|oth)$")],
    "pid": [MatchesRegex("^\d{9}$")],
}


class Ctx:
    ...


def is_passport_valid(passport):
    if not old_is_passport_valid(passport):
        return False
    for key, value in passport.items():
        ctx = Ctx()
        for rule in rules.get(key, []):
            if not rule.accepts(ctx, value):
                return False
    return True


def invert(fn):
    def wrapped(*args, **kwargs):
        return not fn(*args, **kwargs)

    return wrapped


if __name__ == "__main__":
    main(is_passport_valid)
