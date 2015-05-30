#!/usr/bin/env python
# coding: utf-8

import grab
import os
import csv
import argparse
from grab.spider import Spider, Task

#TODO:
#Cделать вывод stdout stderr
#сделать парсинг сайта рейтингов, добавить утилиту для вывода расписания матчей
#Настроить cron
#Допилить парсинг
# --out 'name.csv'

parser = argparse.ArgumentParser()
parser.add_argument("-u", type=str, default='r', help="r - for results ,s - for schedule, g - for getting ranks")
args = parser.parse_args()

class TennisSpider(Spider):
	initial_urls = ['http://www.tennislive.net/', ]
	def task_initial(self, grab, task):
		'''
		'''
		self.base_url = self.initial_urls[0]
		#try args.u == 's'
		if args.u == 'r':
			yield Task('atp_tournament_list', url='http://www.tennislive.net/atp-men')
			yield Task('wta_tournament_list', url='http://www.tennislive.net/wta-women')
		elif args.c == 'r':
			yield Task('ranks', url='http://ranks.com')
		else:
			pass
			#throw exception

	def task_atp_tournament_list(self, grab, task):
		'''
		'''
		civility = "male"
		xpath = "//div[@class='tour_box']/ul/li[@class='menu_main']/a"
		for tournament in grab.doc.select(xpath):
			tournament_url = tournament.attr('href')
			tournament_name = tournament.attr('title')
			if tournament_name != "ATP ranking" and tournament_name != "WTA ranking" and tournament_name != "ALL TOURNAMENTS":
				yield Task('tournament_info', tournament_url, tournament_name=tournament_name, civility=civility)	
	def task_wta_tournament_list(self, grab, task):
		'''
		'''
		civility = "female"
		xpath = "//div[@class='tour_box']/ul/li[@class='menu_main']/a"
		for tournament in grab.doc.select(xpath):
			tournament_url = tournament.attr('href')
			tournament_name = tournament.attr('title')
			if tournament_name != "ATP ranking" and tournament_name != "WTA ranking" and tournament_name != "ALL TOURNAMENTS":
				yield Task('tournament_info', tournament_url, tournament_name=tournament_name, civility=civility)	

	def task_tournament_info(self, grab, task):
		'''
		'''
		xpath ='//ul[@id = "topmenu_full"]/li/a'
		for elem in grab.doc.select(xpath):
			if elem.text() == 'Finished':
				fin_url = elem.attr('href')
				yield Task('get_pairs', fin_url, civility=task.civility)
		
	def task_get_pairs(self, grab, task):
		'''
		'''
		xpath = '//tr[@class="pair" or @class="unpair"]/td[@class!="beg"] | tr[@class="pair" or @class="unpair"]/td[@class="detail"]/div[@class="head2head"]'
		for elem in grab.doc.select(xpath):
			if elem.attr('class') == "head2head":
				el = elem.select('a')
				stats_url = el.attr('href')
				yield Task('get_stats', stats_url, civility=task.civility)

	def task_get_stats(self, grab, task):
		'''
		'''
		row = []
		filename = os.getenv('FILENAME')
		xpath = '//div[@class="player_matches"]/table/tr/td' #данные о матче - дата, раунд, имена, счет
		res = open('%s' %filename, 'a')
		writer = csv.writer(res)
		i = 0
		for elem in grab.doc.select(xpath):
			if i == 0:
				row.append(str(elem.text()))
				i += 1
			elif i == 2:
				row.append(str(task.civility))
				row.append(str(elem.text()))
				i += 1
			elif i == 6:
				row.append(str(elem.text()))
				break
			else:
				row.append(str(elem.text()))
				i += 1
		xpath = '//table[@class="table_stats_match"]/tr/td'
		for j in range(16):
				row.append("-")
		dic = {'1st SERVE %' : 1,
				'1st SERVE POINTS WON' : 2,
				'2nd SERVE POINTS WON' : 3,
				'BREAK POINTS WON' : 4,
				'TOTAL RETURN POINTS WON' : 5,
				'TOTAL POINTS WON' : 6,
				'DOUBLE FAULTS' : 7,
				'ACES' : 8,
				}
		i = 0
		stat = ''
		flag = True
		for elem in grab.doc.select(xpath):
			if flag:
				if i % 3 == 2:
					i += 1
					flag = False
				else:
					i += 1
			else:
				if i % 3 != 0:
					row[dic[stat] * 2 - (i%3)%2 + 7] = str(elem.text())
					i += 1
				else:
					stat = elem.text()
					i += 1
		for j in range(18):
			row.append("-")
		dic = {'Country' : 1,
				'Birthdate' : 2,
				'Height' : 3,
				'Weight' : 4,
				'Profi since' : 5,
				'Play' : 6,
				"Ranking's position" : 7,
				'Points' : 8,
				'Prize money' : 9,
				}
		if "/" not in row[3]:
			compare = []
			xpath = '//div[@class="player_comp_desc"]/text()'
			for elem in grab.doc.select(xpath):
				compare.append([elem.text(), '-', '-'])
			xpath = '//div[@class="player_comp_info_left"]/text()'
			k = 0
			for elem in grab.doc.select(xpath):
				if elem.text() == "":
					compare[k][1] = "-"
				else:
					compare[k][1] = elem.text()
					k += 1
			xpath = '//div[@class="player_comp_info_right"]/text()'
			k = 0
			for elem in grab.doc.select(xpath):
				if elem.text() == "":
					compare[k][2] = "-"
				else:
					compare[k][2] = elem.text()
					k += 1
			for elem in compare:
				if elem[0] != "":
					row[23 + dic[elem[0]]*2 - 1] = elem[1]
					row[23 + dic[elem[0]]*2 ] = elem[2]
			writer.writerow(row)
			res.close()
		else:
			#for j in range(18):
			#	row.append("-")
			#xpath = '//div[@class="player_comp_desc"]/text()'
			#for elem in grab.doc.select(xpath):
			#	compare.append([elem.text(), '-', '-'])
			writer.writerow(row)
			res.close()


def main():
	spider = TennisSpider(thread_number=2)
	spider.run()

main()
