class Processor:
    def __init__(self, mem, ncores):
        self.__processador = [None] * ncores
        self.__processador[0] = mem

        for x in range(1, ncores):
            self.__processador[x] = mem.duplicate()

    def getNumCores(self):
        return len(self.__processador)

    def getCore(self, n):
        return self.__processador[n]

