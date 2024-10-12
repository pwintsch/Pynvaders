from pathlib import Path

import numpy as np


class Processor:     
    def __init__(self):
        self.memory=np.zeros(65536,dtype=np.uint8)
        self.programSize=0
        self.pc=0
        self.InitialiseFuncMap()
        self.cycle=0

    
    def load(self, start, program):
        myFileName=program
        myFile=Path(myFileName)
        if myFile.exists() and myFile.is_file():
            rawData=myFile.read_bytes()
            self.programSize=self.programSize+len(rawData)
            for i in range(len(rawData)):
                self.memory[i+start]=rawData[i]
            return True
        else:
            return False


    def fetch(self):
        op= int(self.memory[self.pc])
        opCode=format(self.pc,"06")+ " - " + format(op, "02X") + " - "
        found=True
        if op in self.funcMap:
            opCode=opCode + self.funcMap[op]()
        else:
            opCode=opCode + "NOT YET IMPLEMENTED"
            found=False
            
        return opCode, found
    

    def InitialiseFuncMap(self):
        self.funcMap = {
            0x00: self.NOP,
            0x0F: self.RRC,
            0x21: self.LXIH,
            0x27: self.DAA,
            0x32: self.STA,
            0x35: self.DECHL,
            0x3A: self.LDA,
            0x3E: self.MVI,
            0xA7: self.ANDA,
            0xAF: self.XORA,
            0xC2: self.JPNZ,
            0xC3: self.JMP,
            0xCA: self.JPZ,
            0xC5: self.PUSHB,
            0xC6: self.ADDA,
            0xCD: self.CALL,
            0xD5: self.PUSHD,
            0xDA: self.JPC,
            0xDB: self.IN,
            0xE1: self.POPH,
            0xE5: self.PUSHH,
            0xF0: self.RETP,
            0xF5: self.PUSHPSW,
            0xFE: self.CP }
        
    def NOP(self):
        self.pc=self.pc+1
        self.cycle=self.cycle+4
        return "NOP"
    
    def RRC(self):
        self.pc=self.pc+1
        self.cycle=self.cycle+4
        return "RRCA"
    
    def LXIH(self):
        self.pc=self.pc+3
        self.cycle=self.cycle+10
        regValue=int(self.memory[self.pc-1])+int(self.memory[self.pc-2])*256
        return "LD HL, " + format(regValue, "04X")

    def DAA(self):
        self.pc=self.pc+1
        self.cycle=self.cycle+4
        return "DAA"
    
    def STA(self):
        self.pc=self.pc+3
        self.cycle=self.cycle+13
        address=int(self.memory[self.pc-2])+int(self.memory[self.pc-1])*256
        return "LD " + format(address, "04X") + ", A"

    def DECHL(self):
        self.pc=self.pc+1
        self.cycle=self.cycle+5
        return "DEC (HL)"

    def LDA(self):
        self.pc=self.pc+3
        self.cycle=self.cycle+13
        address=int(self.memory[self.pc-2])+int(self.memory[self.pc-1])*256
        return "LD A, (" + format(address, "04X") + ")"
    
    def MVI(self):
        self.pc=self.pc+2
        self.cycle=self.cycle+7
        regValue=self.memory[self.pc-1]
        return "LD A, " + format(regValue, "02X")
    
    def ANDA(self):
        self.pc=self.pc+1
        self.cycle=self.cycle+4
        return "AND A"
    
    def XORA(self):
        self.pc=self.pc+1
        self.cycle=self.cycle+4
        return "XOR A"
    
    def JPNZ(self):
        self.pc=self.pc+3
        self.cycle=self.cycle+10
        address=int(self.memory[self.pc-2])+int(self.memory[self.pc-1])*256
        return "JP NZ, " + format(address, "04X")

    def JMP(self):
        self.pc=self.pc+3
        self.cycle=self.cycle+10
        address=int(self.memory[self.pc-2])+int(self.memory[self.pc-1])*256
        return "JMP " + format(address, "04X")
    
    def JPZ(self):
        self.pc=self.pc+3
        self.cycle=self.cycle+10
        address=int(self.memory[self.pc-2])+int(self.memory[self.pc-1])*256
        return "JP Z, " + format(address, "04X")
    
    def PUSHB(self):
        self.pc=self.pc+1
        self.cycle=self.cycle+11
        return "PUSH BC"

    def ADDA(self):
        self.pc=self.pc+2
        self.cycle=self.cycle+7
        value=self.memory[self.pc-1]
        return "ADD A, " + format(value, "02X")
    
    def CALL(self):
        self.pc=self.pc+3
        self.cycle=self.cycle+17
        address=int(self.memory[self.pc-2])+int(self.memory[self.pc-1])*256
        return "CALL " + format(address, "04X")
        
    def PUSHD(self):
        self.pc=self.pc+1
        self.cycle=self.cycle+11
        return "PUSH DE"
    
    def JPC(self):
        self.pc=self.pc+3
        self.cycle=self.cycle+10
        address=int(self.memory[self.pc-2])+int(self.memory[self.pc-1])*256
        return "JP C, " + format(address, "04X")

    def IN(self):
        self.pc=self.pc+2
        self.cycle=self.cycle+10
        value=self.memory[self.pc-1]
        return "IN A,(" + format(value, "02X") + ")"

    def POPH(self):
        self.pc=self.pc+1
        self.cycle=self.cycle+10
        return "POP HL"

    def PUSHH(self):
        self.pc=self.pc+1
        self.cycle=self.cycle+11
        return "PUSH HL"
    
    def RETP(self):
        self.pc=self.pc+1
        self.cycle=self.cycle+11        # 5 or 11 depending on execution
        return "RET P"

    def PUSHPSW(self):
        self.pc=self.pc+1
        self.cycle=self.cycle+11
        return "PUSH PSW"
    
    def CP(self):
        self.pc=self.pc+2
        self.cycle=self.cycle+7
        value=self.memory[self.pc-1]
        return "CP " + format(value, "02X")




            
def main():

    proc=Processor()    
    if proc.load (0, './rom/invaders.h'):
        if proc.load (0x800, './rom/invaders.g'):
            if proc.load (0x1000, './rom/invaders.f'):
                if proc.load (0x1800, './rom/invaders.e'):
                    print ("ROMs loaded")
                else:
                    print ("Problem with invaders.e")
            else:
                print ("Problem with invaders.f")
        else:
            print ("Problem with invaders.g")
    else:
        print ("Problem with invaders.h")
    program=[]
    instuctionFound=True
    while instuctionFound:
        instr, instuctionFound=proc.fetch()
        program.append(instr)

    outputFile=open("Pynvader_Disassembler.txt","w")
    for x in range(len(program)):
        outputText = program[x] + "\n"
        outputFile.write(outputText)
        print (program[x])
    outputFile.close()
    print ("File written") 




print ("Hi this is Pyn_dis.py, a dissasembler in Python of the Space Invaders MAME ROMs")
if __name__ == "__main__":
    main()