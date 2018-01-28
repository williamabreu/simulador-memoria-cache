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
		self.__tamTag = 32 - self.__tamOffset
		
		self.__tags = [0] * self.__numLinhas		
		# cada célula tem 4 bytes (32 bits)
		self.__matriz = [[0] * self.__tamLinha for i in range(self.__numLinhas)] 
		
		self.__posInserirFila = 0
	
	# Lança exceção se algum dos argumentos do construtor estiver errado.
	# 
	# @param capacidade : int - mesmo do construtor.
	# @param numLinhas : int - mesmo do construtor.
	#
	# @raise ArgumentError.
	#
	# @return None.
	#
	def __verificaArgumentos(capacidade, numLinhas):
		if type(numLinhas) != int:
			raise ArgumentError('Número de Linhas inválido, deve ser inteiro.')
		
		if not self.isPotenciaDois(numLinhas):
			raise ArgumentError('Número de Linhas inválido, deve ser potência de 2.')
		
		if type(capacidade) != int:
			raise ArgumentError('Capacidade inválida, deve ser inteiro.')
		
		if not self.isPotenciaDois(capacidade):
			raise ArgumentError('Capacidade inválida, deve ser potência de 2.')
			
		if capacidade % numLinhas != 0:
			raise ArgumentError('Capacidade inválida, deve ser múltiplo de numLinhas.')
	
	# Obtém a posição correta para se inserir uma nova tag na lista (fila circular)
	#
	# @return int.
	#
	def getPosicaoInserirFila(self):
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
	
	# Obtém os bits de offset de um dado endereço. 
	#
	# @param address : int - endereço de 32 bits (4 bytes).
	#
	# @return int.
	#
	def getBitsOffset(self, address):
		return address & (self.tamLinha - 1)
	
	# Obtém os bits de tag de um dado endereço. 
	#
	# @param address : int - endereço de 32 bits (4 bytes).
	#
	# @return int.
	#
	def getBitsTag(self, address):
		return address >> self.tamOffset	
	
	# Obtém o dado salvo do endereço. 
	#
	# @param address : int - endereço de 32 bits (4 bytes).
	# @param value : INT - inteiro para passagem por valor.
	#
	# @return bool.
	#
	def getDado(self, address, value):
		tag = self.getBitsTag(address)
		offset = self.getBitsOffset(adrress)
		
		pos = self.buscaTag(tag)

		if pos != -1:
			value.set(matriz[i][offset])
			return CACHE_HIT
		else:	
			return CACHE_MISS 
	
	def __repr__(self):
		out = ''
		for i in range(self.__numLinhas):
			out += str(tags[i]) + ' ' + str(matriz[i]) + '\n'
		return out

	def setDado(self, address, valor):
		tag = self.getBitsTag(address)
		offset = self.getBitsOffset(address)
		pos = self.getPosicaoInserirFila()
		linha = self.buscaTag(tag)
		
		if linha == -1:
			return False
			# não sei se tá certo!
		else:
			matriz[pos][offset] = valor
			return True

	def setLine(self, address, linha):
		tag = self.getBitsTag(address)
		offset = self.getBitsOffset(address)
		pos = self.buscaTag(tag)
		
		if pos != -1:
			matriz[pos] = linha
		else:
			posFila = self.getPosicaoInserirFila()
			tags[posFila] = tag
			matriz[posFila] = linha


	def buscaTag(self, tag):
		for i in range(self.__numLinhas):
			if tag == self.__tags[i]:
				return i
		
		return -1


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
# @raise TypeError.
#
# @return int.
#
def getTACacheCapacity(tac):
	if type(tac) == TACache:
		return tac.getCapacidade()
	else:
		raise TypeError('Argumento deve ser TACache.')


# Obtém o valor do tamanho da linha da cache.
# 
# @param tac : TACache - referência para cache.
# 
# @raise TypeError.
#
# @return int.
#
def getTACacheLineSize(tac):
	if type(tac) == TACache:
		return tac.getTamanhoLinha()
	else:
		raise TypeError('Argumento deve ser TACache.')

# Tenta obter um valor na cache pelo endereço passado.
# 
# @param tac : TACache - referência para cache.
# @param value : INT - inteiro pora passagem por valor.
# 
# @raise TypeError.
#
# @return bool.
#
def getTACacheData(tac, address, value):
	if type(tac) == TACache and type(value) == INT:
		return tac.getDado(address, value)
	else:
		raise TypeError('Argumentos inválidos.')
		






