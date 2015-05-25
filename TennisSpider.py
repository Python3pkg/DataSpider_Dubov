#!/usr/bin/env python
# coding: utf-8

import grab
from grab.spider import Spider, Task

class TennisLiveSpider(Spider):
	initial_urls = ['http://www.tennislive.net/']
	def task_initial(self, grab, task):
		'''
		'''
		self.base_url = self.initial_urls[0]
		print('''For watching Atp Ranking, type Ra\nFor watching Wta Ranking, type Rw\nFor watching Tournments, type T \nFor watching schedule type S \nFor watching finished games type F\n[Ra, Rw, T, S, F] - ''', end=" ")
		TASK = input()
		if TASK == 'T':
			yield Task('tournment_list', url=task.url)
		elif TASK == "Ra":
			yield Task('get_atp_ranks', url='http://www.tennislive.net/atp/ranking/')
		elif TASK == "Rw":
			yield Task('get_wta_ranks', url='http://www.tennislive.net/wta/ranking/')
		elif TASK == 'S':
			yield Task('schedule', url=task.url)
		elif TASK == 'F':
			yield Task('finished_games', url=task.url)
		else:
			print("Not valid input")
	def task_tournment_list(self, grab, task):
		'''
		'''
		xpath = "//div[@class='tour_box']/ul/li[@class='menu_main']/a"
		for tournment in grab.doc.select(xpath):
			tournment_url = tournment.attr('href')
			tournment_name = tournment.attr('title')
			if tournment_name != "ATP ranking" and tournment_name != "WTA ranking" and tournment_name != "ALL TOURNAMENTS":
				yield Task('tournment_info', tournment_url, tournment_name=tournment_name)			

	def task_tournment_info(self, grab, task):
		'''
		'''
		xpath ='//ul[@id = "topmenu_full"]/li/a'
		for elem in grab.doc.select(xpath):
			if elem.text() == 'Finished':
				fin_url = elem.attr('href')
				yield Task('get_pairs', fin_url, tournment_name = task.tournment_name)
		

	def task_get_stat(self, grab, task):
		'''
		'''
		f = open("stats_sites", 'a')
		f.write(task.line)
		f.close()
	def task_get_pairs(self, grab, task):
		'''
		'''
		f = open("results.txt", 'a')
		a = []

		xpath = '//tr[@class="header"]/td'
		xpath = '//tr[@class="pair" or @class="unpair"]/td[@class="beg"]'
		for elem in grab.doc.select(xpath):
			p1 = 'text()'
			p2 = 'div'
			a.append([elem.select(p1)[0].text(), elem.select(p2)[0].text()]) #как сделать, чтобы раунд был отдельно от даты

		xpath = '//tr[@class="pair" or @class="unpair"]/td[@class!="beg"] | tr[@class="pair" or @class="unpair"]/td[@class="detail"]/div[@class="head2head"]'
		l = 0
		flag = True
		flagg = True
		for elem in grab.doc.select(xpath):
			if elem.attr('class') == "head2head":
				el = elem.select('a')
				stats_url = el.attr('href')
				yield Task('get_stat', stats_url, line = stats_url)
			else:
				if flagg:
					f.write('"' + task.tournment_name + '"' + "," + ' ' + a[l][0] + ',' + ' ' + '"' + a[l][1] + '"')
					flagg = False
				if elem.attr('class') != ('fift' or 'detail'):
					if flag:
						if elem.attr('class') == 'match':
							f.write(',' + ' ' + '"' + elem.text() + '"')
						else:
							f.write(',' + ' ' + elem.text())
					else:
						if elem.attr('class') == 'match':
							f.write('"' + elem.text() + '"')
						else:
							f.write(',' + ' ' + elem.text())
				elif flag == True:
					flag = False
				else:
					f.write('\n')
					l += 1
					flag = True
					flagg = True
		f.close()




	'''def task_finished_games(self, grab, task):
		xpath = '//div[@class = "full"]/ul/li/a'
		for elem in grab.doc.select(xpath):
			if elem.text() == "Finished":
				new_url = elem.attr('href')
				print("Finisched games:")
				yield Task('get_finished_pairs', new_url)

	def task_schedule(self, grab, task):
		xpath = '//div[@class = "full"]/ul/li/a'
		for elem in grab.doc.select(xpath):
			if elem.text() == "Scheduled":
				new_url = elem.attr('href')
				print("Schedule:")
				yield Task('get_pairs', new_url)'''

	'''def task_get_finished_pairs(self, grab, task):
		xpath = '//tr[@class="pair"]/td/a | //tr[@class="unpair"]/td/a'
		flag = True
		for elem in grab.doc.select(xpath):
			if flag:
				print(elem.text(), end=" - ")
				flag = False
			else:
				print(elem.text())'''

	'''def task_get_atp_ranks(self, grab, task):
		xpath = '//div[@class="rank_block"]/div/table/tr[@class="pair" or @class="unpair"]'
		for elem in grab.doc.select(xpath):
			print(elem.text())


	def task_get_wta_ranks(self, grab, task):
		xpath = '//div[@class="rank_block"]/div/table/tr[@class="pair" or @class="unpair"]'
		for elem in grab.doc.select(xpath):
			print(elem.text())'''

def main():
    spider = TennisLiveSpider(thread_number=2)
    spider.run()

main()

#CSV - comma
#TSV - tab
#модуль csv - посмотреть
#pandos - библиотека, некий ексель для питона (научных вычеслений) (sireies, dataframe, panel)
#click - пакет для утилит командной строки
#HW- с одного сайта запись в файл