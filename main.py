from src.interpreter import Interpreter
from src.interpreter import CompilationError
from sys import argv
from sys import stderr
from traceback import print_exc


def main(filePath):
    arquivoComandos = None

    try:
        arquivoComandos = open(filePath)
    except BaseException as e:
        if arquivoComandos != None: arquivoComandos.close()
        raise e

    simulador = Interpreter(arquivoComandos)
    relatorio = simulador.getRelatorio().gerarRelatorio()

    print(relatorio)

    arquivoComandos.close()




if __name__ == '__main__':
    if len(argv) != 2:
        stderr.writelines('Parâmetro incorreto.\nUso:\n  python3 main.py <arquivo>\n')
        exit(1)

    try:
        main(argv[1])
    except CompilationError as e:
        stderr.writelines(e.getMessage())
        stderr.writelines('\n')
        exit(1)
    except:
        print_exc()
        exit(1)