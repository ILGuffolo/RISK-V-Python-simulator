'''
traslate programs into bitstring

commands syntax

<comand> <input1>, <input2>, ...
'''
def tokenize(instr :str, debug = False): #tokenize intruction into arguments
    
    instr.lower()
    instr = substitute_alias(instr, aliases, debug)
    tokens = instr.split(',')
    command = tokens[0].split()
    tokens = command + tokens[1:]
    tokens = [t.strip() for t in tokens] 
    
    return tokens

def pack(value, start, length): #paks value into position (bitwise)
    mask = (1 << length) - 1
    return (value & mask) << start

def bits(value, start, length):
        mask = (1 << length) - 1
        return (value >> start) & mask
    
def substitute_alias(text, replacements, debug = False):
    
    keys = sorted(replacements.keys(), key=len, reverse=True) #sorted for non greedy approch
    
    for key in keys:
        text = text.replace(key, str(replacements[key]))
    
    if debug : print(text)
    return text

def encode_R(opcode, func3, func7, rd, rs1, rs2):
    
    instr = 0b0
    instr |= pack(opcode, 0, 7)
    instr |= pack(rd, 7, 5)
    instr |= pack(func3, 12, 3)
    instr |= pack(rs1, 15, 5)
    instr |= pack(rs2, 20, 5)
    instr |= pack(func7, 25, 7)
    
    return instr
            
def encode_I(opcode, func3, rd, rs1, imm):
    
    instr = 0b0
    instr |= pack(opcode, 0, 7)
    instr |= pack(rd, 7, 5)
    instr |= pack(func3, 12, 3)
    instr |= pack(rs1, 15, 5)
    instr |= pack(imm, 20, 12)
    
    return instr
        
def encode_S(opcode, func3, rs1, rs2, imm):
    
    instr = 0b0
    
    imm_low = bits(imm, 0, 5)
    imm_high = bits(imm, 5, 7)
    
    instr |= pack(opcode, 0, 7)
    instr |= pack(imm_low, 7, 5)
    instr |= pack(func3, 12, 3)
    instr |= pack(rs1, 15, 5)
    instr |= pack(rs2, 20, 5)
    instr |= pack(imm_high, 25, 7)
    
    return instr
        
def encode_B(opcode, func3, rs1, rs2, imm):
    
    instr = 0b0
    
    imm_low = bits(imm, 0, 4)
    imm_high = bits(imm, 4, 6)
    imm_11 = bits(imm, 10, 1)
    imm_12 = bits(imm, 11, 1)
    
    instr |= pack(opcode, 0, 7)
    instr |= pack(imm_11, 7, 1)
    instr |= pack(imm_low, 8, 4)
    instr |= pack(func3, 12, 3)
    instr |= pack(rs1, 15, 5)
    instr |= pack(rs2, 20, 5)
    instr |= pack(imm_high, 25, 6)
    instr |= pack(imm_12, 31, 1)
    
    return instr
            
def encode_U(opcode, rd, imm):
            pass
            
def encode_J(opcode, rd, imm):
    
    instr = 0b0
    
    imm_20   = (imm >> 20) & 1
    imm_high = (imm >> 12) & 0xFF
    imm_11   = (imm >> 11) & 1
    imm_low  = (imm >> 1) & 0x3FF
    
    instr |= pack(opcode, 0, 7)
    instr |= pack(rd, 7, 5)
    instr |= pack(imm_high, 12, 8)
    instr |= pack(imm_11, 20, 1)
    instr |= pack(imm_low, 21, 9)
    instr |= pack(imm_20, 30, 1)
          


aliases = {
    "zero" : "x0", # Constant 0
    "ra" : "x1",   # Return addres
    "sp" : "x2",   # Stack pointer
    "gp" : "x3",   # Global pointer
    "tp" : "x4",   # Thread pointer
    "t0" : "x5",   # Temporary
    "t1" : "x6",   # .
    "t2" : "x7",   # .
    "s0" : "x8", " fp " : " x8 ", # Saved (callee-served)
    "s1" : "x9",   # .
    "a0" : "x10",  # Function arguments
    "a1" : "x11",  # .
    "a2" : "x12",  # .
    "a3" : "x13",  # .
    "a4" : "x14",  # .
    "a5" : "x15",  # .
    "a6" : "x16",  # .
    "a7" : "x17",  # .
    "s2" : "x18",  # Saved (callee-served)
    "s3" : "x19",  # .
    "s4" : "x20",  # .
    "s5" : "x21",  # .
    "s6" : "x22",  # .
    "s7" : "x23",  # .
    "s8" : "x24",  # .
    "s9" : "x25",  # .
    "s10" : "x26", # .
    "s11" : "x27", # .
    "t3" : "x28",  # Temporary
    "t4" : "x29",  # .
    "t5" : "x30",  # .
    "t6" : "x31",  # .
        
    }
inverse_lookup = {v: k for k, v in aliases.items()}


def inverse_reg_conversion(idx):

    s = f"x{idx}"          # convert int to string with 'x' prefix
    converted = inverse_lookup.get(s, s)  # replace if found

    return converted

def traslate(line, debug = False): # --- TRANSLATOR --- #
    
    tokens = tokenize(line, debug)
    
    #register to index
    tokens = [tokens[0]] + [int(t.replace('x', '')) for t in tokens[1:]]
    
    instr = 0b0
    
    match tokens[0]:
        case "add": #ADD
            
            instr = encode_R(0b0110011,
                             0b000,
                             0b0000000,
                             tokens[1],
                             tokens[2],
                             tokens[3]
                             )

        
        case "sub": #SUB
            
            instr = encode_R(0b0110011,
                             0b000,
                             0b0110000,
                             tokens[1],
                             tokens[2],
                             tokens[3]
                             )
        
        case "addi": #ADDI
            
            instr = encode_I(0b0010011,
                             0b000,
                             tokens[1],
                             tokens[2],
                             tokens[3])
        
        case "lw": #LW
            
            instr = encode_I(0b0000011,
                             0b010,
                             tokens[1],
                             tokens[2],
                             tokens[3]
                             )
        
        case "sw": #SW
            
            encode_S(0b0100011,
                     0b010,
                     tokens[1],
                     tokens[2],
                     tokens[3]
                     )
        
        case "beq": #BEQ
            
            encode_B(0b1100011,
                     0b000,
                     tokens[1],
                     tokens[2],
                     tokens[3]
                     )
        
        case "bne": #BNE
            
            encode_B(0b1100011,
                     0b001,
                     tokens[1],
                     tokens[2],
                     tokens[3]
                     )
        
        case "jal": #JAL
            
            encode_J(0b1011111,
                     tokens[1],
                     tokens[2]
                     )
        
        case "jalr": #JALR
            
            rd = tokens[1]
            rs1 = tokens[2]
            imm = tokens[3]
            
            opcode = 0b1100111
            func3 =  0b000
            
            encode_I(0b1100111,
                     0b000,
                     tokens[1],
                     tokens[2],
                     tokens[3]
                     )
            
        case "ecall": #ECALL
            
            opcode = 0b1110011
            instr |= pack(opcode, 0, 7)
        
    #END MATCH-CASE
    
    return instr
        