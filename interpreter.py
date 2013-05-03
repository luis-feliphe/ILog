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
class Notify:
	def __init__(self, sensor, hora, variacao, pessoas):
		self.sensor = sensor
		self.hora = hora
		self.variacao = variacao
		self.pessoas = pessoas


class Alert: 
	def __init__ (self, qtd, tempo):
		self.qtd = qtd
		self.tempo = tempo

class sensor:
	def __init__(self,name ):
		self.name= str(name)
		self.notifys = []
		self.pessoas = []
		self.mapa= {}
		self.alerts = []

	def __str__(self):
		return self.name
	
	def receberComando(self, tempo, pessoas):
		alerta = None
		#verificar Aumento
		variacao =  len (pessoas) - len(self.pessoas)
		self.mapa[tempo] = pessoas
		tempoNotify = 0
		if (len (self.notifys) != 0):
			tempoNotify = self.notifys[0].hora
			alerta = self.notifys.pop(0)

		return variacao, alerta, tempoNotify


	def notify (self, dados):
		self.notifys.append(dados)

	#mensagem enviada a um unico sensor na direção oposta (se recebeu notify do sul manda alert pra norte)
	#ao receber alert continuar mandadndo para o sentido" até o fim "
	def alert(self,dados):
		print (self.name, "receive a alert",dados.qtd, " in ", dados.tempo, "sec")
		soma = dados.qtd
		for i in self.alerts:
			if i.tempo == dados.tempo: 
				soma+= i.qtd
		if soma >= LIMITE:
			print ("ALARM!!!: Sensor ", self.name)
			return True
		return False


	#envido se ao somar as pessoas previstas para chegar neste sensor (pelo alert) for maior q o limite
	def alarm(self):
		return False



	
class sensorNulo(sensor): #quando não existe sensor em determinada posicao
	def __init__(self,name ):
		self.name= str(name)
	def __str__(self):
		return self.name
	def receberComando(self, tempo, pessoas):
		return 0
	def notify (self, sensor):
		return False
	def alert(self, x):
		return False
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
					self.lista[linha].append(sensorNulo("x"))
	
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
			variacao, alerta, tempoNotify = self.redeSensores.getLista()[linha][elemento].receberComando(tempo, pessoas)
			#se aconteceu variacao, mandar notifys (todas direcoes)
			if variacao > 0: 
				dados = Notify (sensor, tempo, variacao, pessoas)	
				if linha > 0:
					self.redeSensores.getLista()[linha-1][elemento].notify(dados)
					if elemento < len (self.redeSensores.getLista()[linha]):
						self.redeSensores.getLista()[linha-1][elemento+1].notify(dados)
					if elemento > 0:
						self.redeSensores.getLista()[linha-1][elemento-1].notify(dados)
				if linha < len (self.redeSensores.getLista()):
					self.redeSensores.getLista()[linha+1][elemento].notify(dados)
					if elemento > 0:
						self.redeSensores.getLista()[linha+1][elemento-1].notify(dados)
					if elemento < len (self.redeSensores.getLista()[linha]):
						self.redeSensores.getLista()[linha+1][elemento+1].notify(dados)
				if elemento > 0:
					self.redeSensores.getLista()[linha][elemento-1].notify(dados)
				if elemento < len(self.redeSensores.getLista()[linha]):
					self.redeSensores.getLista()[linha][elemento+1].notify(dados)
			#TODO dar prioridade ao alert inves do notify
			if alerta != None:
				linhaAlerta, elementoAlerta = self.redeSensores.buscarSensor(alerta.sensor)
				cont=1
				cont2=-1 
				dados = Alert (variacao, tempo-tempoNotify)
				if linhaAlerta < linha :
					if elementoAlerta == elemento:
						#TODO envia alerta para elemento (linha +1 , elemento)
						while (linha + cont < len(self.redeSensores.getLista())):
							self.redeSensores.getLista()[linha+cont][elemento].alert(dados)
							cont+= 1
					if (elementoAlerta < elemento):
						#TODO envia alerta para elemento (linha +1 , elemento + 1)
						while (linha + cont < len(self.redeSensores.getLista()) and elemento+cont <= self.redeSensores.getLista()[linha]):
							self.redeSensores.getLista()[linha+cont][elemento+cont].alert(dados)
							cont+= 1
					if elementoAlerta > elemento :
						#TODO envia alerta para elemento (linha +1 , elemento - 1)
						while (linha + cont <= len(self.redeSensores.getLista()) and elemento+cont2 >= 0):
							self.redeSensores.getLista()[linha+cont][elemento+cont2].alert(dados)
							cont+= 1
							cont2-= 1
				if linhaAlerta > linha :
					if elementoAlerta == elemento:
						#TODO envia alerta para elemento (linha -1 , elemento)
						while (linha + cont >= 0):
							self.redeSensores.getLista()[linha+ cont2][elemento].alert(dados)
							cont2 -= 1
					if elementoAlerta < elemento :
						#TODO envia alerta para elemento (linha -1 , elemento + 1)
						while (linha + cont2 >= 0 and elemento+cont <= self.redeSensores.getLista()[linha]):
							self.redeSensores.getLista()[linha+ cont2][elemento+cont].alert(dados)
							cont+= 1
							cont2 -= 1
					if elementoAlerta > elemento :
						#TODO envia alerta para elemento (linha -1 , elemento - 1)
						while (linha + cont2 >= 0 and elemento+cont2 >= 0):
							self.redeSensores.getLista()[linha+ cont2][elemento+ cont2].alert(dados)
							cont2 -= 1
				if linhaAlerta == linha :
					if elementoAlerta < elemento:
						#TODO envia alerta para elemento (linha , elemento + 1)
						while (linha + cont <= self.redeSensores.getLista()[linha]):
							self.redeSensores.getLista()[linha][elemento+cont].alert(dados)
							cont+= 1
					if elementoAlerta > elemento: 
						#TODO envia alerta para elemento (linha , elemento - 1)
						while (elemento + cont2 <= 0):
							self.redeSensores.getLista()[linha][elemento+cont2].alert(dados)
							cont2 -= 1
					
					
				
				

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

