#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import csv

class Axado(object):

	def __init__(self, x):
		self.x = x

	def multiplica_por_dois(self):
		return self.x * 2

	def calculoFreteTabela1(self, origem, destino, nota_fiscal, peso):
		try:
			valor_seguro = 0.0
			fixa = 0.0
			faixa = 0.0
			valor_tabela1 = 0.0
			icms = 6 #o icms sempre sera 6% para a tabela 1
			prazo = "0"

			#percorrer a tabela de rotas e encontrar os parametro conforme origem e destino
			f = csv.reader(open('tabela/rotas.csv'), delimiter=',')
			#os dados do arquivo serao separados nas variaveis referente sua informacao
			for [rt_origem, rt_destino, rt_prazo, rt_seguro, rt_kg, rt_fixa] in f:
				#se origem e destino passados por parametro encontrados no arquivo
				if origem == rt_origem and destino == rt_destino:
					#calcular seguro: <(valor da nota fiscal * taxa do seguro)/100>
					valor_seguro = float(nota_fiscal)*float(rt_seguro)/100
					#valor da taxa fixa
					fixa = float(rt_fixa)
					#prazo 
					prazo = rt_prazo

					#ler arquivo com as faixas de valores cobrados por peso de acordo com a faixa de peso
					p = csv.reader(open('tabela/preco_por_kg.csv'), delimiter=',')
					#os dados do arquivo serao separados nas variaveis referente sua informacao
					for [p_nome, p_inicial, p_final, p_preco] in p:
						#compara o nome das faixas referencia para cobranca de frente por kilograma
						if rt_kg.strip() == p_nome.strip():
							#verificar se o peso final foi declarado na tabela de cobranca
							if len(p_final.strip()) > 0:
								if rt_kg.strip() == p_nome.strip() and (float(peso) >= float(p_inicial) and float(peso) < float(p_final)):							
									faixa = float(peso) * float(p_preco)
									break
							else:
								faixa = float(peso) * float(p_preco)
								break

					#calculo do valor do frete da tabela 1 (ja foi calculado a divisao do icms)
					valor_tabela1 = (float(valor_seguro) + float(fixa) + float(faixa)) / 0.94				

			return 'tabela: %s, %.2f' % (prazo, valor_tabela1)
		except:
			return 'Houve um erro ao calcular o frete da tabela 1'

	def calculoFreteTabela2(self, origem, destino, nota_fiscal, peso):
		try:
			valor_seguro = 0.0
			fixa = 0.0
			faixa = 0.0
			icms = 0.0
			alfandega = 0.0
			valor_tabela2 = 0.0
			prazo = "0"
			status = 1

			#coverter o arquivo .tsv em .csv e realizar a leituras das rotas
			with open('tabela2/rotas.tsv','rb') as tsvin_rt, open('tabela2/rotas.csv', 'wb') as csvout_rt:
				tsvin_rt = csv.reader(tsvin_rt, delimiter='\t')
				csvout_rt = csv.writer(csvout_rt)

				#percorrer as linhas com todas as rotas
				for r_rotas in tsvin_rt:
					#se encontrar origem e destino compativel com o parametro
					if origem == r_rotas[0] and destino == r_rotas[1]:
						#calcular seguro: <(valor da nota fiscal * taxa do seguro)/100>
						valor_seguro = float(nota_fiscal)*float(r_rotas[4])/100
						#prazo
						prazo = r_rotas[3]

						#coverter o arquivo .tsv em .csv e realizar a leituras das faixas de preco por peso
						with open('tabela2/preco_por_kg.tsv','rb') as tsvin_pk, open('tabela2/preco_por_kg.csv', 'wb') as csvout_pk:
							tsvin_pk = csv.reader(tsvin_pk, delimiter='\t')
							csvout_pk = csv.writer(csvout_pk)

							#percorrer as linhas do arquivo
							for r_preco in tsvin_pk:
								#comparar siglas de cobranca por faixa de preco
								if r_preco[0].strip() == r_rotas[7].strip(): 																					
									#se limite de cobranca for 0
									if r_preco[0].strip() == r_rotas[7].strip(): 																					
										if float(r_rotas[2]) == 0:
											faixa = float(peso) * float(r_preco[3])
											break
									
										if len(r_preco[2]) > 0:
											if float(r_preco[2]) < float(r_rotas[2]):
												faixa = float(peso) * float(r_preco[3])
										else:
											status = 0
											break

						#calculo alfandega: <subtotal * (taxa alfandega/100)>
						alfandega = (float(valor_seguro) + float(fixa) + float(faixa)) * (float(r_rotas[6]) / float(100))
						#icms de acordo com a origem e o destino
						icms = float(r_rotas[5])
						#valor do frete <subtotal (com a taxa de alfandega) / calculo icms>
						if status == 1:
							valor_tabela2 = (float(valor_seguro) + float(fixa) + float(faixa) + float(alfandega)) / ((100 - float(icms))/100)
						else:
							prazo = '-'
							valor_tabela2 = '-'
						
				if valor_tabela2 == '-':
					return 'tabela 2: %s, %s' % (prazo, valor_tabela2)
				else:
					return 'tabela 2: %s, %.2f' % (prazo, valor_tabela2)
		except:
			return 'Houve um erro ao calcular o frete da tabela 2'

if __name__ == "__main__":
	#instancia da classe Axado
	ax = Axado(x=10)
	
	#ler os parametros para calculo do frete
	param = sys.argv[1:]
	if len(param) == 4:
		origem = param[0]
		destino = param[1]
		nota_fiscal = param[2]
		peso = param[3]
		
		#calcular o valor do frete da tabela 1
		print ax.calculoFreteTabela1(origem, destino, nota_fiscal, peso)
		#calcular o valor do frete da tabela 2
		print ax.calculoFreteTabela2(origem, destino, nota_fiscal, peso)
	else:
		print "Por favor informar todos os parametros para calcular o frete"