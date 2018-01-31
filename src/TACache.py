import math
import util

# Constantes:
CACHE_MISS = False
CACHE_HIT = True


class TACache:
    # Construtor da cache totalmente associativa.
    #
    # @param capacidade : int - tamanho total em bytes, deve ser potência de 2 e
    #                           múltiplo do número de linhas.
    #
    # @param numLinhas : int - número de bytes por linha, deve ser potência de 2.
    #
    def __init__(self, capacidade, numLinhas):
        self.__verificaArgumentos(capacidade, numLinhas)

        self.__capacidade = capacidade
        self.__numLinhas = numLinhas
        self.__tamLinha = capacidade // numLinhas
        self.__tamOffset = int(math.log(self.__tamLinha, 2))

        self.__tags = [None] * self.__numLinhas

        # cada célula tem 4 bytes (32 bits)
        self.__matriz = [[None] * self.__tamLinha for i in range(self.__numLinhas)]

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
    def __verificaArgumentos(self, capacidade, numLinhas):
        if type(numLinhas) != int:
            raise ValueError('Número de Linhas inválido, deve ser inteiro.')

        if not util.isPotenciaDois(numLinhas):
            raise ValueError('Número de Linhas inválido, deve ser potência de 2.')

        if type(capacidade) != int:
            raise ValueError('Capacidade inválida, deve ser inteiro.')

        if not util.isPotenciaDois(capacidade):
            raise ValueError('Capacidade inválida, deve ser potência de 2.')

        if capacidade % numLinhas != 0:
            raise ValueError('Capacidade inválida, deve ser múltiplo de numLinhas.')

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
    def getTamanhoLinha(self):
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
        return address & (self.__tamLinha - 1)

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
        for i in range(1, self.__numLinhas - 1):
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
    # @param valor : list - valores da linha da memória.
    #
    # return None.
    #
    def setLine(self, address, linha):
        tag = self.getBitsTag(address)
        pos = self.buscaTag(tag)

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


# Cria nova cache totalmente associativa.
# 
# @param c : int - capacidade.
# @param l : int - número de linhas.
# 
# @return TACache.
#
def createTACache(c, l):
    return TACache(c, l)


# Obtém o valor da capacidade da cache.
# 
# @param tac : TACache - referência para cache.
#
# @return int.
#
def getTACacheCapacity(tac):
    return tac.getCapacidade()


# Obtém o valor do tamanho da linha da cache.
# 
# @param tac : TACache - referência para cache.
#
# @return int.
#
def getTACacheLineSize(tac):
    return tac.getTamanhoLinha()


# Tenta obter um valor na cache pelo endereço passado.
# 
# @param tac : TACache - referência para cache.
# @param address : int - endereço de origem.
# @param value : INT - inteiro pora passagem por valor.
#
# @return bool.
#
def getTACacheData(tac, address, value):
    return tac.getDado(address, value)


# Insere uma linha da memória na cache.
#
# @param tac : TACache - referência para cache.
# @param address : int - endereço de origem.
# @param line : list - valores da linha da memória.
#
# return None.
#
def setTACacheLine(tac, address, line):
    tac.setLine(address, line)


# Insere um dado lido da memória na cache.
#
# @param tac : TACache - referência para cache.
# @param address : int - endereço de origem do dado.
# @param value : int - valor propriamente dito
#
# return bool.
#
def setTACacheData(tac, address, value):
    return tac.setDado(address, value)
