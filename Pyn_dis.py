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
        opCode=format(self.pc,"04X")+ " - " + format(op, "02X") + " - "
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
            0x01: self.LDBCnn,
            0x04: self.INCB,
            0x05: self.DECB,
            0X06: self.LDB,
            0X07: self.RLCA,
            0x0D: self.DECC,
            0x0E: self.LDC,
            0x0F: self.RRCA,
            0x11: self.LDDEnn,
            0x13: self.INCDE,
            0x14: self.INCD,
            0x15: self.DECD,
            0x16: self.LDD,
            0x19: self.ADDHLDE,
            0x1A: self.LDADE,
            0x21: self.LXIH,                # Z80 LD HL, Val
            0x22: self.SHLD,                #
            0x23: self.INCHL,
            0x26: self.LDHn,                # Z80 LD H, Val
            0x27: self.DAA,
            0x29: self.ADDHLHL,
            0X2A: self.LDHL,                # Z80 LD HL,(addr)
            0x2B: self.DECHL,
            0x2C: self.INCL,
            0x2E: self.LDL,                # Z80 LD L, Val
            0x31: self.LDSPnn,
            0x32: self.STA,
            0x34: self.INCatHL,
            0x35: self.DECatHL,
            0x36: self.LDIHL,
            0x37: self.SCF,
            0x3A: self.LDA,
            0x3C: self.INCA,
            0x3D: self.DECA,
            0x3E: self.MVI,
            0x44: self.LDBH,
            0x46: self.LDBHL,
            0x47: self.LDBA,
            0x4E: self.LDCHL,
            0x4F: self.LDCA,
            0x53: self.LDDE,
            0x56: self.LDDHL,
            0x5E: self.LDEHL,
            0x5F: self.LDEA,
            0x61: self.LDHC,
            0x66: self.LDHHL,
            0x67: self.LDHA,
            0x68: self.LDLB,
            0x69: self.LDLC,
            0x6F: self.LDLA,
            0x70: self.LDHLB,
            0x71: self.LDHLC,
            0x72: self.LDHLD,
            0x73: self.LDHLE,
            0x77: self.LDHLA,
            0x78: self.LDAB,
            0x79: self.LDAC,
            0x7A: self.LDAD,
            0x7B: self.LDAE,
            0x7C: self.LDAH,
            0x7D: self.LDAL,
            0x7E: self.LDAHL,
            0x80: self.ADDAB,
            0x85: self.ADDAL,
            0x86: self.ADDAHL,
            0x97: self.SUBA,
            0xA0: self.ANDB,
            0xA7: self.ANDA,
            0xAF: self.XORA,
            0xB0: self.ORB,
            0xB4: self.ORE,
            0xB8: self.CPB,
            0xBE: self.CPHL,
            0xC0: self.RETNZ,
            0xC1: self.POPB,
            0xC2: self.JPNZ,
            0xC3: self.JMP,
            0xC4: self.CALLNZ,
            0xCA: self.JPZ,
            0xC5: self.PUSHB,
            0xC6: self.ADDA,
            0xC8: self.RETZ,
            0xC9: self.RET,
            0xCC: self.CALLZ,
            0xCD: self.CALL,
            0xD0: self.RETNC,
            0xD1: self.POPD,
            0xD2: self.JPNC,
            0xD3: self.OUTnnA,
            0xD5: self.PUSHD,
            0xD6: self.SUBV,   
            0xDA: self.JPC,
            0xDB: self.IN,
            0xDE: self.SBCA,
            0xE1: self.POPH,
            0xE3: self.JPnn,
            0xE5: self.PUSHH,
            0XE6: self.ANDV,
            0XEB: self.EXDEHL,
            0xF0: self.RETP,
            0xF1: self.POPPSW,
            0xF5: self.PUSHPSW,
            0xF6: self.ORV,
            0xFA: self.JPM,
            0xFB: self.EI,
            0xFE: self.CP }
        
    def NOP(self):
        #OpCode 00
        self.pc=self.pc+1
        self.cycle=self.cycle+4
        return "NOP"
    
    def LDBCnn(self):
        #OpCode 01
        self.pc=self.pc+3
        self.cycle=self.cycle+10
        regValue=int(self.memory[self.pc-1])+int(self.memory[self.pc-2])*256
        return "LD BC, " + format(regValue, "04X")
    
    def INCB(self):
        #OpCode 04
        self.pc=self.pc+1
        self.cycle=self.cycle+4
        return "INC B"

    def DECB(self):
        #OpCode 05
        self.pc=self.pc+1
        self.cycle=self.cycle+4
        return "DEC B"
    
    def LDB(self):
        self.pc=self.pc+2
        self.cycle=self.cycle+7
        regValue=self.memory[self.pc-1]
        return "LD B, " + format(regValue, "02X")
    
    def RLCA(self):
        #OpCode 07
        self.pc=self.pc+1
        self.cycle=self.cycle+4
        return "RLCA"
    
    def DECC(self):
        #OpCode 0D
        self.pc=self.pc+1
        self.cycle=self.cycle+4
        return "DEC C"

    def LDC(self):
        #OpCode 0E
        self.pc=self.pc+2
        self.cycle=self.cycle+7
        regValue=self.memory[self.pc-1]
        return "LD C, " + format(regValue, "02X")

    def RRCA(self):
        #OpCode 0F
        self.pc=self.pc+1
        self.cycle=self.cycle+4
        return "RRCA"
    
    def LDDEnn(self):
        #OpCode 11
        self.pc=self.pc+3
        self.cycle=self.cycle+10
        regValue=int(self.memory[self.pc-1])+int(self.memory[self.pc-2])*256
        return "LD DE, " + format(regValue, "04X")

    def INCDE(self):
        #OpCode 13
        self.pc=self.pc+1
        self.cycle=self.cycle+6
        return "INC DE"
    
    def INCD(self):
        #OpCode 14
        self.pc=self.pc+1
        self.cycle=self.cycle+4  #8080 has 5 cycles, 8085 has 4, z80 has 4
        return "INC D"
    
    def DECD(self):
        self.pc=self.pc+1
        self.cycle=self.cycle+4
        return "DEC D"
    
    def LDD(self):
        self.pc=self.pc+2
        self.cycle=self.cycle+7
        regValue=self.memory[self.pc-1]
        return "LD D, " + format(regValue, "02X")
    
    def ADDHLDE(self):
        #OpCode 19
        self.pc=self.pc+1
        self.cycle=self.cycle+11
        return "ADD HL, DE"

    def LDADE(self):
        #OpCode 1A
        self.pc=self.pc+1
        self.cycle=self.cycle+7
        return "LD A, (DE)"
     
    def LXIH(self):
        #OpCode 21
        self.pc=self.pc+3
        self.cycle=self.cycle+10
        regValue=int(self.memory[self.pc-2])+int(self.memory[self.pc-1])*256
        return "LD HL, " + format(regValue, "04X")
    
    def SHLD(self):
        self.pc=self.pc+3
        self.cycle=self.cycle+16
        address=int(self.memory[self.pc-2])+int(self.memory[self.pc-1])*256
        return "LD (" + format(address, "04X") + "), HL"
    
    def INCHL(self):
        self.pc=self.pc+1
        self.cycle=self.cycle+6    #8080 has 5 cycles, 8085 has 6, z80 has 6
        return "INC (HL)"

    def LDHn(self):
        #OpCode 26
        self.pc=self.pc+2
        self.cycle=self.cycle+7
        regValue=self.memory[self.pc-1]
        return "LD H, " + format(regValue, "02X")
    
    def DAA(self):
        #OpCode 27
        self.pc=self.pc+1
        self.cycle=self.cycle+4
        return "DAA"
    
    def ADDHLHL(self):
        #OpCode 29
        self.pc=self.pc+1
        self.cycle=self.cycle+11
        return "ADD HL, HL"
    
    def LDHL(self):
        #OpCode 2A
        self.pc=self.pc+3
        self.cycle=self.cycle+16
        address=int(self.memory[self.pc-2])+int(self.memory[self.pc-1])*256
        return "LD HL, (" + format(address, "04X") + ")"
    
    def DECHL(self):
        #OpCode 2B
        self.pc=self.pc+1
        self.cycle=self.cycle+6   #8080 has 5 cycles, 8085 has 6, z80 has 6
        return "DEC (HL)"
    
    def INCL(self):
        #OpCode 2C
        self.pc=self.pc+1
        self.cycle=self.cycle+6
        return "INC L"
    
    def LDL(self):
        #OpCode 2E
        self.pc=self.pc+2
        self.cycle=self.cycle+7
        regValue=self.memory[self.pc-1]
        return "LD L, " + format(regValue, "02X")
    
    def LDSPnn(self):
        #OpCode 31
        self.pc=self.pc+3
        self.cycle=self.cycle+10
        regValue=int(self.memory[self.pc-1])+int(self.memory[self.pc-2])*256
        return "LD SP, " + format(regValue, "04X")
    
    def STA(self):
        #OpCode 32
        self.pc=self.pc+3
        self.cycle=self.cycle+13
        address=int(self.memory[self.pc-2])+int(self.memory[self.pc-1])*256
        return "LD " + format(address, "04X") + ", A"

    def INCatHL(self):
        #OpCode 34
        self.pc=self.pc+1
        self.cycle=self.cycle+11
        return "INC (HL)"
    
    def DECatHL(self):
        #OpCode 35
        self.pc=self.pc+1
        self.cycle=self.cycle+5
        return "DEC (HL)"
        
    def LDIHL(self):
        #OpCode 36
        self.pc=self.pc+2
        self.cycle=self.cycle+10
        regValue=self.memory[self.pc-1]
        return "LD (HL), " + format(regValue, "02X")

    def SCF(self):
        #OpCode 37
        self.pc=self.pc+1
        self.cycle=self.cycle+4
        return "SCF"
    
    def LDA(self):
        #OpCode 3A
        self.pc=self.pc+3
        self.cycle=self.cycle+13
        address=int(self.memory[self.pc-2])+int(self.memory[self.pc-1])*256
        return "LD A, (" + format(address, "04X") + ")"
    
    def INCA(self):
        self.pc=self.pc+1
        self.cycle=self.cycle+4
        return "INC A"
    
    def DECA(self):
        self.pc=self.pc+1
        self.cycle=self.cycle+4
        return "DEC A"
    
    def MVI(self):
        self.pc=self.pc+2
        self.cycle=self.cycle+7
        regValue=self.memory[self.pc-1]
        return "LD A, " + format(regValue, "02X")
    
    def LDEA(self):
        self.pc=self.pc+1
        self.cycle=self.cycle+4
        return "LD E, A"
    
    def LDBH(self):
        self.pc=self.pc+1
        self.cycle=self.cycle+4     #8080 has 5 cycles, 8085 has 4, z80 has 4
        return "LD B, H"

    
    def LDBHL(self):
        self.pc=self.pc+1
        self.cycle=self.cycle+7
        return "LD B, (HL)"
    
    def LDBA(self):
        self.pc=self.pc+1
        self.cycle=self.cycle+4
        return "LD B, A"
    
    def LDCHL(self):
        self.pc=self.pc+1
        self.cycle=self.cycle+7
        return "LD C, (HL)"
    
    def LDCA(self):
        #OpCode 4F
        self.pc=self.pc+1
        self.cycle=self.cycle+4
        return "LD C, A"
    
    def LDDE(self):
        #OpCode 53
        self.pc=self.pc+1
        self.cycle=self.cycle+4
        return "LD D, E"
    
    def LDDHL(self):
        #OpCode 56
        self.pc=self.pc+1
        self.cycle=self.cycle+7
        return "LD D, (HL)"
    
    def LDEHL(self):
        #OpCode 5E
        self.pc=self.pc+1
        self.cycle=self.cycle+7
        return "LD E, (HL)"
        
    def LDHC(self):
        #OpCode 61
        self.pc=self.pc+1
        self.cycle=self.cycle+4
        return "LD H, C"
    
    def LDHHL(self):
        #OpCode 66
        self.pc=self.pc+1
        self.cycle=self.cycle+7
        return "LD H, (HL)"

    def LDHA(self):
        #OpCode 67
        self.pc=self.pc+1
        self.cycle=self.cycle+4
        return "LD H, A"
    
    def LDLB(self):
        #OpCode 68
        self.pc=self.pc+1
        self.cycle=self.cycle+4  #8080 has 5 cycles, 8085 has 4, z80 has 4
        return "LD L, B"
    
    def LDLC(self):
        #OpCode 69
        self.pc=self.pc+1
        self.cycle=self.cycle+4
        return "LD L, C"

    def LDLA(self):
        #OpCode 6F
        self.pc=self.pc+1
        self.cycle=self.cycle+4
        return "LD L, A"
    
    def LDHLB(self):
        #OpCode 70
        self.pc=self.pc+1
        self.cycle=self.cycle+7
        return "LD (HL), B"
    
    def LDHLC(self):
        #OpCode 71
        self.pc=self.pc+1
        self.cycle=self.cycle+7
        return "LD (HL), C"
    
    def LDHLD(self):
        #OpCode 72
        self.pc=self.pc+1
        self.cycle=self.cycle+7
        return "LD (HL), D"
    
    def LDHLE(self):
        #OpCode 73
        self.pc=self.pc+1
        self.cycle=self.cycle+7
        return "LD (HL), E"
    
    def LDHLA(self):
        #OpCode 77
        self.pc=self.pc+1
        self.cycle=self.cycle+7
        return "LD (HL), A"
       
    def LDAB(self):
        #OpCode 78
        self.pc=self.pc+1
        self.cycle=self.cycle+4
        return "LD A, B"
    
    def LDAC(self):
        #OpCode 79
        self.pc=self.pc+1
        self.cycle=self.cycle+4
        return "LD A, C"
    
    def LDAD(self):
        #OpCode 7A
        self.pc=self.pc+1
        self.cycle=self.cycle+4
        return "LD A, D"
    
    def LDAE(self):
        #OpCode 7B
        self.pc=self.pc+1
        self.cycle=self.cycle+4
        return "LD A, E"
    
    def LDAL(self):
        #OpCode 7D
        self.pc=self.pc+1
        self.cycle=self.cycle+4
        return "LD A, L"

    def LDAH(self):
        #OpCode 7C
        self.pc=self.pc+1
        self.cycle=self.cycle+4
        return "LD A, H"
         
    def LDAHL(self):
        #OpCode 7E
        self.pc=self.pc+1
        self.cycle=self.cycle+7
        return "LD A, (HL)"
    
    def ADDAB(self):
        #OpCode 80
        self.pc=self.pc+1
        self.cycle=self.cycle+4
        return "ADD A, B"

    def ADDAL(self):
        #OpCode 85
        self.pc=self.pc+1
        self.cycle=self.cycle+4
        return "ADD A, L"
    
    def ADDAHL(self):
        #OpCode 86
        self.pc=self.pc+1
        self.cycle=self.cycle+7
        return "ADD A, (HL)"

    def SUBA(self):
        #OpCode 97
        self.pc=self.pc+1
        self.cycle=self.cycle+4
        return "SUB A"   
    
    def ANDB(self):
        #OpCode A0
        self.pc=self.pc+1
        self.cycle=self.cycle+4
        return "AND B"
    
    def ANDA(self):
        #OpCode A7
        self.pc=self.pc+1
        self.cycle=self.cycle+4
        return "AND A"
    
    def XORA(self):
        #OpCode AF
        self.pc=self.pc+1
        self.cycle=self.cycle+4
        return "XOR A"
    
    def ORB(self):
        #OpCode B0
        self.pc=self.pc+1
        self.cycle=self.cycle+4
        return "OR B"
    
    def ORE(self):
        #OpCode B4
        self.pc=self.pc+1
        self.cycle=self.cycle+4
        return "OR E"

    def CPB(self):
        #OpCode B8
        self.pc=self.pc+1
        self.cycle=self.cycle+4
        return "CP B"
    
    def CPHL(self):
        #OpCode BE
        self.pc=self.pc+1
        self.cycle=self.cycle+7
        return "CP (HL)"
    
    def RETNZ(self):
        #OpCode C0
        self.pc=self.pc+1
        self.cycle=self.cycle+5        # 5 or 11 depending on execution
        return "RET NZ"
    
    def POPB(self):
        self.pc=self.pc+1
        self.cycle=self.cycle+10
        return "POP BC"
    
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
    
    def CALLNZ(self):
        self.pc=self.pc+3
        self.cycle=self.cycle+17  # 10 or 17 depending on execution
        address=int(self.memory[self.pc-2])+int(self.memory[self.pc-1])*256
        return "CALL NZ, " + format(address, "04X")
    
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
    
    def RETZ(self):
        self.pc=self.pc+1
        self.cycle=self.cycle+11        # 5 or 11 depending on execution
        return "RET Z"
    
    def RET(self):
        self.pc=self.pc+1
        self.cycle=self.cycle+10
        return "RET"
    
    def CALLZ(self):
        self.pc=self.pc+3
        self.cycle=self.cycle+17  # 10 or 17
        address=int(self.memory[self.pc-2])+int(self.memory[self.pc-1])*256
        return "CALL Z, " + format(address, "04X")

    def CALL(self):
        #OpCode CD
        self.pc=self.pc+3
        self.cycle=self.cycle+17
        address=int(self.memory[self.pc-2])+int(self.memory[self.pc-1])*256
        return "CALL " + format(address, "04X")


    def RETNC(self):
        #OpCode D0
        self.pc=self.pc+1
        self.cycle=self.cycle+11       # 5 or 11 depending on execution
        return "RET NC"


    def POPD(self):
        #OpCode D1
        self.pc=self.pc+1
        self.cycle=self.cycle+10
        return "POP DE"

    def JPNC(self):
        #OpCode D2
        self.pc=self.pc+3
        self.cycle=self.cycle+10
        address=int(self.memory[self.pc-2])+int(self.memory[self.pc-1])*256
        return "JP NC, " + format(address, "04X")

    def OUTnnA(self):
        #OpCode D3
        self.pc=self.pc+2
        self.cycle=self.cycle+11       # Z80 has 11 cycles, 8080 has 10, 8085 has 10
        value=self.memory[self.pc-1]
        return "OUT (" + format(value, "02X") + "), A"
    
    def PUSHD(self):
        #OpCode D5
        self.pc=self.pc+1
        self.cycle=self.cycle+11
        return "PUSH DE"
    
    def SUBV(self):
        #OpCode D6
        self.pc=self.pc+2
        self.cycle=self.cycle+7
        value=self.memory[self.pc-1]
        return "SUB " + format(value, "02X")
    
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
    
    def SBCA(self):
        self.pc=self.pc+2
        self.cycle=self.cycle+7
        value=self.memory[self.pc-1]
        return "SBC A, " + format(value, "02X")

    def POPH(self):
        #OpCode E1
        self.pc=self.pc+1
        self.cycle=self.cycle+10
        return "POP HL"

    def JPnn(self):
        #OpCode E3
        self.pc=self.pc+3
        self.cycle=self.cycle+10
        address=int(self.memory[self.pc-2])+int(self.memory[self.pc-1])*256
        return "JP " + format(address, "04X")
    
    def PUSHH(self):
        #OpCode E5
        self.pc=self.pc+1
        self.cycle=self.cycle+11
        return "PUSH HL"
    
    def ANDV(self):
        self.pc=self.pc+2
        self.cycle=self.cycle+7
        value=self.memory[self.pc-1]
        return "AND " + format(value, "02X")
    
    def EXDEHL(self):
        self.pc=self.pc+1
        self.cycle=self.cycle+4
        return "EX DE, HL"
    
    def RETP(self):
        self.pc=self.pc+1
        self.cycle=self.cycle+11        # 5 or 11 depending on execution
        return "RET P"

    def POPPSW(self):
        #OpCode F1
        self.pc=self.pc+1
        self.cycle=self.cycle+10
        return "POP AF"

    def PUSHPSW(self):
        #OpCode F5
        self.pc=self.pc+1
        self.cycle=self.cycle+11
        return "PUSH PSW"
    
    def ORV(self):
        #OpCode F6
        self.pc=self.pc+2
        self.cycle=self.cycle+7
        value=self.memory[self.pc-1]
        return "OR " + format(value, "02X")
    
    def JPM(self):
        #OpCode FA
        self.pc=self.pc+3
        self.cycle=self.cycle+10
        address=int(self.memory[self.pc-2])+int(self.memory[self.pc-1])*256
        return "JP M, " + format(address, "04X")
    
    def EI(self):
        self.pc=self.pc+1
        self.cycle=self.cycle+4
        return "EI"

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