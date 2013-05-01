# -*- coding: utf-8 -*-

#no arquvivo sensor, tempo , pessoas
LIMITE = 5
import os
	

class leitorComandos:
	def __init__(self, endereco):
		self.endereco = endereco

	def lerArquivo(self):
		var = self.endereco
		if (os.path.isfile(var)):
			arquivo = open(var)
			lista =  arquivo.readlines()
			arquivo.close()
			return lista
		return []

class sensor:
	def __init__(self,name ):
		self.name= str(name)
		self.notifys = []
		self.pessoas = []
		self.mapa= {}

	def __str__(self):
		return self.name
	
	def receberComando(self, tempo, pessoas):
		#verificar Aumento
		print "recebendo comando "
		variacao = len(self.pessoas) - len (pessoas)
		if (variacao > 0 ): print "eh maior !!!!!"
		self.mapa[tempo] = pessoas
		return variacao

	#parametros (qual sensor? ,momento , qtd de variacao, id de cada pessoa (provavelmente lista)
	# vizinhos guardam o notify até receberem um alert
	def notify (self, sensor, momento, variacao, pessoas):
#		self.notify.append()
		print ("chgou um notify porr aqui no sensor  ",self.name, " do sensor ", sensor , " time ", momento)
		#avisa todos os vizinhos se aumentar o numero de pessoas em sua area de cobertura
		#return False


	#detectar um aumento de pessoas em sua regio e conter um notify dos vizinhos

	#mensagem enviada a um unico sensor na direção oposta (se recebeu notify do sul manda alert pra norte)
	#ao receber alert continuar mandadndo para o sentido" até o fim "
	def alert(self):
		return False


	#envido se ao somar as pessoas previstas para chegar neste sensor (pelo alert) for maior q o limite
	def alarm(self):
		return False



	

class rssf:
	def __init__(self, numeroLinhas, tamLinhas ):
		self.lista = [] 
		count = 1
		for linha in range (numeroLinhas):
			self.lista.append([])
		for linha in range(len(self.lista)):
			for j in range(max(tamLinhas)):
				if j < tamLinhas[linha]:
					self.lista[linha].append(sensor(count))
					count+= 1
				else:
					self.lista[linha].append(sensor("x"))
	
	def verModelo(self):	
		retorno = "modelo:\n\n"
		for linha in self.lista:
			for elemento in linha:
				retorno += str (elemento) + "\t"
			retorno+= "\n"
		print retorno
	
	def buscarSensor(self, num):
		for linha in range (len(self.lista)):
			for elemento in range (len(self.lista[linha])):
				if str(num) == str(self.lista[linha][elemento]):
					return linha, elemento
		return None

	def getLista(self):
		return self.lista
			

class Gerente:

	def __init__(self):
		#leitura de dados (linha e tamanhos das linhas)
		self.comandos = leitorComandos("entrada.txt")
		self.comandos = self.comandos.lerArquivo()
		self.linhas = int (self.comandos.pop(0))
		self.tamanhoLinhas = (self.comandos.pop(0)).split(" ")
		self.getListaNumeros()
		
		#criando rede de sensores
		self.redeSensores = rssf(self.linhas, self.tamanhoLinhas)
		self.redeSensores.verModelo()
		
		#iniciar interpretacao de comandos
		for comando in self.comandos:
			sensor , tempo, pessoas = self.interpretarComando(comando)
			linha, elemento = self.redeSensores.buscarSensor(sensor)
			variacao = self.redeSensores.getLista()[linha][elemento].receberComando(tempo, pessoas)
			#se aconteceu variacao, mandar notifys (todas direcoes)
			if variacao < 0: 
					if linha > 0:
						self.redeSensores.getLista()[linha-1][elemento].notify(sensor, tempo , variacao, pessoas)
						if elemento < len (self.redeSensores.getLista()[linha]):
							self.redeSensores.getLista()[linha-1][elemento+1].notify(sensor, tempo , variacao, pessoas)
						if elemento > 0:
							self.redeSensores.getLista()[linha-1][elemento-1].notify(sensor, tempo , variacao, pessoas)
					if linha < len (self.redeSensores.getLista()):
						self.redeSensores.getLista()[linha+1][elemento].notify(sensor, tempo , variacao, pessoas)
						if elemento > 0:
							self.redeSensores.getLista()[linha+1][elemento-1].notify(sensor, tempo , variacao, pessoas)
						if elemento < len (self.redeSensores.getLista()[linha]):
							self.redeSensores.getLista()[linha+1][elemento+1].notify(sensor, tempo , variacao, pessoas)
					if elemento > 0:
						self.redeSensores.getLista()[linha][elemento-1].notify(sensor, tempo , variacao, pessoas)
					if elemento < len(self.redeSensores.getLista()[linha]):
						self.redeSensores.getLista()[linha][elemento+1].notify(sensor, tempo , variacao, pessoas)


	def getListaNumeros(self):
		lista = []
		for i in self.tamanhoLinhas:
			lista.append(int (i))
		self.tamanhoLinhas = lista

	def interpretarComando (self, linha):
		lista = linha.split("-")
		sensor =int (lista.pop(0))
		tempo = float (lista.pop(0))
		pessoas = lista.pop(0)
		pessoas = pessoas.replace ("[","")
		pessoas = pessoas.replace ("]","")
		pessoas = pessoas.split(",")
		return sensor, tempo , pessoas 


Gerente()

