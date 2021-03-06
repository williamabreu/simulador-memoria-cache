# Verifica se x é potência de 2.
# 
# @param x : int - número a ser verificado. 
#
# @return bool.
#
def isPotenciaDois(x):
    if x == 0:
        return False
    
    while x != 1:
        if x % 2 == 0:
            x >>= 1
        else:
            return False
    
    return True


# Cacula logaritimo inteiro na base 2.
#
# @param x : int - número de referência do cálculo.
#
# @return int.
#
def log2(x):
    if x == 0:
        raise ArithmeticError('Impossível.')
    
    cont = 0
    
    while x != 1:
        if x % 2 == 0:
            x >>= 1
            cont += 1
        else:
            raise ArithmeticError('Impossível.')
    
    return cont


class Word:
    # Cria uma palavra de 32 bits (4 bytes).
    #
    # @param valor : int - valor da palavra (usando inteiro).
    #
    # @raise TypeError, ValueError.
    #
    def __init__(self, valor=None):
        if type(valor) != int and valor != None:
            raise TypeError('Valor da word deve ser int.')

        self.__valor = None

        if valor != None:
            self.set(valor)
    
    # Método set, para mudar o valor da variável.
    #
    # @param valor : int - novo valor.
    #
    # @raise TypeError, ValueError.
    #
    # @return None.
    #
    def set(self, valor):
        if type(valor) != int and valor != None:
            raise TypeError('Valor da word deve ser int.')
        if valor.bit_length() > 32:
            raise ValueError('Tamanho da word deve ser no máx. 32 bits.')

        self.__valor = valor
    
    # Método para obter o valor da variável.
    #
    # @return int.
    #
    def get(self):
        return self.__valor

    # Método para criar cópia.
    #
    # @return Word.
    #
    def copy(self):
        return Word(self.__valor)

    # Representação.
    #
    # @return str.
    #
    def __repr__(self):
        return str(self.__valor)


