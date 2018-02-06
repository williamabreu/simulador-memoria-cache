from src.constantes import *

class Relatorio:
    # Cria um novo objeto responsável por montar o relatório
    # final do programa.
    # @param cache : Cache - cache 3 níveis do programa.
    # @param memprinc : MainMemory - memória do programa.
    #
    def __init__(self, cache, memprinc):
        self.__cache = cache
        self.__memprinc = memprinc

        self.__numHits1 = 0
        self.__numHits2 = 0
        self.__numHits3 = 0
        self.__numHits4 = 0
        self.__numErros = 0

    # Método para contabilizar um hit no nível L1.
    #
    def hit1(self):
        self.__numHits1 += 1

    # Método para contabilizar um hit no nível L2.
    #
    def hit2(self):
        self.__numHits2 += 1

    # Método para contabilizar um hit no nível L3.
    #
    def hit3(self):
        self.__numHits3 += 1

    # Método para contabilizar um hit na memória principal.
    #
    def hit4(self):
        self.__numHits4 += 1

    # Método para contabilizar um erro de endereço.
    #
    def erro(self):
        self.__numErros += 1

    # Método que gera o relatório final do programa,
    # em forma de tabela.
    # @return str.
    #
    def gerarRelatorio(self):
        MAX_LENGTH = 71
        TAM_CELULA = 18

        aux = self.__cache.getL1d()
        tupla = (aux.getCapacidade(), aux.getNumLinhas(), aux.getTamLinha())
        l1d = [str(x).center(TAM_CELULA) for x in tupla]

        aux = self.__cache.getL1i()
        tupla = (aux.getCapacidade(), aux.getNumLinhas(), aux.getTamLinha())
        l1i = [str(x).center(TAM_CELULA) for x in tupla]

        aux = self.__cache.getL2()
        tupla = (aux.getCapacidade(), aux.getNumLinhas(), aux.getTamLinha())
        l2 = [str(x).center(TAM_CELULA) for x in tupla]

        aux = self.__cache.getL3()
        tupla = (aux.getCapacidade(), aux.getNumLinhas(), aux.getTamLinha())
        l3 = [str(x).center(TAM_CELULA) for x in tupla]

        ram = str(self.__memprinc.getTamRam()).center(TAM_CELULA * 3)
        vm = str(self.__memprinc.getTamMemVirtual()).center(TAM_CELULA * 3)
        total = str(self.__memprinc.getTamTotal()).center(TAM_CELULA * 3)

        cod1 = str(FOUND_IN_L1).center(TAM_CELULA)
        cod2 = str(FOUND_IN_L2).center(TAM_CELULA)
        cod3 = str(FOUND_IN_L3).center(TAM_CELULA)
        cod4 = str(FOUND_IN_MEM).center(TAM_CELULA)
        cod5 = str(ADDRESS_OUT_OF_RANGE).center(TAM_CELULA)

        cont1 = str(self.__numHits1).center(TAM_CELULA * 2)
        cont2 = str(self.__numHits2).center(TAM_CELULA * 2)
        cont3 = str(self.__numHits3).center(TAM_CELULA * 2)
        cont4 = str(self.__numHits4).center(TAM_CELULA * 2)
        cont5 = str(self.__numErros).center(TAM_CELULA * 2)

        out =  ' RELATÓRIO FINAL DE EXECUÇÃO'.center(MAX_LENGTH) + '\n'
        out += '\n'
        out += '\n'
        out += 'Características da Cache'.center(MAX_LENGTH) + '\n'
        out += '+-------+--------------------+-------------------+--------------------+\n'
        out += '| Nível |     Capacidade     |  Associatividade  |  Tamanho da Linha  |\n'
        out += '+-------+--------------------+-------------------+--------------------+\n'
        out += '|  L1d  | {} | {}| {} |\n'.format(l1d[0], l1d[1], l1d[2])
        out += '|  L1i  | {} | {}| {} |\n'.format(l1i[0], l1i[1], l1i[2])
        out += '|  L2   | {} | {}| {} |\n'.format(l2[0], l2[1], l2[2])
        out += '|  L3   | {} | {}| {} |\n'.format(l3[0], l3[1], l3[2])
        out += '+-------+--------------------+-------------------+--------------------+\n'
        out += '\n'
        out += '\n'
        out += 'Características da Memória'.center(MAX_LENGTH) + '\n'
        out += '+-------+-------------------------------------------------------------+\n'
        out += '| Tipo  |                         Capacidade                          |\n'
        out += '+-------+-------------------------------------------------------------+\n'
        out += '| RAM   |    {}   |\n'.format(ram)
        out += '| VIRT. |    {}   |\n'.format(vm)
        out += '+-------+-------------------------------------------------------------+\n'
        out += '| total |    {}   |\n'.format(total)
        out += '+-------+-------------------------------------------------------------+\n'
        out += '\n'
        out += '\n'
        out += 'Resultados de hits/erros'.center(MAX_LENGTH) + '\n'
        out += '+-------+--------------------+----------------------------------------+\n'
        out += '| Nível |       Código       |            Contagem Total              |\n'
        out += '+-------+--------------------+----------------------------------------+\n'
        out += '|  L1   | {} |  {}  |\n'.format(cod1, cont1)
        out += '|  L2   | {} |  {}  |\n'.format(cod2, cont2)
        out += '|  L3   | {} |  {}  |\n'.format(cod3, cont3)
        out += '|  Mem. | {} |  {}  |\n'.format(cod4, cont4)
        out += '|  Erro |{}  |  {}  |\n'.format(cod5, cont5)
        out += '+-------+--------------------+----------------------------------------+\n'

        return out