from sys import stderr

from src.SACache import SACache
from src.Relatorio import Relatorio



class CompilationError(BaseException):
    def __init__(self, name, line, msg):
        self.__name = name
        self.__line = line
        self.__msg = msg

    def getMessage(self):
        msg =  'Erro durante a compilação:\n'
        msg += '  Linha:    {}\n'.format(self.__line)
        msg += '  Tipo:     {}\n'.format(self.__name)
        msg += '  Detalhes: {}\n'.format(self.__msg)
        return msg



class Interpreter:

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
        # Cria um processador com n núcleos, sendo que cada núcleo terá uma hierarquia de
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

    def __init__(self, arquivo):
        self.__L1D = None
        self.__L1I = None
        self.__L2 = None
        self.__L3 = None
        self.__MP = None
        self.__MEM = None
        self.__PROC = None

        self.__relatorio = Relatorio()
        self.__comandos = self.__compilarArquivo(arquivo)

        try:
            self.__crirarHierarquia()
        except BaseException as e:
            stderr.writelines(e.args[0] + '\n')
            exit(1)

        try:
            self.__executarComandos()
        except BaseException as e:
            stderr.writelines(e.args[0] + '\n')


    def __compilarArquivo(self, arquivo):
        lines = []
        for num, line in enumerate(arquivo):
            if line[0] == '#':
                # Comentário, ignora e busca próxima linha.
                continue
            else:
                try:
                    # Verifica o comando, senão lança erro de compilação.
                    cmd = self.__extrairComando(line)
                    lines.append(cmd)
                except BaseException as e:
                    erro = CompilationError(type(e), num+1, e)
                    stderr.writelines(erro.getMessage())
                    exit(1)
        return lines

    def __extrairComando(self, string):
        lista = string.split()
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

                print('Criado cache L1d (lookup {}, offset {}, tag {})'.format(
                    aux.getTamLookup(), aux.getTamOffset(), aux.getTamTag()
                    )
                )

            elif i == 1:
                c, a, l = args
                aux = self.__L1I = SACache(c, a, l)

                print('Criado cache L1i (lookup {}, offset {}, tag {})'.format(
                    aux.getTamLookup(), aux.getTamOffset(), aux.getTamTag()
                    )
                )

            elif i == 2:
                c, a, l = args
                aux = self.__L2 = SACache(c, a, l)

                print('Criado cache L2 (lookup {}, offset {}, tag {})'.format(
                    aux.getTamLookup(), aux.getTamOffset(), aux.getTamTag()
                    )
                )

            elif i == 3:
                c, a, l = args
                aux = self.__L3 = SACache(c, a, l)

                print('Criado cache L3 (lookup {}, offset {}, tag {})'.format(
                    aux.getTamLookup(), aux.getTamOffset(), aux.getTamTag()
                    )
                )

            elif i == 4:
                '''
                ramsize, vmsize = args
                self.__MP = None # cria memoria princ.
                '''
                print('criar hierarquia passo 5')

            elif i == 5:
                '''
                self.__MEM = None # cria hierarquia
                '''
                print('criar hierarquia passo 6')

            elif i == 6:
                '''
                n = args
                self.__PROC = None # cria processador
                '''
                print('criar hierarquia passo 7')

            else:
                raise RuntimeError('Isso não deveria ter acontecido!')

    def __executarComandos(self):
        for i in range(7, len(self.__comandos)):
            cmd, args = self.__comandos[i]
            if cmd in ('cl1d','cl1i','cl2','cl3','cmp','cmem','cp'):
                raise RuntimeError('Comando de construção de hierarquia fora do lugar.')
            else:
                self.executarComando(cmd, args)

    def executarComando(self, cmd, args):
        relatorio = self.__relatorio

        if cmd not in ('ri', 'wi', 'rd', 'wd', 'asserti', 'assertd'):
            raise RuntimeError('Comando inválido.')

        elif cmd == 'ri':
            print(cmd)

        elif cmd == 'wi':
            print(cmd)

        elif cmd == 'rd':
            print(cmd)

        elif cmd == 'wd':
            print(cmd)

        elif cmd == 'asserti':
            print(cmd)

        elif cmd == 'assertd':
            print(cmd)

        else:
            raise RuntimeError('Isso não deveria ter acontecido!')








