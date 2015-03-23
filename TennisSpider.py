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
		print('''For watching Tournments, type T \nFor watching schedule type S \nFor watching finished games type F\n[T, S, F] - ''', end=" ")
		TASK = input()
		if TASK == 'T':
			yield Task('tournment_list', url=task.url)
		elif TASK == 'S':
			yield Task('schedule', url=task.url)
		elif TASK == 'F':
			yield Task('finished_games', url=task.url)
		else:
			print("Not valid input")
	def task_tournment_list(self, grab, task):
		'''
		'''
		xpath = "//li[@class='menu_main']/a"
		for tournment in grab.doc.select(xpath):
			tournment_url = tournment.attr('href')
			tournment_name = tournment.attr('title')
			print(tournment_name)

	def task_tournment_info(self, grab, task):
		'''
		'''
		xpath ='//tr[@class = "pair"]/td[@class = "match"]'
		for elem in grab.doc.select(xpath):
			name = elem.select('a').text()
			print(name, end=", ")

	def task_finished_games(self, grab, task):
		'''
		'''
		xpath = '//div[@class = "full"]/ul/li/a'
		for elem in grab.doc.select(xpath):
			if elem.text() == "Finished":
				new_url = elem.attr('href')
				print("Finisched games:")
				yield Task('get_pairs', new_url)

	def task_schedule(self, grab, task):
		'''
		'''
		xpath = '//div[@class = "full"]/ul/li/a'
		for elem in grab.doc.select(xpath):
			if elem.text() == "Scheduled":
				new_url = elem.attr('href')
				print("Schedule:")
				yield Task('get_pairs', new_url)

	def task_get_pairs(self, grab, task):
		'''
		'''
		xpath = '//tr[@class="pair"]/td/a | //tr[@class="unpair"]/td/a'
		flag = True
		for elem in grab.doc.select(xpath):
			if flag:
				print(elem.text(), end=" - ")
				flag = False
			else:
				print(elem.text())
				flag = True

def main():
    spider = TennisLiveSpider(thread_number=2)
    spider.run()

main()