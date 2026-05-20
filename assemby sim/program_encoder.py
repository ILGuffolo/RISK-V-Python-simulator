'''
traslate programs into bitstring

commands syntax

<comand> <input1>, <input2>, ...
'''
def tokenize(instr :str): #tokenize intruction into arguments
    
    instr.lower()
    tokens = instr.split(',')
    command = tokens[0].split()
    tokens = command + tokens[1:]
    tokens = [t.strip() for t in tokens] 
    
    return tokens

def pack(value, start, length): #paks value into position bitwise
    mask = (1 << length) - 1
    return (value & mask) << start

def bits(value, start, length):
        mask = (1 << length) - 1
        return (value >> start) & mask
    

def traslate(line): # --- TRANSLATOR --- #
    
    tokens = tokenize(line)
    
    #register to index
    tokens = [tokens[0]] + [int(t.strip('x')) for t in tokens[1:]]
    
    instr = 0b0
    
    match tokens[0]:
        case "add": #ADD
            rd = tokens[1]
            rs1 = tokens[2]
            rs2 = tokens[3]
            
            opcode = 0b0110011
            func3 =  0b000
            func7 =  0b0000000
            
            instr |= pack(opcode, 0, 7)
            instr |= pack(rd, 7, 5)
            instr |= pack(func3, 12, 3)
            instr |= pack(rs1, 15, 5)
            instr |= pack(rs2, 20, 5)
            instr |= pack(func7, 25, 7)

        
        case "sub": #SUB
            
            rd = tokens[1]
            rs1 = tokens[2]
            rs2 = tokens[3]
            
            opcode = 0b0110011
            func3 =  0b000
            func7 =  0b0110000
            
            instr |= pack(opcode, 0, 7)
            instr |= pack(rd, 7, 5)
            instr |= pack(func3, 12, 3)
            instr |= pack(rs1, 15, 5)
            instr |= pack(rs2, 20, 5)
            instr |= pack(func7, 25, 7)
        
        case "addi": #ADDI
            
            rd = tokens[1]
            rs1 = tokens[2]
            imm = tokens[3]
            
            opcode = 0b0010011
            func3 =  0b000
            
            instr |= pack(opcode, 0, 7)
            instr |= pack(rd, 7, 5)
            instr |= pack(func3, 12, 3)
            instr |= pack(rs1, 15, 5)
            instr |= pack(imm, 20, 12)
        
        case "lw": #LW
            
            rd = tokens[1]
            rs1 = tokens[2]
            imm = tokens[3]
            
            opcode = 0b0000011
            func3 =  0b010
            
            instr |= pack(opcode, 0, 7)
            instr |= pack(rd, 7, 5)
            instr |= pack(func3, 12, 3)
            instr |= pack(rs1, 15, 5)
            instr |= pack(imm, 20, 12)
        
        case "sw": #SW
            
            rs1 = tokens[1]
            rs2 = tokens[2]
            imm = tokens[3]
            
            opcode = 0b0100011
            func3 =  0b010
            
            imm_low = bits(imm, 0, 5)
            imm_high = bits(imm, 5, 7)
            
            instr |= pack(opcode, 0, 7)
            instr |= pack(imm_low, 7, 5)
            instr |= pack(func3, 12, 3)
            instr |= pack(rs1, 15, 5)
            instr |= pack(rs2, 20, 5)
            instr |= pack(imm_high, 25, 7)
        
        case "beq": #BEQ
            
            rs1 = tokens[1]
            rs2 = tokens[2]
            imm = tokens[3]
            
            opcode = 0b1100011
            func3 =  0b000
            
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
        
        case "bne": #BNE
            
            rs1 = tokens[1]
            rs2 = tokens[2]
            imm = tokens[3]
            
            opcode = 0b1100011
            func3 =  0b001
            
            imm_12   = (imm >> 12) & 1
            imm_11   = (imm >> 11) & 1
            imm_high = (imm >> 5)  & 0b111111
            imm_low  = (imm >> 1)  & 0b1111
            
            instr |= pack(opcode, 0, 7)
            instr |= pack(imm_11, 7, 1)
            instr |= pack(imm_low, 8, 4)
            instr |= pack(func3, 12, 3)
            instr |= pack(rs1, 15, 5)
            instr |= pack(rs2, 20, 5)
            instr |= pack(imm_high, 25, 6)
            instr |= pack(imm_12, 31, 1)
        
        case "jal": #JAL
            
            rd = tokens[1]
            imm = tokens[2]
            
            opcode = 0b1011111
            
            imm_20    = (imm >> 20) & 1
            imm_high = (imm >> 12) & 0xFF
            imm_11    = (imm >> 11) & 1
            imm_low  = (imm >> 1) & 0x3FF
            
            instr |= pack(opcode, 0, 7)
            instr |= pack(rd, 7, 5)
            instr |= pack(imm_high, 12, 8)
            instr |= pack(imm_11, 20, 1)
            instr |= pack(imm_low, 21, 9)
            instr |= pack(imm_20, 30, 1)
        
        case "jalr": #JALR
            
            rd = tokens[1]
            rs1 = tokens[2]
            imm = tokens[3]
            
            opcode = 0b1100111
            func3 =  0b000
            
            instr |= pack(opcode, 0, 7)
            instr |= pack(rd, 7, 5)
            instr |= pack(func3, 12, 3)
            instr |= pack(rs1, 15, 5)
            instr |= pack(imm, 20, 12)
        
    #END MATCH-CASE
    
    return instr
        