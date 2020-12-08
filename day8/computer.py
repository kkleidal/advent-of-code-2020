from abc import ABC, abstractmethod
from typing import List, NamedTuple


class Computer:
    def __init__(self):
        self.program = None
        self.reset()

    def load_program(self, program):
        self.program = program
        return self

    def reset(self):
        self.pc = 0
        self.accumulator = 0

    @property
    def current_op(self) -> "Op":
        return self.program.ops[self.pc]

    def jump_abs(self, i):
        self.pc = i
        return self

    def jump_rel(self, i):
        self.pc += i
        return self

    def jump_next(self):
        self.pc += 1
        return self

    def execute_next_op(self):
        self.program.ops[self.pc].execute(self)

    @property
    def state(self):
        return State(pc=self.pc, accumulator=self.accumulator)


class State(NamedTuple):
    pc: int
    accumulator: int


class Program:
    def __init__(self, ops):
        self.ops = ops

    @classmethod
    def load_from_file(cls, fileobj):
        return cls.parse_from_lines(fileobj)

    @classmethod
    def parse_from_lines(cls, lines):
        ops = []
        for line in lines:
            ops.extend(cls._parse_line(line))
        return Program(ops)

    @classmethod
    def _parse_line(cls, line):
        line = line.strip()
        if line:
            args = line.split(" ")
            op_name = args[0]
            op_args = args[1:]
            op = ops[op_name].parse(op_args)
            yield op


ops = {}


def register_op(name):
    def wrap(cls):
        ops[name] = cls
        return cls

    return wrap


class Op(ABC):
    @classmethod
    @abstractmethod
    def parse(cls, args: List[str]):
        ...

    @abstractmethod
    def execute(self, computer: Computer):
        ...


class SingleIntOp(Op):
    def __init__(self, amount: int):
        self.amount = amount

    @classmethod
    def parse(cls, args: List[str]):
        return cls(int(args[0]))


@register_op("nop")
class Nop(SingleIntOp):
    def execute(self, computer: Computer):
        computer.jump_next()


@register_op("acc")
class Acc(SingleIntOp):
    def execute(self, computer: Computer):
        computer.accumulator += self.amount
        computer.jump_next()


@register_op("jmp")
class Jmp(SingleIntOp):
    def execute(self, computer: Computer):
        computer.jump_rel(self.amount)
