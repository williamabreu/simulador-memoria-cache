from src.SACache import SACache
from src.Cache import Cache
from src.MainMemory import MainMemory
from src.Memory import Memory
from src.Processor import Processor
from src.Relatorio import Relatorio
from src.util import Word
from src.constantes import *



class CompilationError(BaseException):
    # Construtor da exceção de compilação do arquivo de comandos
    # @param objeto : object - objeto de origem da erro.
    # @param linha : int - linha do arquivo de comandos com erro.
    # @param arquivo : open() - arquivo de comandos.
    #
    def __init__(self, objeto, linha, arquivo):
        tipo = str(type(objeto))
        start = tipo.index("'")
        end = tipo.index("'", start+1)
        tipo = tipo[start+1:end]

        self.__tipo = tipo
        self.__linha = linha
        self.__arquivo = arquivo
        self.__detalhes = str(objeto)

    # Retorna a mensagem de erro formatada.
    # @return str.
    #
    def getMessage(self):
        msg =  'Erro durante a compilação:\n'
        msg += '  Arquivo de comandos "{}", linha {}\n'.format(self.__arquivo.name, self.__linha)
        msg += '    {}'.format(self.__getFileLine())
        msg += '    ^\n'
        msg += '{}: {}'.format(self.__tipo, self.__detalhes)
        return msg

    # Método para auxiliar na busca da linha que deu erro no arquivo,
    # para exibir na mensagem e facilitar a correção do mesmo.
    # @return str.
    #
    def __getFileLine(self):
        self.__arquivo.seek(0)
        for i in range(self.__linha):
            linha = self.__arquivo.readline()
        return linha




