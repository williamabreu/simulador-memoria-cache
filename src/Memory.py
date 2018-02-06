from src.Cache import Cache
from src.util import Word
from src.MainMemory import MainMemory
from src.constantes import *


class Memory:

    def __init__(self, cache, mem):
        self.__cache = cache
        self.__mem = mem

    # @raise TypeError.
    #
    def getDado(self, address, data):
        try:
            return self.__cache.getCacheData(self.__mem, address, data)
        except ValueError:
            return ADDRESS_OUT_OF_RANGE

    # @raise TypeError.
    #
    def getInstrucao(self, address, instruction):
        try:
            return self.__cache.getCacheInst(self.__mem, address, instruction)
        except ValueError:
            return ADDRESS_OUT_OF_RANGE

    # metodo de cache nao implementado
    def setData(self, address, data):
        self.__cache.setCacheData(address, data)
        self.__mem.setMainMemoryData(address, data)

    def setInstruction(self, address, instruction):
        self.__cache.setCacheInstruction(address, instruction)

    # ok
    def duplicate(self):
        return Memory(self.__cache.duplicate(), self.__mem)

    # Lança exceção se algum dos argumentos do construtor estiver inconsistente.
    #
    # @param cache : Cache - mesmo do construtor.
    # @param mem : MainMemory - mesmo do construtor.
    #
    # @raise TypeError
    #
    # @return None.
    #
    def __apuraInput(self, cache, mainMem):
        if type(cache) != Cache:
            raise TypeError('Tipo objeto Cache incorreto.')

        if type(mainMem) != MainMemory:
            raise TypeError('Tipo objeto Memory incorreto.')
