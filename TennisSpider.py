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

		yield Task('atp_tournament_list', url='http://www.tennislive.net/atp-men')
		yield Task('wta_tournament_list', url='http://www.tennislive.net/wta-women')
	def task_atp_tournament_list(self, grab, task):
		'''
		'''
		print('atp_tournament_list')
		xpath = "//div[@class='tour_box']/ul/li[@class='menu_main']/a"
		for tournament in grab.doc.select(xpath):
			tournament_url = tournament.attr('href')
			tournament_name = tournament.attr('title')
			if tournament_name != "ATP ranking" and tournament_name != "WTA ranking" and tournament_name != "ALL TOURNAMENTS":
				yield Task('tournament_info', tournament_url, tournament_name=tournament_name)	
	def task_wta_tournament_list(self, grab, task):
		'''
		'''
		print('wta_tournament_list')
		xpath = "//div[@class='tour_box']/ul/li[@class='menu_main']/a"
		for tournament in grab.doc.select(xpath):
			tournament_url = tournament.attr('href')
			tournament_name = tournament.attr('title')
			if tournament_name != "ATP ranking" and tournament_name != "WTA ranking" and tournament_name != "ALL TOURNAMENTS":
				yield Task('tournament_info', tournament_url)		

	def task_tournament_info(self, grab, task):
		'''
		'''
		print('tournament_info')
		xpath ='//ul[@id = "topmenu_full"]/li/a'
		for elem in grab.doc.select(xpath):
			if elem.text() == 'Finished':
				fin_url = elem.attr('href')
				yield Task('get_pairs', fin_url)
		
	def task_get_pairs(self, grab, task):
		'''
		'''
		print('get_pairs')
		xpath = '//tr[@class="pair" or @class="unpair"]/td[@class!="beg"] | tr[@class="pair" or @class="unpair"]/td[@class="detail"]/div[@class="head2head"]'
		for elem in grab.doc.select(xpath):
			if elem.attr('class') == "head2head":
				el = elem.select('a')
				stats_url = el.attr('href')
				yield Task('get_stats', stats_url)

	def task_get_stats(self, grab, task):
		'''
		'''
		print('get_stats')
		xpath = '//div[@class="player_matches"]/table/tr/td' #данные о матче - дата, раунд, имена, счет
		f = open("new_results.txt", 'a')
		i = 0
		winner = ''
		for elem in grab.doc.select(xpath):
			print(elem.text())
			if i == 0:
				f.write(elem.text())
				i += 1
			elif i == 4:
				f.write(' ' + ',' +  ' ' + '"' + elem.text() + '"')
				i += 1
			elif i == 6:
				f.write(' ' + ',' + ' ' + '"' + elem.text() + '"')
				break
			else:
				f.write(' ' + ',' +  ' ' + '"' + elem.text() + '"')
				i += 1
		xpath = '//table[@class="table_stats_match"]/tr/td'
		i = 0
		flag = True
		for elem in grab.doc.select(xpath):
			print(elem.text())
			if flag:
				if i % 3 == 2:
					flag = False
					i += 1
				else:
					i += 1
			else:
				if i % 3 != 0:
					f.write(' ' + ','  +  ' ' + '"' + elem.text() + '"')
					i += 1
				else:
					i += 1
		f.write('\n')
		f.close()


def main():
    spider = TennisLiveSpider(thread_number=2)
    spider.run()

main()
