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
			x //= 2
		else:
			return False
	
	return True


class INT:
	# Cria um inteiro por referência.
	#
	# @param valor  int - valor propriamente dito.
	#
	def __init__(self, valor):
		self.__valor = valor
	
	# Método set, para mudar o valor da variável.
	#
	# @param valor : int - novo valor.
	#
	# @return None.
	#
	def set(self, valor):
		self.valor = valor
	
	# Método para obter o valor da variável.
	#
	# @return int.
	#
	def get(self):
		return self.valor

