from src.util import isPotenciaDois
from src.util import log2
from src.util import Word
from src.constantes import *


class TACache:
    # Construtor da cache totalmente associativa.
    #
    # @param capacidade : int - tamanho total em bytes, deve ser potência de 2 e
    #                           múltiplo de tamLinha.
    #
    # @param tamLinha : int - número de bytes por linha, deve ser potência de 2.
    #
    # @raise TypeError, ValueError.
    #
    def __init__(self, capacidade, tamLinha):
        self.__verificaArgumentos(capacidade, tamLinha)

        self.__capacidade = capacidade
        self.__tamLinha = tamLinha
        self.__numLinhas = capacidade // tamLinha
        self.__numColunas = tamLinha // 4
        self.__tamOffset = log2(self.__numColunas)

        self.__tags = [None] * self.__numLinhas

        # cada célula tem uma word de 4 bytes (32 bits)
        self.__matriz = [[Word(0)] * self.__numColunas for i in range(self.__numLinhas)]

        self.__posInserirFila = 0

    # Lança exceção se algum dos argumentos do construtor estiver errado.
    # 
    # @param capacidade : int - mesmo do construtor.
    # @param tamLinha : int - mesmo do construtor.
    #
    # @raise TypeError, ValueError.
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
    # @raise TypeError, ValueError.
    #
    # @return int.
    #
    def getBitsOffset(self, address):
        self.__verificaAddress(address)
        return address & (self.__numColunas - 1)

    # Obtém os bits de tag de um dado endereço. 
    #
    # @param address : int - endereço de 32 bits (4 bytes).
    #
    # @raise TypeError, ValueError.
    #
    # @return int.
    #
    def getBitsTag(self, address):
        self.__verificaAddress(address)
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
    # @param word : Word - inteiro de 32 bits passado por valor.
    #
    # @raise TypeError, ValueError, IndexError.
    #
    # @return bool.
    #
    def getDado(self, address, word):
        self.__verificaAddress(address)
        self.__verificaWord(word)

        tag = self.getBitsTag(address)
        offset = self.getBitsOffset(address)

        if offset % 4 != 0:
            raise IndexError('Offset deve ser múltiplo de 4.')

        pos = self.buscaTag(tag)

        if pos != -1:
            celula = self.__matriz[pos][offset]
            word.set(celula.get())
            return CACHE_HIT
        else:
            return CACHE_MISS

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
        self.__verificaLinha(linha)

        tag = self.getBitsTag(address)
        pos = self.buscaTag(tag)
        linha = [word.copy() for word in linha]

        if pos != -1:
            self.__matriz[pos] = linha
        else:
            posFila = self.__getPosicaoInserirFila()
            self.__tags[posFila] = tag
            self.__matriz[posFila] = linha

    # Insere um dado lido da memória na cache.
    #
    # @param address : int - endereço de origem do dado.
    # @param word : Word - dado a ser inserido.
    #
    # @raise TypeError, ValueError.
    #
    # return bool.
    #
    def setDado(self, address, word):
        self.__verificaAddress(address)
        self.__verificaWord(word)

        tag = self.getBitsTag(address)
        linha = self.buscaTag(tag)

        if linha == -1:
            return CACHE_MISS
        else:
            offset = self.getBitsOffset(address)

            if offset % 4 != 0:
                raise IndexError('Offset deve ser múltiplo de 4.')

            self.__matriz[linha][offset] = word.copy()
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

    # Verifica corretude da linha da memória.
    #
    # @param linha : list - lista de words.
    #
    # @raise TypeError, IndexError.
    #
    # @return None.
    #
    def __verificaLinha(self, linha):
        if type(linha) != list:
            raise TypeError('Linha deve ser list.')

        if len(linha) > self.__tamLinha:
            raise IndexError('Linha é maior que a capacidade da cache.')

        for item in linha:
            if type(item) != Word:
                raise TypeError('Elementos da linha devem ser Word.')


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
