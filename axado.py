#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import csv

class Axado(object):

	def __init__(self, x):
		self.x = x

	def multiplica_por_dois(self):
		return self.x * 2

if __name__ == "__main__":
	# ax = Axado(x=10)
	# print ax.x
	# print "%d vezes 2 e %d\n" % (ax.x, ax.multiplica_por_dois())
	
	param = sys.argv[1:]
	if len(param) == 4:
		#lendo os parametros
		print(param)
		origem = param[0]
		destino = param[1]
		nota_fiscal = param[2]
		peso = param[3]
		print origem
		print destino
		print nota_fiscal
		print peso
		
		#lendo o arquivo
		#print __doc__
		f = csv.reader(open('tabela/rotas.csv'), delimiter=',')
		for [rt_origem, rt_destino, rt_prazo, rt_seguro, rt_kg, rt_fixa] in f:
			# print 'origem=%s | destino=%s | prazo=%s | seguro=%s | kg=%s | fixa: %s' % (origem, destino, prazo, seguro, kg, fixa)
			# print f.line_num, 'linhas lidas'
			# print '--- fim'
			if origem == rt_origem and destino == rt_destino:
				#print 'origem=%s | destino=%s | prazo=%s | seguro=%s | kg=%s | fixa: %s' % (rt_origem, rt_destino, rt_prazo, rt_seguro, rt_kg, rt_fixa)
				valor_seguro = float(nota_fiscal)*float(rt_seguro)/100
				fixa = float(rt_fixa)
				faixa = 0

				#ler arquivo com as faixas de valores por peso
				p = csv.reader(open('tabela/preco_por_kg.csv'), delimiter=',')
				for [p_nome, p_inicial, p_final, p_preco] in p:
					#print 'p_nome=%s | p_inicial=%s | p_final=%s | p_preco=%s' % (p_nome, p_inicial, p_final, p_preco)
					#print '%s - %s - %s - %s' % (rt_kg, p_inicial, p_final, peso)
					
					# if (p_final):
					# 	if rt_kg.strip() == p_nome.strip() and (float(peso) >= float(p_inicial) and float(peso) < float(p_final)):							
					# 		faixa = float(peso) * float(p_preco)	

					if rt_kg.strip() == p_nome.strip():
						if (p_final):
							if (float(peso) >= float(p_inicial) and float(peso) < float(p_final)):							
								faixa = float(peso) * float(p_preco)
						else:
							faixa = float(peso) * float(p_preco)

				#quo = 94 / 100
				#print 'quo: %s' % quo
				icms = 6
				valor_tabela1 = (float(valor_seguro) + float(fixa) + float(faixa)) / 0.94				
				print 'seguro: <nota_fiscal> %s * <seguro> %s / 100 = %.2f' % (nota_fiscal, rt_seguro, valor_seguro)
				print 'fixa: <proprio valor da taxa> = %2.f' % (fixa)
				print 'faixa: <valor de acordo com o peso> = %2.f' % (faixa)
				print 'valor_seguro + fixa + faixa <subtotal antes do icms> = %s' % (valor_seguro+fixa+faixa)
				print 'icms: na <tabela 1> sempre sera 6 = %s' % (icms)
				print ''
				print '========'
				print ''
				print 'tabela: %s, %s' % (rt_prazo, valor_tabela1)

		print ''
		print '========'
		print ''
		
		valor_seguro = 0
		fixa = 0
		faixa = 0
		icms = 0
		alfandega = 0
		valor_tabela2 = 0
		with open('tabela2/rotas.tsv','rb') as tsvin_rt, open('rotas.csv', 'wb') as csvout_rt:
			tsvin_rt = csv.reader(tsvin_rt, delimiter='\t')
			csvout_rt = csv.writer(csvout_rt)

			for r_rotas in tsvin_rt:
				#print '%s' % r_rotas
				if origem == r_rotas[0] and destino == r_rotas[1]:
					valor_seguro = float(nota_fiscal)*float(r_rotas[4])/100
					
					with open('tabela2/preco_por_kg.tsv','rb') as tsvin_pk, open('preco_por_kg.csv', 'wb') as csvout_pk:
						tsvin_pk = csv.reader(tsvin_pk, delimiter='\t')
						csvout_pk = csv.writer(csvout_pk)

						for r_preco in tsvin_pk:
							if r_preco[0].strip() == r_rotas[7].strip(): 																					
								if float(r_rotas[2]) == 0:
									faixa = float(peso) * float(r_preco[3])
									break
								
								if float(r_preco[2]) < float(r_rotas[2]):
									faixa = float(peso) * float(r_preco[3])

								# if r_rotas[2]:
								# 	if float(r_preco[2]) < float(r_rotas[2]):
								# 		faixa = float(peso) * float(r_preco[3])
								# else:
								# 	faixa = float(peso) * float(r_preco[3])

					alfandega = (float(valor_seguro) + float(fixa) + float(faixa)) * (float(r_rotas[6]) / float(100))
					icms = float(r_rotas[5])
					valor_tabela2 = (float(valor_seguro) + float(fixa) + float(faixa) + float(alfandega)) / ((100 - float(icms))/100)
					print ''
					print 'seguro: <nota_fiscal> %s * <seguro> %s / 100 = %.2f' % (nota_fiscal, r_rotas[4], valor_seguro)
					print 'fixa: <proprio valor da taxa> = %s' % (fixa)
					print 'faixa: <valor de acordo com o peso> = %s' % (faixa)
					print '<subtotal> = %s' % (valor_seguro + fixa + faixa)
					print '<alfandega> = %s' % (r_rotas[6])
					print 'calculo alfandega: <subtotal * (alfandega/100)> = %s' % (alfandega)
					print '<subtotal antes do icms> = %s' % (valor_seguro + fixa + faixa + alfandega)
					print 'icms: na <tabela 2> = %s' % (icms)
					print ''
					print '========'
					print ''
					print 'tabela 2: %s, %s' % (r_rotas[3], valor_tabela2)
	else:
		print "Por favor informar todos os parametros para calcular o frete"