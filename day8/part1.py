import sys
from computer import Program, Computer

if __name__ == "__main__":
    program = Program.load_from_file(sys.stdin)
    computer = Computer().load_program(program)
    seen_pcs = set()
    while computer.pc not in seen_pcs:
        seen_pcs.add(computer.pc)
        computer.execute_next_op()
    print(computer.accumulator)
