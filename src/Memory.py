from src.Cache import Cache
from src.MainMemory import MainMemory
from src.constantes import *


class Memory:
    # Cosntrutor.
    # @param cache : Cache - cache inclusivo.
    # @param mem : MainMemory - memória principal.
    # @raise TypeError.
    #
    def __init__(self, cache, mem):
        self.__apuraInput(cache, mem)
        self.__cache = cache
        self.__mem = mem

    # Obtém um dado pelo endereço em algum nível na hierarquia.
    # Retorna o nível em que foi encontrado.
    # @param adddress : int - endereço de 32 bits.
    # @param data : Word - palavra de retorno de 32 bits.
    # @raise TypeError.
    # @return int.
    #
    def getDado(self, address, data):
        try:
            return self.__cache.getCacheData(self.__mem, address, data)
        except ValueError:
            return ADDRESS_OUT_OF_RANGE

    # Obtém uma instrução pelo endereço em algum nível na hierarquia.
    # Retorna o nível em que foi encontrado.
    # @param adddress : int - endereço de 32 bits.
    # @param data : Word - palavra de retorno de 32 bits.
    # @raise TypeError.
    # @return int.
    #
    def getInstrucao(self, address, instruction):
        try:
            return self.__cache.getCacheInst(self.__mem, address, instruction)
        except ValueError:
            return ADDRESS_OUT_OF_RANGE

    # Insere um dado na memória, obedecendo a hierarquia.
    # @param adddress : int - endereço de 32 bits.
    # @param data : Word - palavra a inserir de 32 bits.
    # @return None.
    #
    def setDado(self, address, data):
        #self.__cache.setCacheData(address, data)
        self.__mem.setDado(address, data)

    # Insere uma instrução na memória, obedecendo a hierarquia.
    # @param adddress : int - endereço de 32 bits.
    # @param data : Word - palavra a inserir de 32 bits.
    # @return None.
    #
    def setInstrucao(self, address, instruction):
        #self.__cache.setCacheInstruction(address, instruction)
        self.setDado(address, instruction)

    # Duplica.
    # @return Memory.
    #
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



