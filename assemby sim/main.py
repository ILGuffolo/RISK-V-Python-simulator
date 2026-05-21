'''
simulator envriomonet
'''

from cpu import CPU
import program_encoder as enc

def instruction_loader(cpu :CPU, instructions, debug = False):
    if debug : print("\nTraslation initialized")
    
    idx = 0
    for inst in instructions:
        inscode = enc.traslate(inst, debug)
        cpu.store_word(idx, inscode)
        idx += 4
        
    if debug : print("Tralsation finished\n")

def extract_code(filename):

    result = []

    with open(filename, "r") as f:

        for line in f:

            line = line.strip()

            if not line:
                continue

            if line.startswith("#"):
                continue

            result.append(line)

    return result

# ---------- MAIN --------- #

lines = extract_code("program.txt")

cpu = CPU()

instruction_loader(cpu, lines, True)

cpu.run_program(True)

print("registers value:")
print(cpu.regs)