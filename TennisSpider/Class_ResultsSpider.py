#!/usr/bin/env python
# coding: utf-8

import time
import grab
import os
import csv
import sys
import argparse
from grab.spider import Spider, Task



class ResultsSpider(Spider):
	initial_urls = ['http://www.tennislive.net/',]
	def task_initial(self, grab, task):
		'''
		'''
		self.base_url = self.initial_urls[0]
		data = ''
		if os.getenv('DATA') != None
			data = os.getenv('DATA')			
		atp_url = ('http://www.tennislive.net/atp-men/{}'.format(data))
		wta_url = ('http://www.tennislive.net/wta-women/{}'.format(data))
		print(men_url)
		yield Task('atp_tournament_list', url=atp_url)
		yield Task('wta_tournament_list', url=wta_url)


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

		for j in range(36):
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
			last = 0
			position = ''
			xpath = '//div[@class="player_comp_info_left"]/a'
			for elem in grab.doc.select(xpath):
				position = elem.text()
			xpath = '//div[@class="player_comp_info_left"]/text() | //div[@class="player_comp_info_left"]/a'
			for elem in grab.doc.select(xpath):
				if not last:
					row[23 + dic['Country']] = elem.text()
					last = dic['Country']
				elif 'years' in elem.text():
					row[23 + dic['Birthdate']] = elem.text()
					last = dic['Birthdate']
				elif 'cm' in elem.text():
					row[23 + dic['Height']] = elem.text()
					last = dic['Height']
				elif 'kg' in elem.text():
					row[23 + dic['Weight']] = elem.text()
					last = dic['Weight']
				elif 'handed' in elem.text():
					row[23 + dic['Play']] = elem.text()
					last = dic['Play']
				elif '$' in elem.text():
					row[23 + dic['Prize money']] = elem.text()
					last = dic['Prize money']
				else:
					try:
						int(elem.text())
						if elem.text() != position and last != 7:
							row[23 + dic['Profi since']] = elem.text()
							last = dic['Profi since']
						elif elem.text() == position:
							row[23 + dic["Ranking's position"]] = elem.text()
							last = dic["Ranking's position"]
						elif last == 7:
							row[23 + dic['Points']] = elem.text()
							last = dic['Points']
					except ValueError:
						pass

			last = 0
			position = ''
			xpath = '//div[@class="player_comp_info_right"]/a'
			for elem in grab.doc.select(xpath):
				position = elem.text()
			xpath = '//div[@class="player_comp_info_right"]/text() | //div[@class="player_comp_info_right"]/a'
			for elem in grab.doc.select(xpath):
				if not last:
					row[32 + dic['Country']] = elem.text()
					last = dic['Country']
				elif 'years' in elem.text():
					row[32 + dic['Birthdate']] = elem.text()
					last = dic['Birthdate']
				elif 'cm' in elem.text():
					row[32 + dic['Height']] = elem.text()
					last = dic['Height']
				elif 'kg' in elem.text():
					row[32 + dic['Weight']] = elem.text()
					last = dic['Weight']
				elif 'handed' in elem.text():
					row[32 + dic['Play']] = elem.text()
					last = dic['Play']
				elif '$' in elem.text():
					row[32 + dic['Prize money']] = elem.text()
					last = dic['Prize money']
				else:
					try:
						int(elem.text())
						if elem.text() != position and last != 7:
							row[32 + dic['Profi since']] = elem.text()
							last = dic['Profi since']
						elif elem.text() == position:
							row[32 + dic["Ranking's position"]] = elem.text()
							last = dic["Ranking's position"]
						elif last == 7:
							row[32 + dic['Points']] = elem.text()
							last = dic['Points']
					except ValueError:
						pass
			writer.writerow(row)
			res.close()
		else:
			xpath = '//div[@class="player_comp_info_left"]/text()'
			num = 0
			flag = True
			for elem in grab.doc.select(xpath):
				if flag:
					row[23 + dic['Country']] = elem.text()
					flag = False
				else:
					if 'years' in elem.text():
						row[23 + 9 * num + dic['Birthdate']] = elem.text()
					elif 'cm' in elem.text():
						row[23 + 9 * num + dic['Height']] = elem.text()
					elif 'kg' in elem.text():
						row[23 + 9 * num + dic['Weight']] = elem.text()
					elif 'handed' in elem.text():
						row[23 + 9 * num + dic['Play']] = elem.text()
					else:
						if elem.text().isnumeric():
							row[23 + 9 * num + dic['Profi since']] = elem.text()											
						elif elem.text() != '':
							row[32 + dic['Country']] = elem.text()
							num += 1

			xpath = '//div[@class="player_comp_info_right"]/text()'
			num = 0
			flag = True
			for elem in grab.doc.select(xpath):
				if flag:
					row[41 + dic['Country']] = elem.text()
					flag = False
				else:
					if 'years' in elem.text():
						row[41 + 9 * num + dic['Birthdate']] = elem.text()
					elif 'cm' in elem.text():
						row[41 + 9 * num + dic['Height']] = elem.text()
					elif 'kg' in elem.text():
						row[41 + 9 * num + dic['Weight']] = elem.text()
					elif 'handed' in elem.text():
						row[41 + 9 * num + dic['Play']] = elem.text()
					else:
						if elem.text().isnumeric():
							row[41 + 9 * num + dic['Profi since']] = elem.text()											
						elif elem.text() != '':
							row[50 + dic['Country']] = elem.text()
							num += 1
			writer.writerow(row)
			res.close()