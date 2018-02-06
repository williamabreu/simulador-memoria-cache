from src.SACache import SACache

class Cache:
    # estático:
    __l3Instace = None      # instância única
    __l2Reference = None    # referência para cópia
    __l1iReference = None   # referência para cópia
    __l1dReference = None   # referência para cópia

    # Cosntrutor da cache inclusiva de 3 níveis.
    #
    # @param l1d : SACache - cache L1 de dados.
    # @param l1i : SACache - cache L1 de instruções.
    # @param l2 : SACache - cache L2.
    # @param l3 : SACache - cache L3.
    #
    # @raise PermissionError, TypeError, ValueError.
    #
    def __init__(self, l1d, l1i, l2, l3):
        if Cache.__l3Instace != None and Cache.__l3Instace != l3:
            # Só cria um, o resto deve ser cópia (estruturas iguais).
            raise PermissionError('Já existe uma instância de Cache, utilize duplicate.')
        elif Cache.__l3Instace == None:
            # Primeira instância.
            self.__veririficaArgumentos(l1d, l1i, l2, l3)
            Cache.__l1dReference = l1d
            Cache.__l1iReference = l1i
            Cache.__l2Reference = l2
            Cache.__l3Instace = l3

        self.__l1d = l1d
        self.__l1i = l1i
        self.__l2 = l2
        self.__l3 = l3

    # Lança exceção se algum dos argumentos do construtor estiver errado.
    #
    # @param l1d : SACache - mesmo do construtor.
    # @param l1i : SACache - mesmo do construtor.
    # @param l2 : SACache - mesmo do construtor.
    # @param l3 : SACache - mesmo do construtor.
    #
    # @raise TypeError, ValueError.
    #
    # @return None.
    #
    def __veririficaArgumentos(self, l1d, l1i, l2, l3):
        if type(l1d) != SACache:
            raise TypeError('L1 dados deve ser SACache.')

        if type(l1i) != SACache:
            raise TypeError('L1 intruções deve ser SACache.')

        if type(l2) != SACache:
            raise TypeError('L2 deve ser SACache.')

        if type(l3) != SACache:
            raise TypeError('L3 deve ser SACache.')

        if sorted([l1d, l2, l3]) != [l1d, l2, l3]:
            raise ValueError('Tamanhos de linha inválidos, devem ser crescentes.')

        if sorted([l1i, l2, l3]) != [l1i, l2, l3]:
            raise ValueError('Tamanhos de linha inválidos, devem ser crescentes.')

    # Get instance.
    # @return SACache.
    #
    def getL3(self):
        return self.__l3

    # Get instance.
    # @return SACache.
    #
    def getL2(self):
        return self.__l2

    # Get instance.
    # @return SACache.
    #
    def getL1i(self):
        return self.__l1i

    # Get instance.
    # @return SACache.
    #
    def getL1d(self):
        return self.__l1d

    # Cria uma nova Cache com a mesma estrutura, mas vazia.
    #
    # @raise ModuleNotFoundError.
    #
    # return Cache.
    #
    def duplicate(self):
        if Cache.__l3Instace == None:
            raise ModuleNotFoundError('Não existe instância a ser duplicada.')
        else:
            l1d = Cache.__l1dReference.duplicate()
            l1i = Cache.__l1iReference.duplicate()
            l2 = Cache.__l2Reference.duplicate()
            l3 = Cache.__l3Instace
            return Cache(l1d, l1i, l2, l3)

    # Representação em string.
    #
    # @return str.
    #
    def __repr__(self):
        out = '[L1 data] {}\n{}\n{}\n'.format('{', self.__l1d, '}')
        out += '[L1 instruction] {}\n{}\n{}\n'.format('{', self.__l1i, '}')
        out += '[L2] {}\n{}\n{}\n'.format('{', self.__l2, '}')
        out += '[L3] {}\n{}\n{}'.format('{', self.__l3, '}')

        out = out.replace('{\n', '{\n\t')
        out = out.replace(':\n', ':\n\t')
        out = out.replace(']\n', ']\n\t')
        out = out.replace(']\n\t}', ']\n}')

        return out

    # Linha de dados.
    # Método para inserir em todos os níveis da cache uma linha buscada na
    # memória através do endereço dado, mantendo a coerência da cache inclusiva,
    # pois os tamanhos de linha de cada nível pode ser diferente.
    #
    # @param mainMem : MainMemory - referência para a memória principal.
    # @param address : int - endreço de 32 bits.
    #
    # @return None.
    #
    def setLineCacheData(self, mainMem, address):
        raise NotImplementedError('Método não implementado.')

    # Linha de instruções.
    # Método para inserir em todos os níveis da cache uma linha buscada na
    # memória através do endereço dado, mantendo a coerência da cache inclusiva,
    # pois os tamanhos de linha de cada nível pode ser diferente.
    #
    # @param mainMem : MainMemory - referência para a memória principal.
    # @param address : int - endreço de 32 bits.
    #
    # @return None.
    #
    def setLineCacheInst(self, mainMem, address):
        raise NotImplementedError('Método não implementado.')

    # Busca um dado na cache pelo endereço, retorna o nível em que foi
    # encontrado.
    #
    # @param mainMem : MainMemory - referência para a memória principal.
    # @param address : int - endreço de 32 bits.
    # @param value : Word - palavra a ser retornada de 32 bits.
    #
    # @return int.
    #
    def getCacheData(self, mainMem, address, value):
        raise NotImplementedError('Método não implementado.')

    # Busca uma instrução na cache pelo endereço, retorna o nível em que foi
    # encontrado.
    #
    # @param mainMem : MainMemory - referência para a memória principal.
    # @param address : int - endreço de 32 bits.
    # @param value : Word - palavra a ser retornada de 32 bits.
    #
    # @return int.
    #
    def getCacheInst(self, mmem, address, value):
        raise NotImplementedError('Método não implementado.')

    # Insere um dado em toda a hierarquia de cache inclusivo. Retorna
    # o nível em que o valor foi encontrado na hierarquia.
    #
    # @param address : int - endereço de 32 bits.
    # @param value : Word - palavra de 32 bits de retorno.
    #
    # @return int.
    def setCacheData(self, address, value):
        raise NotImplementedError('Método não implementado.')

    # Insere uma instrução em toda a hierarquia de cache inclusivo. Retorna
    # o nível em que o valor foi encontrado na hierarquia.
    #
    # @param address : int - endereço de 32 bits.
    # @param value : Word - palavra de 32 bits de retorno.
    #
    # @return int.
    def setCacheInst(self, address, value):
        raise NotImplementedError('Método não implementado.')


### FUNÇÕES DE INTERFACE (requisitos do Dr. Saúde):


def createCache(l1d, l1i, l2, l3):
    return Cache(l1d, l1i, l2, l3)

def fetchCacheData(c, mmem, address):
    c.setLineCacheData(mmem, address)


def fetchCacheInstruction(c, mmem, address):
    c.setLineCacheData(mmem, address)


def getCacheData(c, mmem, address, value):
    return c.getCacheData(mmem, address, value)


def getCacheInstruction(c, mmem, address, value):
    return c.getCacheInst(mmem, address, value)


def setCacheData(c, address, value):
    return c.setCacheData(address, value)


def setCacheInstruction(c, address, value):
    return c.setCacheInst(address, value)


def duplicateCache(c):
    return c.duplicate()