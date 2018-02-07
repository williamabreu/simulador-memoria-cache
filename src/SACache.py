from src.util import isPotenciaDois
from src.util import log2
from src.TACache import TACache


class SACache:
    # Construtor da cache associativa por conjuntos.
    #
    # @param capacidade : int - tamanho total em bytes, deve ser potência de 2 e
    #                           múltiplo de (tamLinha) x (associatividade).
    #
    # @param associatividade : int - número de linhas em cada conjunto, deve ser potência de 2.
    #
    # @param tamLinha : int - número de bytes por linha de cada conjunto, deve ser potência de 2.
    #
    # @raise ValueError, TypeError.
    #
    def __init__(self, capacidade, associatividade, tamLinha):
        self.__verificaArgumentos(capacidade, associatividade, tamLinha)

        self.__capacidade = capacidade
        self.__numLinhasConjunto = associatividade
        self.__tamLinha = tamLinha
        self.__numConjuntos = capacidade // (associatividade * tamLinha)
        self.__numColunas = tamLinha // 4
        self.__tamOffset = log2(self.__tamLinha)
        self.__tamLookup = log2(self.__numConjuntos)

        c = self.__capacidade // self.__numConjuntos
        l = self.__tamLinha
        self.__conjuntos = [TACache(c, l) for i in range(self.__numConjuntos)]

    # Lança exceção se algum dos argumentos do construtor estiver errado.
    # 
    # @param capacidade : int - mesmo do construtor.
    # @param associatividade : int - mesmo do construtor.
    # @param tamLinha : int - mesmo do construtor.
    #
    # @raise ValueError, TypeError.
    #
    # @return None.
    #
    def __verificaArgumentos(self, capacidade, associatividade, tamLinha):
        if type(capacidade) != int:
            raise TypeError('Capacidade inválida, deve ser inteiro.')

        if type(associatividade) != int:
            raise TypeError('Associatividade inválida, deve ser inteiro.')

        if type(tamLinha) != int:
            raise TypeError('Tamanho de Linha inválido, deve ser inteiro.')

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

    # Obtém a quantidade de bits de lookup.
    #
    # @return int.
    #
    def getTamLookup(self):
        return self.__tamLookup

    # Obtém a quantidade de bits de offset.
    #
    # @return int.
    #
    def getTamOffset(self):
        return self.__tamOffset

    # Obtém a quantidade de bits de tag.
    #
    # @return int.
    #
    def getTamTag(self):
        return 32 - self.__tamOffset - self.__tamLookup

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
    # @raise TypeError, ValueError.
    #
    # @return int.
    #
    def getBitsLookup(self, address):
        self.__verificaAddress(address)
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
    # @param word : Word - palavra de 32 bits (4 bytes).
    #
    # @raise TypeError, ValueError, IndexError.
    #
    # @return bool.
    #
    def getDado(self, address, word):
        self.__verificaAddress(address)
        lookup = self.getBitsLookup(address)
        tac = self.__conjuntos[lookup]
        return tac.getDado(address, word)


    # Insere uma linha da memória na cache.
    #
    # @param address : int - endereço de origem.
    # @param linha : list - valores da linha da memória.
    #
    # @raise TypeError, IndexError, ValueError.
    #
    # return None.
    #
    def setLine(self, address, linha):
        self.__verificaAddress(address)
        lookup = self.getBitsLookup(address)
        tac = self.__conjuntos[lookup]
        tac.setLine(address, linha)

    # Insere um dado lido da memória na cache.
    #
    # @param address : int - endereço de origem do dado.
    # @param valor : Word - palavra de 32 bits (4 bytes).
    #
    # @raise TypeError, ValueError.
    #
    # return bool.
    #
    def setDado(self, address, valor):
        self.__verificaAddress(address)
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


### FUNÇÕES DE INTERFACE (adapter):


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



