import sys
from computer import Program, Computer

if __name__ == "__main__":
    base_program = [line for line in (line.strip() for line in sys.stdin) if line]
    for i in range(len(base_program)):
        if base_program[i].startswith("nop"):
            repl = base_program[i].replace("nop", "jmp")
        elif base_program[i].startswith("jmp"):
            repl = base_program[i].replace("jmp", "nop")
        else:
            continue
        program = list(base_program)
        program[i] = repl
        program = Program.parse_from_lines(program)

        computer = Computer().load_program(program)
        seen_pcs = set()

        while computer.pc not in seen_pcs and computer.pc != len(program.ops):
            seen_pcs.add(computer.pc)
            computer.execute_next_op()
        if computer.pc == len(program.ops):
            print(computer.accumulator)
            break
