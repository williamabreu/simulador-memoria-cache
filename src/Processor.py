class Processor:
    def __init__(self, hierarquia, numCores):
        self.__mem = hierarquia
        self.__numCores = numCores

    def getNumCores(self):
        return self.__numCores
