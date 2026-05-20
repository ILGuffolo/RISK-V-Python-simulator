# RISK-V-Python-simulator
a small project, simulating a RV32I architecture on python

# Instruction
write the code with any tool you like and paste it into the "assembly sim" folder as "program.txt" then execute main.py

# Coming updates
completing instruction set

ecalls to read and print to/from terminal

global variables

stack

optimizzation

QoL

# Current supported commands

(r) -> value in register r
m[i] -> memory at index i

add rd rs1 rs2 : (rd) = (rs1) + (rs2)

sub rd rs1 rs2 : (rd) = (rs1) - (rs2)

addi rd rs1 imm : (rd) = (rs1) + (imm)

lw rd rs1 imm : (rd) = M[rs1 + imm]

sw rs1 rs2 : M[rs1 + imm] = (rs2)

beq rs1 rs2 imm : if rs1 == rs2: pc += imm

beq rs1 rs2 imm : if rs1 != rs2: pc += imm

jal rd imm : (rd) = pc + 4; pc += imm

jalr rd rs1 imm : (rd) = pc + 4; pc += (rs1) + imm

# Aliases
registers: {
    " zero " : " x0 ", # Constant 0
    " ra " : " x1 ",   # Return addres
    " sp " : " x2 ",   # Stack pointer
    " gp " : " x3 ",   # Global pointer
    " tp " : " x4 ",   # Thread pointer
    " t0 " : " x5 ",   # Temporary
    " t1 " : " x6 ",   # .
    " t2 " : " x7 ",   # .
    " s0 " : " x8 ", " fp " : " x8 ", # Saved (callee-served)
    " s1 " : " x9 ",   # .
    " a0 " : " x10 ",  # Function arguments
    " a1 " : " x11 ",  # .
    " a2 " : " x12 ",  # .
    " a3 " : " x13 ",  # .
    " a4 " : " x14 ",  # .
    " a5 " : " x15 ",  # .
    " a6 " : " x16 ",  # .
    " a7 " : " x17 ",  # .
    " s2 " : " x18 ",  # Saved (callee-served)
    " s3 " : " x19 ",  # .
    " s4 " : " x20 ",  # .
    " s5 " : " x21 ",  # .
    " s6 " : " x22 ",  # .
    " s7 " : " x23 ",  # .
    " s8 " : " x24 ",  # .
    " s9 " : " x25 ",  # .
    " s10 " : " x26 ", # .
    " s11 " : " x27 ", # .
    " t3 " : " x28 ",  # Temporary
    " t4 " : " x29 ",  # .
    " t5 " : " x30 ",  # .
    " t6 " : " x31 ",  # .
    
    
    }
