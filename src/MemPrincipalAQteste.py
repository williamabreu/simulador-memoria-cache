class MainMemory:
    def __init__(self, ramsize, vmsize):      #MainMemory createMainMemory(int ramsize, int vmsize);
        self.adressList = [0] * (ramsize + vmsize)

    
    def setMainMemoryData(self, address, value):      # void setMainMemoryData(MainMemory mem, int address, int value);   
        self.adressList[adress]=value
        self.total += 1

    def getMainMemoryData(self, adress, value):      # int getMainMemoryData(MainMemory mem, int address, int * value);
        for i in self.adressList:
            if i == adress:
                value=4;
                return value
        value=-1;
        return value
