'''
CPU class and instruction interpreter
'''

class CPU:
    def __init__(self, memory_size=1024 * 64):
        self.regs = [0] * 32
        self.pc = 0
        self.memory = bytearray(memory_size)
        
    def read_reg(self, idx):
        if idx == 0:
            return 0
        return self.regs[idx]
    
    def write_reg(self, idx, value):
        if idx != 0:
            self.regs[idx] = value & 0xFFFFFFFF
            
    def load_word(self, addr):
        b0 = self.memory[addr]
        b1 = self.memory[addr + 1]
        b2 = self.memory[addr + 2]
        b3 = self.memory[addr + 3]

        return ( b0 | (b1 << 8) | (b2 << 16) | (b3 << 24) )

    def store_word(self, addr, value):
        self.memory[addr    ] =  value        & 0xFF
        self.memory[addr + 1] = (value >> 8)  & 0xFF
        self.memory[addr + 2] = (value >> 16) & 0xFF
        self.memory[addr + 3] = (value >> 24) & 0xFF
        
    def fetch(self):
        
        return self.load_word(self.pc)
    
    def bits(self, value, start, length):
        mask = (1 << length) - 1
        return (value >> start) & mask
    
    def sign_extend(self, value, bit_len):
        if value & (1 << (bit_len - 1)):
            value -= 2**bit_len
        return value
    
    def run_cycle(self):
        instr = self.fetch()
        self.execute(instr)
        self.pc += 4
        
    def run_program(self):
        instr = self.fetch()
        
        while instr != 0:
            self.run_cycle()
            instr = self.fetch()
    
    def execute(self, instr): # --- INSTRUCTION SET --- #
        
        # constant
        opcode = self.bits(instr, 0, 7)
        rd     = self.bits(instr, 7, 5)
        funct3 = self.bits(instr, 12, 3)
        rs1    = self.bits(instr, 15, 5)
        rs2    = self.bits(instr, 20, 5)
        
        # R-type
        funct7 = self.bits(instr, 25, 7)
        
        #I-type
        Iimm = 0
        Iimm = self.bits(instr, 20, 12)
        Iimm = self.sign_extend(Iimm, 12)
        
        #S-type
        Simm = 0
        Simm = (self.bits(instr, 25, 7) << 5) | self.bits(instr, 7, 5)
        Simm = self.sign_extend(Simm, 12)
        
        #B-type
        Bimm = 0
        Bimm = (self.bits(instr, 31, 1) << 12) | (self.bits(instr, 7, 1) << 11) | (self.bits(instr, 25, 6) << 5) | (self.bits(instr, 8, 4) << 1)
        Bimm = self.sign_extend(Bimm, 13)
        
        #U-type
           #to do
        
        #J-type
        Jimm = 0
        Jimm = (self.bits(instr, 31, 1) << 20) | (self.bits(instr, 12, 8) << 12) | (self.bits(instr, 20, 1) << 11) | (self.bits(instr, 21, 10) << 1)   
        Jimm = self.sign_extend(Jimm, 20)
        
        # instructions
        if (opcode == 0b0110011 and
            funct3 == 0b000 and
            funct7 == 0b000000): #ADD
            
            print(f"debug: add {rd}, {rs1}, {rs2}")
            
            a = self.read_reg(rs1)
            b = self.read_reg(rs2)

            self.write_reg(rd, a + b)
            
        elif (opcode == 0b0110011 and
              funct3 == 0b000 and
              funct7 == 0b010000): #SUB
            
            print(f"debug: sub {rd}, {rs1}, {rs2}")
            
            a = self.read_reg(rs1)
            b = self.read_reg(rs2)

            self.write_reg(rd, a - b)
        
        elif (opcode == 0b0010011 and
              funct3 == 0b000): #ADDI
            
            print(f"debug: addi {rd}, {rs1}, {Iimm}")
            
            a = self.read_reg(rs1)

            self.write_reg(rd, a + Iimm)
            
        elif (opcode == 0b0000011 and
              funct3 == 0b010): #LW
            
            print(f"debug: lw {rd}, {rs1}, {Iimm}")
            
            r = self.read_reg(rs1)
            
            self.write_reg(rd, self.load_word(r + Iimm))
            
            
        elif (opcode == 0b0100011 and
              funct3 == 0b010): #SW
            
            print(f"debug: sw {rs1}, {rs2}, {Simm}")
            
            r = self.read_reg(rs1)
            self.store_word(r + Simm, self.read_reg(rs2))
            
            
        elif (opcode == 0b1100011 and
              funct3 == 0b000): #BEQ
            
            print(f"debug: beq {rs1}, {rs2}, {Bimm}")
            
            a = self.read_reg(rs1)
            b = self.read_reg(rs2)
            
            if a == b:
                self.pc += Bimm
            
        elif (opcode == 0b1100011 and
              funct3 == 0b001): #BNE
            
            print(f"debug: bne {rs1}, {rs2}, {Bimm}")
            
            a = self.read_reg(rs1)
            b = self.read_reg(rs2)
            
            if a != b:
                self.pc += Bimm -4 #accounting for fde cycle
            
        elif (opcode == 0b1011111): #JAL
            
            print(f"debug: jal {rd}, {Jimm}")
            
            self.write_reg(rd, self.pc + 4)
            self.pc += Jimm -4 #accounting for fde cycle
            
        elif (opcode == 0b1100111 and
              funct3 == 0b000): #JALR
            
            print(f"debug: jalr {rd}, {rs1}, {Iimm}")
            
            self.write_reg(rd, self.pc + 4)
            r = self.read_reg(rs1)
            self.pc += r + Iimm -4 #accounting for fde cycle
            
        else:
            print("debug: unrecognized instruction")
                
    
