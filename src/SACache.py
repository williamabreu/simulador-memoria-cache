import math

from src.util import isPotenciaDois
from src.TACache import TACache


class SACache:
    # Construtor da cache associativa por conjuntos.
    #
    # @param capacidade : int - tamanho total em bytes, deve ser potência de 2 e
    #                           múltiplo de (numLinhas) x (associatividade).
    #
    # @param associatividade : int - número de conjuntos TAC dentro da SAC, deve
    #                          ser potência de 2.
    #
    # @param tamLinha : int - número de bytes por linha por conjunto, deve ser potência de 2.
    #
    def __init__(self, capacidade, associatividade, tamLinha):
        self.__verificaArgumentos(capacidade, associatividade, tamLinha)

        self.__capacidade = capacidade
        self.__numLinhasConjunto = associatividade
        self.__tamLinha = tamLinha
        self.__numConjuntos = capacidade // (associatividade * tamLinha)
        self.__tamOffset = int(math.log(tamLinha, 2))
        self.__tamLookup = int(math.log(self.__numConjuntos, 2))

        c = self.__capacidade // self.__numConjuntos
        l = self.__tamLinha
        self.__conjuntos = [TACache(c, l) for i in range(self.__numConjuntos)]

    # Lança exceção se algum dos argumentos do construtor estiver errado.
    # 
    # @param capacidade : int - mesmo do construtor.
    # @param associatividade : int - mesmo do construtor.
    # @param tamLinha : int - mesmo do construtor.
    #
    # @raise ValueError.
    #
    # @return None.
    #
    def __verificaArgumentos(self, capacidade, associatividade, tamLinha):
        if type(capacidade) != int:
            raise ValueError('Capacidade inválida, deve ser inteiro.')

        if type(associatividade) != int:
            raise ValueError('Associatividade inválida, deve ser inteiro.')

        if type(tamLinha) != int:
            raise ValueError('Tamanho de Linha inválido, deve ser inteiro.')

        if not isPotenciaDois(capacidade):
            raise ValueError('Capacidade inválida, deve ser potência de 2.')

        if not isPotenciaDois(associatividade):
            raise ValueError('Associatividade inválida, deve ser potência de 2.')

        if not isPotenciaDois(tamLinha):
            raise ValueError('Tamanho de Linha inválido, deve ser potência de 2.')

        if capacidade % (tamLinha * associatividade) != 0:
            raise ValueError('Capacidade inválida, deve ser múltiplo de (assoc)x(tamLinha).')

    # Obtém a capacidade.
    #
    # @return int.
    #
    def getCapacidade(self):
        return self.__capacidade

    # Obtém o tamanho da linha.
    #
    # @return int.
    #
    def getTamLinha(self):
        return self.__tamLinha

    # Obtém o número de linhas por conjunto da cache.
    #
    # @return int.
    #
    def getNumLinhas(self):
        return self.__numLinhasConjunto

    # Obtém o número de conjuntos da cache.
    #
    # @return int.
    #
    def getNumConjuntos(self):
        return self.__numConjuntos

    # Obtém os bits de lookup de um dado endereço.
    #
    # @param address : int - endereço de 32 bits (4 bytes).
    #
    # @return int.
    #
    def getBitsLookup(self, address):
        return (address >> self.__tamOffset) & (2 ** self.__tamLookup - 1)

    # Representação em string.
    #
    # @return str.
    #
    def __repr__(self):
        out = '#{}:\n{}'.format(0, self.__conjuntos[0])
        for i in range(1, self.__numConjuntos):
            out += '\n#{}:\n{}'.format(i, self.__conjuntos[i])
        return out

    # Obtém o dado salvo do endereço.
    #
    # @param address : int - endereço de 32 bits (4 bytes).
    # @param valor : INT - inteiro para passagem por valor.
    #
    # @return bool.
    #
    def getDado(self, address, valor):
        lookup = self.getBitsLookup(address)
        tac = self.__conjuntos[lookup]
        return tac.getDado(address, valor)


    # Insere uma linha da memória na cache.
    #
    # @param address : int - endereço de origem.
    # @param linha : list - valores da linha da memória.
    #
    # return None.
    #
    def setLine(self, address, linha):
        lookup = self.getBitsLookup(address)
        tac = self.__conjuntos[lookup]
        tac.setLine(address, linha)

    # Insere um dado lido da memória na cache.
    #
    # @param address : int - endereço de origem do dado.
    # @param valor : int - valor propriamente dito
    #
    # return bool.
    #
    def setDado(self, address, valor):
        lookup = self.getBitsLookup(address)
        tac = self.__conjuntos[lookup]
        return tac.setDado(address, valor)


### FUNÇÕES DE INTERFACE (requisitos do Dr. Saúde):


# Cria nova cache associativa por conjutos.
#
# @param c : int - capacidade.
# @param a : int - associatividade.
# @param l : int - tamanho da linha.
#
# @return SACache.
#
def createSACache(c, a, l):
    return SACache(c, a, l)


# Obtém o valor da capacidade da cache.
#
# @param sac : SACache - referência para cache.
#
# @return int.
#
def getSACacheCapacity(sac):
    return sac.getCapacidade()


# Obtém o valor do tamanho da linha da cache.
#
# @param tac : SACache - referência para cache.
#
# @return int.
#
def getSACacheLineSize(sac):
    return sac.getTamLinha()


# Tenta obter um valor na cache pelo endereço passado.
#
# @param sac : SACache - referência para cache.
# @param address : int - endereço de origem.
# @param value : INT - inteiro por passagem por valor.
#
# return bool.
#
def getSACacheData(sac, address, value):
    return sac.getDado(address, value)


# Insere uma linha da memória na cache.
#
# @param sac : SACache - referência para cache.
# @param address : int - endereço de origem.
# @param line : list - valores da linha da memória.
#
# return None.
#
def setSACacheLine(sac, address, line):
    sac.setLine(address, line)


# Insere um dado lido da memória na cache.
#
# @param tac : SACache - referência para cache.
# @param address : int - endereço de origem do dado.
# @param value : int - valor propriamente dito.
#
# return bool.
#
def setSACacheData(sac, address, value):
    return sac.setDado(address, value)


# Cria nova SAC com as mesmas características, mas vazia.
#
# @param sac : SACache - cache de referência.
#
# return SACache.
#
def duplicateSACache(sac):
    c = sac.getCapacidade()
    a = sac.getNumLinhas()
    l = sac.getTamLinha()
    return SACache(c, a, l)



