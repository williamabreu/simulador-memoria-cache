from src.util import isPotenciaDois
from src.util import log2
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
        self.__numColunas = tamLinha // 4
        self.__tamOffset = log2(self.__numColunas)
        self.__tamLookup = log2(self.__numConjuntos)

        self.__verifica32Bits()

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
            raise ValueError('Tamanho de linha inválido, deve ser potência de 2.')

        if tamLinha % 4 != 0:
            raise ValueError('Tamanho de Linha inválido, deve ser múltiplo de 4.')

        if capacidade % (tamLinha * associatividade) != 0:
            raise ValueError('Capacidade inválida, deve ser múltiplo de (assoc)x(tamLinha).')

    # Lança exceção se lookup e offset estourarem 32 bits.
    #
    # @raise ValueError.
    #
    # @return None.
    #
    def __verifica32Bits(self):
        if self.__tamLookup + self.__tamOffset > 32:
            raise ValueError('Tamanho do lookup + offset ultrapassam 32 bits.')

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

    # Operador <.
    #
    # @param other : SACache - instância de comparação.
    #
    # @raise TypeError.
    #
    # @return bool.
    #
    def __lt__(self, other):
        if type(other) != SACache:
            raise TypeError('Objetos devem ser SACache para comparar.')
        else:
            return self.__tamLinha < other.__tamLinha

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

    # Cria nova SAC com as mesmas características, mas vazia.
    #
    # @param sac : SACache - cache de referência.
    #
    # return SACache.
    #
    def duplicate(self):
        c = self.getCapacidade()
        a = self.getNumLinhas()
        l = self.getTamLinha()
        return SACache(c, a, l)


### FUNÇÕES DE INTERFACE (requisitos do Dr. Saúde):


def createSACache(c, a, l):
    return SACache(c, a, l)


def getSACacheCapacity(sac):
    return sac.getCapacidade()


def getSACacheLineSize(sac):
    return sac.getTamLinha()


def getSACacheData(sac, address, value):
    return sac.getDado(address, value)


def setSACacheLine(sac, address, line):
    sac.setLine(address, line)


def setSACacheData(sac, address, value):
    return sac.setDado(address, value)


def duplicateSACache(sac):
    return sac.duplicate()



