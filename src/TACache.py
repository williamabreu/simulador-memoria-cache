from src.util import isPotenciaDois
from src.util import log2
from src.util import CACHE_HIT
from src.util import CACHE_MISS


class TACache:
    # Construtor da cache totalmente associativa.
    #
    # @param capacidade : int - tamanho total em bytes, deve ser potência de 2 e
    #                           múltiplo de bytesLinha.
    #
    # @param tamLinha : int - número de bytes por linha, deve ser potência de 2.
    #
    def __init__(self, capacidade, tamLinha):
        self.__verificaArgumentos(capacidade, tamLinha)

        self.__capacidade = capacidade
        self.__tamLinha = tamLinha
        self.__numLinhas = capacidade // tamLinha
        self.__numColunas = tamLinha // 4
        self.__tamOffset = log2(self.__numColunas)

        self.__tags = [None] * self.__numLinhas

        # cada célula tem 4 bytes (32 bits)
        self.__matriz = [[None] * self.__numColunas for i in range(self.__numLinhas)]

        self.__posInserirFila = 0

    # Lança exceção se algum dos argumentos do construtor estiver errado.
    # 
    # @param capacidade : int - mesmo do construtor.
    # @param numLinhas : int - mesmo do construtor.
    #
    # @raise ValueError.
    #
    # @return None.
    #
    def __verificaArgumentos(self, capacidade, tamLinha):
        if type(capacidade) != int:
            raise ValueError('Capacidade inválida, deve ser inteiro.')

        if type(tamLinha) != int:
            raise ValueError('Tamanho da Linha inválido, deve ser inteiro.')

        if not isPotenciaDois(capacidade):
            raise ValueError('Capacidade inválida, deve ser potência de 2.')

        if not isPotenciaDois(tamLinha):
            raise ValueError('Tamanho de linha inválido, deve ser potência de 2.')

        if tamLinha % 4 != 0:
            raise ValueError('Tamanho de linha inválido, deve ser múltiplo de 4.')

        if capacidade % tamLinha != 0:
            raise ValueError('Capacidade inválida, deve ser múltiplo de tamLinha.')

    # Obtém a posição correta para se inserir uma nova tag na lista (fila circular)
    #
    # @return int.
    #
    def __getPosicaoInserirFila(self):
        posAtual = self.__posInserirFila
        self.__posInserirFila = (self.__posInserirFila + 1) % self.__numLinhas
        return posAtual

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

    # Obtém o número de linhas da cache.
    #
    # @return int.
    #
    def getNumLinhas(self):
        return self.__numLinhas

    # Obtém os bits de offset de um dado endereço. 
    #
    # @param address : int - endereço de 32 bits (4 bytes).
    #
    # @return int.
    #
    def getBitsOffset(self, address):
        return address & (self.__numColunas - 1)

    # Obtém os bits de tag de um dado endereço. 
    #
    # @param address : int - endereço de 32 bits (4 bytes).
    #
    # @return int.
    #
    def getBitsTag(self, address):
        return address >> self.__tamOffset

    # Representação em string.
    #
    # @return str.
    #
    def __repr__(self):
        out = '{} -> {}'.format(self.__tags[0], self.__matriz[0])
        for i in range(1, self.__numLinhas):
            out += '\n{} -> {}'.format(self.__tags[i], self.__matriz[i])
        return out

    # Obtém o dado salvo do endereço. 
    #
    # @param address : int - endereço de 32 bits (4 bytes).
    # @param valor : INT - inteiro para passagem por valor.
    #
    # @return bool.
    #
    def getDado(self, address, valor):
        tag = self.getBitsTag(address)
        offset = self.getBitsOffset(address)

        pos = self.buscaTag(tag)

        if pos != -1:
            valor.set(self.__matriz[pos][offset])
            return CACHE_HIT
        else:
            return CACHE_MISS

    # Insere uma linha da memória na cache.
    #
    # @param address : int - endereço de origem.
    # @param linha : list - valores da linha da memória.
    #
    # return None.
    #
    def setLine(self, address, linha):
        tag = self.getBitsTag(address)
        pos = self.buscaTag(tag)
        linha = [linha[i] for i in range(self.__numColunas)]

        if pos != -1:
            self.__matriz[pos] = linha
        else:
            posFila = self.__getPosicaoInserirFila()
            self.__tags[posFila] = tag
            self.__matriz[posFila] = linha

    # Insere um dado lido da memória na cache.
    #
    # @param address : int - endereço de origem do dado.
    # @param valor : int - valor propriamente dito
    #
    # return bool.
    #
    def setDado(self, address, valor):
        tag = self.getBitsTag(address)
        linha = self.buscaTag(tag)

        if linha == -1:
            return CACHE_MISS
        else:
            offset = self.getBitsOffset(address)
            self.__matriz[linha][offset] = valor
            return CACHE_HIT

    # Busca posição (linha) onde está a tag na cache. Se não
    # encontrar, retorna -1.
    #
    # @param tag : int - tag a ser buscada
    #
    # @return int.
    #
    def buscaTag(self, tag):
        for i in range(self.__numLinhas):
            if tag == self.__tags[i]:
                return i
        return -1


### FUNÇÕES DE INTERFACE (requisitos do Dr. Saúde):


def createTACache(c, l):
    return TACache(c, l)


def getTACacheCapacity(tac):
    return tac.getCapacidade()


def getTACacheLineSize(tac):
    return tac.getTamLinha()


def getTACacheData(tac, address, value):
    return tac.getDado(address, value)


def setTACacheLine(tac, address, line):
    tac.setLine(address, line)


def setTACacheData(tac, address, value):
    return tac.setDado(address, value)
