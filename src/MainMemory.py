from src.util import log2
from src.util import Word
from src.constantes import *


class MainMemory:
    # Construtor da Memória principal.
    #
    # @param ramsize : int - Capacidade total da memória real, que deve ser múltiplo de 4.
    #
    # @param tamLinha : int - Capacidade total da memória virtual, que deve ser múltiplo de 4.
    #
    # @raise TypeError, ValueError.
    #
    def __init__(self, ramsize, vmsize):
        self.__apuraInput(ramsize, vmsize)

        self.__ramSize = ramsize
        self.__vmSize = vmsize
        self.__totalSize = ramsize + vmsize
        self.__dataList = [Word(0)] * (self.__totalSize // 4)

    # Lança exceção se algum dos argumentos do construtor estiver inconsistente.
    #
    # @param ramsize : int - mesmo do construtor.
    # @param vmsize : int - mesmo do construtor.
    #
    # @raise TypeError, ValueError.
    #
    # @return None.
    #
    def __apuraInput(self, ramsize, vmsize):
        if type(ramsize) != int:
            raise TypeError('ramsize deve ser int.')

        if type(vmsize) != int:
            raise TypeError('vmsize deve ser int.')

        if ((ramsize % 4) != 0):
            raise ValueError('Armazenamento em mem principal incorreto, deve ser múltiplo de 4.')

        if ((vmsize % 4) != 0):
            raise ValueError('Armazenamento em mem virtual incorreto, deve ser múltiplo de 4.')

    # Get atribute.
    # @return int.
    #
    def getTamRam(self):
        return self.__ramSize

    # Get atribute.
    # @return int.
    #
    def getTamMemVirtual(self):
        return self.__vmSize

    # Get atribute.
    # @return int.
    #
    def getTamTotal(self):
        return self.__totalSize

    # Obter os log2(totalSize/4) primeiros bits de address.
    #
    # @param address : int - endereço de 32 bits.
    #
    # @raise TypeError, ValueError.
    #
    # return int.
    #
    def getEndMem(self, address):
        self.__verificaAddress(address)
        return address >> 2 #( 32 - log2(self.__totalSize // 4) )

    # Setar um endereço da memória com determinado valor.
    #
    # @param address : int - endereço de 32 bits.
    # @param value : int - valor a ser colocado.
    #
    # @raise TypeError.
    #
    # return None.
    #
    def setDado(self, address, value):
        try:
            self.__verificaWord(value)
            end = self.getEndMem(address)
        except ValueError:
            return ADDRESS_OUT_OF_RANGE

        self.__dataList[end] = value.copy()
        return FOUND_IN_MEM

    # Obter o valor de um requesitado endereço da memória.
    #
    # @param address : int - endereço de 32bits.
    # @param value : int - valor a ser recuperado
    #
    # @raise TypeError.
    #
    # return None.
    #
    def getDado(self, address, value):
        try:
            self.__verificaWord(value)
            value.set( self.__dataList[self.getEndMem(address)].get() )
        except ValueError:
            return ADDRESS_OUT_OF_RANGE

        return FOUND_IN_MEM

    # Retorna cópia dos dados, para depuração.
    #
    # @return list.
    #
    def getList(self):
        return list(self.__dataList)

    # Verifica corretude do endereço.
    #
    # @param address : int - endereço de 32 bits.
    #
    # @raise TypeError, ValueError.
    #
    # @return None.
    #
    def __verificaAddress(self, address):
        if type(address) != int:
            raise TypeError('Endereço deve ser int.')
        if address.bit_length() > 32 or address < 0:
            raise ValueError('Endereço inválido.')
        if address >= self.__totalSize:
            raise ValueError('Endereço fora da faixa.')

    # Verifica corretude da palavra de 32 bits.
    #
    # @param word : Word - palavra 32 bits.
    #
    # @raise TypeError.
    #
    # @return None.
    #
    def __verificaWord(self, word):
        if type(word) != Word:
            raise TypeError('Word inválida.')

    # Pega uma linha inteira que cabe no L3.
    # @param start : int - endereço inicial.
    # @return list.
    #
    def getMemoryLine(self, start, tamLinha):
        # print([self.__dataList[i] for i in range(start//4, start//4 + tamLinha)])
        return [self.__dataList[i] for i in range(start//4, start//4 + tamLinha)]


### Funções de interface (adapter):


def createMainMemory(ramsize, vmsize):
    return MainMemory(ramsize, vmsize)


def getMainMemoryData(mem, address, value):
    return mem.getDado(address, value)


def setMainMemoryData(mem, address, value):
    return mem.setDado(address, value)
