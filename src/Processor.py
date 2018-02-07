from src.Memory import Memory


class Processor:
    # Cosntrutor.
    # @param mem : Memory - hierarquia de memória.
    # @param ncores : int - número de núcleos.
    # @raise TypeError.
    #
    def __init__(self, mem, ncores):
        if type(mem) != Memory:
            raise TypeError('Tipo mem incorreto.')
        if type(ncores) != int:
            raise TypeError('Tipo ncores incorreto.')

        self.__processador = [None] * ncores
        self.__processador[0] = mem

        for x in range(1, ncores):
            self.__processador[x] = mem.duplicate()

    # Retorna número de núcleos.
    # @return int.
    #
    def getNumCores(self):
        return len(self.__processador)

    # Retorna a hirarquia de mem do processador n.
    # @param n : int - número do núcleo do processador.
    # @raise IndexError, TypeError.
    # @return Memory.
    #
    def getCore(self, n):
        return self.__processador[n]


### Função de interface (adpter):

def createProcessor(mem, ncores):
    return Processor(mem, ncores)