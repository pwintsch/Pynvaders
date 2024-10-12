from pathlib import Path

import numpy as np


class Processor:     
    def __init__(self, program):
        self.memory=np.zeros(65536,dtype=np.uint8)
        self.programSize=len(program)
        for i in range(len(program)):
            self.memory[i]=program[i]
        self.pc=0
    
    def fetch(self):
        addr=format(self.pc,"06")
        opCode=""
        found=True
        if self.memory[self.pc] == 0:
            opCode=format(self.memory[self.pc], "<02x") + " - " + "NOP"
            self.pc=self.pc+1
        else:
            opCode=format(self.memory[self.pc], "<02x") + " - " +"NOT YET IMPLEMENTED"
            found=False
        return addr + " - " + opCode, found

            
def main():
    myFileName='./rom/invaders.h'
    myFile=Path(myFileName)
    if myFile.exists() and myFile.is_file():
        myFileExtension = myFile.suffix
        myFileSize=myFile.stat().st_size
        print ("FileSize is ", myFileSize)
        rawData=myFile.read_bytes()
        index=0
        program=[]
        proc=Processor(rawData)
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
    else:
        print("Problem with file:", myFileName)




print ("Hi this is Pyn_dis.py, a dissasembler in Python of the Space Invaders MAME ROMs")
if __name__ == "__main__":
    main()