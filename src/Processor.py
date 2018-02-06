
class Processor:
    processador=[]

    def __init__createProcessor(mem ,ncores):
        self.processador=[None]* ncores
        self.processador[0]=mem
        for x in range(1,ncores):
            self.processador[x]=Memory.duplicateMemory(mem)
        return processador