class Interpreter:
    # estático.
    comandosValidos = {
        'cl1d': '<c> <a> <l>',
        # Cria uma variável L1D que é uma cache associativa por conjuntos com
        # capacidade c, associatividade a e l bytes por linha.

        'cl1i': '<c> <a> <l>',
        # Cria uma variável L1I que é uma cache associativa por conjuntos com
        # capacidade c, associatividade a e l bytes por linha.

        'cl2': '<c> <a> <l>',
        # Cria uma variável L2 que é uma cache associativa por conjuntos com capacidade
        # c, associatividade a e l bytes por linha.

        'cl3': '<c> <a> <l>',
        # Cria uma variável L3 que é uma cache associativa por conjuntos com capacidade
        # c, associatividade a e l bytes por linha.

        'cmp': '<ramsize> <vmsize>',
        # Cria uma variável MP que é uma memória principal com ramsize
        # bytes de RAM e vmsize bytes de memória virtual.

        'cmem': '',
        # Cria uma variável MEM que é uma hierarquia de memória criada com L1D, L1I, L2, L3
        # e MP já criados anteriormente.

        'cp': '<n>',
        # Cria um __processador com n núcleos, sendo que cada núcleo terá uma hierarquia de
        # memória baseada em MEM.

        'ri': '<n> <addr>',
        # Lê a instrução de endereço addr na hierarquia de memória do núcleo n.

        'wi': '<n> <addr> <value>',
        # Escreve a instrução value no endereço addr pela hierarquia de
        # memória do núcleo n.

        'rd': '<n> <addr>',
        # Lê o dado de endereço addr na hierarquia de memória do núcleo n.

        'wd': '<n> <addr> <value>',
        # Escreve o dado value no endereço addr pela hierarquia de memória
        # do núcleo n.

        'asserti': '<n> <addr> <level> <value>',
        # Lê a instrução de endereço addr na hierarquia de
        # memória do núcleo n e verifica se o valor foi lido do nível level (variando de 1 a 5 conforme
        # retorno de getInstruction) e o valor lido é igual a value.

        'assertd': '<n> <addr> <level> <value>'
        # Lê o dado de endereço addr na hierarquia de memória
        # do núcleo n e verifica se o valor foi lido do nível level (variando de 1 a 5 conforme retorno de
        # getData) e o valor lido é igual a value.
    }

    # Inicializa o interpretador.
    # @param arquivo : open() - buffer do arquivo de comandos.
    #
    def __init__(self, arquivo):
        self.__L1D = None
        self.__L1I = None
        self.__L2 = None
        self.__L3 = None
        self.__MP = None
        self.__MEM = None
        self.__PROC = None

        self.__relatorio = None
        self.__comandos = self.__compilarArquivo(arquivo)

        self.__crirarHierarquia()
        self.__executarComandos()

    # Retorna uma referência para o objeto que compõe o relatório
    # de execução.
    # @return Relatorio.
    #
    def getRelatorio(self):
        return self.__relatorio

    # Faz a análise sintática/léxica do arquivo de comandos
    # e compila tudo em forma de lista para o interpretador
    # executar.
    # @param arquivo : open() - buffer do arquivo.
    # @return list.
    #
    def __compilarArquivo(self, arquivo):
        lines = []
        for num, line in enumerate(arquivo):
            lista = line.split()
            if lista == [] or line[0] == '#':
                # Vazio ou Comentário, ignora e busca próxima linha.
                continue
            else:
                try:
                    # Verifica o comando, senão lança erro de compilação.
                    cmd = self.__extrairComando(lista)
                    lines.append(cmd)
                except BaseException as e:
                    erro = CompilationError(e, num+1, arquivo)
                    raise erro
        return lines

    # Extrai o comando de uma string para um formato que o interpretador
    # consegue executar (chave da instrução + argumentos inteiros).
    # @param lista : list - lista de string.
    # @return tuple.
    #
    def __extrairComando(self, lista):
        cmd = lista.pop(0)
        args = lista

        if cmd in self.comandosValidos:
            length = len(self.comandosValidos[cmd].split())
            if length == len(args):
                return cmd, map(int, args)
            else:
                raise IndexError('Número de args incorreto. Esperado {}, dado {}.'.format(length, len(args)))
        else:
            raise KeyError('{} não é um comando válido.'.format(cmd))

    # Cria a hierarquia toda executando os comandos na ordem correta.
    # Inicializa os atributos conforme comandos do arquivo.
    # @return None.
    #
    def __crirarHierarquia(self):
        # 7 comandos executados em ordem.
        ordem = ('cl1d','cl1i','cl2','cl3','cmp','cmem','cp')

        for i in range(7):
            cmd, args = self.__comandos[i]
            if cmd != ordem[i]:
                raise RuntimeError('Construção da hierarquia falhou (comandos fora da ordem definida).')

            elif i == 0:
                c, a, l = args
                aux = self.__L1D = SACache(c, a, l)

                print('Criado cache L1d (lookup {}, offset {}, tag {}).'.format(
                    aux.getTamLookup(), aux.getTamOffset(), aux.getTamTag()
                    )
                )

            elif i == 1:
                c, a, l = args
                aux = self.__L1I = SACache(c, a, l)

                print('Criado cache L1i (lookup {}, offset {}, tag {}).'.format(
                    aux.getTamLookup(), aux.getTamOffset(), aux.getTamTag()
                    )
                )

            elif i == 2:
                c, a, l = args
                aux = self.__L2 = SACache(c, a, l)

                print('Criado cache L2 (lookup {}, offset {}, tag {}).'.format(
                    aux.getTamLookup(), aux.getTamOffset(), aux.getTamTag()
                    )
                )

            elif i == 3:
                c, a, l = args
                aux = self.__L3 = SACache(c, a, l)

                print('Criado cache L3 (lookup {}, offset {}, tag {}).'.format(
                    aux.getTamLookup(), aux.getTamOffset(), aux.getTamTag()
                    )
                )

            elif i == 4:
                ramsize, vmsize = args
                aux = self.__MP = MainMemory(ramsize, vmsize)

                print('Criada memória principal (capacidade {} bytes, endereços [0, {}]).'.format(
                    aux.getTamTotal(), aux.getTamTotal() - 1
                    )
                )

            elif i == 5:
                cache = Cache(self.__L1D, self.__L1I, self.__L2, self.__L3)
                memprinc = self.__MP
                self.__relatorio = Relatorio(cache, memprinc)
                self.__MEM = Memory(cache, memprinc)

                print('Criada hierarquia de memória.')

            elif i == 6:
                n = tuple(args)[0]
                aux = self.__PROC = Processor(self.__MEM, n)

                print('Criada CPU com {} núcleos.'.format(aux.getNumCores()))

            else:
                raise RuntimeError('Isso não deveria ter acontecido!')

    # Executa todos os comandos de leitura/escrita do arquivo de uma vez.
    # @return None.
    #
    def __executarComandos(self):
        for i in range(7, len(self.__comandos)):
            cmd, args = self.__comandos[i]
            if cmd in ('cl1d','cl1i','cl2','cl3','cmp','cmem','cp'):
                raise RuntimeError('Comando de construção de hierarquia fora do lugar.')
            else:
                self.executarComando(cmd, args)

    # Executa um comando só, passando a instrução e a lista de argumentos.
    # @param cmd : str - chave do comando.
    # @param args : list - lista de parâmetros.
    # @return None.
    #
    def executarComando(self, cmd, args):
        if cmd not in ('ri', 'wi', 'rd', 'wd', 'asserti', 'assertd'):
            raise RuntimeError('Comando inválido.')

        elif cmd == 'ri':
            n, addr = args
            self.ri(n, addr)

        elif cmd == 'wi':
            n, addr, value = args
            self.wi(n, addr, value)

        elif cmd == 'rd':
            n, addr = args
            self.rd(n, addr)

        elif cmd == 'wd':
            n, addr, value = args
            self.wd(n, addr, value)

        elif cmd == 'asserti':
            n, addr, level, value = args
            self.asserti(n, addr, level, value)

        elif cmd == 'assertd':
            n, addr, level, value = args
            self.assertd(n, addr, level, value)

        else:
            raise RuntimeError('Isso não deveria ter acontecido!')

    # Executa comando específico.
    #
    def ri(self, n, addr):
        pointer = Word()
        x = self.__PROC.getCore(n).getInstrucao(addr, pointer)

        if x == FOUND_IN_L1:
            self.__relatorio.hit1()
        elif x == FOUND_IN_L2:
            self.__relatorio.hit2()
        elif x == FOUND_IN_L3:
            self.__relatorio.hit3()
        elif x == FOUND_IN_MEM:
            self.__relatorio.hit4()
        else:
            self.__relatorio.erro()

        if pointer.get() != None:
            print('Obtida instrução "{}" no nivel {}'.format(pointer.get(), x))
        else:
            print('Endereço fora da faixa.')

    # Executa comando específico.
    #
    def wi(self, n, addr, value):
        self.wd(n, addr, value)

    # Executa comando específico.
    #
    def rd(self, n, addr):
        pointer = Word()
        x = self.__PROC.getCore(n).getDado(addr, pointer)

        if x == FOUND_IN_L1:
            self.__relatorio.hit1()
        elif x == FOUND_IN_L2:
            self.__relatorio.hit2()
        elif x == FOUND_IN_L3:
            self.__relatorio.hit3()
        elif x == FOUND_IN_MEM:
            self.__relatorio.hit4()
        else:
            self.__relatorio.erro()

        if pointer.get() != None:
            print('Obtido dado "{}" no nivel {}'.format(pointer.get(), x))
        else:
            print('Endereço fora da faixa.')

    # Executa comando específico.
    #
    def wd(self, n, addr, value):
        pointer = Word(value)
        self.__PROC.getCore(n).setDado(addr, pointer)

        print('Salvo "{}" no endereço {} da memória.'.format(value, addr))

    # Executa comando específico.
    #
    def asserti(self, n, addr, level, value):
        pointer = Word()
        x = self.__PROC.getCore(n).getInstrucao(addr, pointer)

        if x == level and pointer.get() == value.get():
            print('OK.')
        else:
            print('ERRADO.')

    # Executa comando específico.
    #
    def assertd(self, n, addr, level, value):
        pointer = Word()
        x = self.__PROC.getCore(n).getDado(addr, pointer)

        if x == level and pointer.get() == value.get():
            print('OK.')
        else:
            print('ERRADO.')