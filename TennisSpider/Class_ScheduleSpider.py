#!/usr/bin/env python
# coding: utf-8

import grab
import os
import csv
import sys
import argparse
from grab.spider import Spider, Task

class ScheduleSpider(Spider):
	initial_urls = ['http://www.tennislive.net/', ]
	def task_initial(self, grab, task):
		'''
		'''
		self.base_url = self.initial_urls[0]
		yield Task('schedule', url=task.url)

	def task_schedule(self, grab, task):
		'''
		'''
		xpath = '//div[@class = "full"]/ul/li/a'
		for elem in grab.doc.select(xpath):
			if elem.text() == "Scheduled":
				new_url = elem.attr('href')
				sys.stdout.write("Schedule:")
				yield Task('get_pairs', new_url)

	def task_get_pairs(self, grab, task):
		'''
		'''
		xpath = '//tr[@class="pair" or @class="unpair"]/td[@class!="beg"] | tr[@class="pair" or @class="unpair"]/td[@class="detail"]/div[@class="head2head"]'
		for elem in grab.doc.select(xpath):
			if elem.attr('class') == "head2head":
				el = elem.select('a')
				stats_url = el.attr('href')
				yield Task('get_info', stats_url)

	def task_get_info(self, grab, task):
		'''
		'''
		xpath = '//div[@class="player_matches"]/table/tr/td'
		i = 0
		match = []
		for elem in grab.doc.select(xpath):
			if i == 0:
				if elem.text() != '':
					match.append(str(elem.text()))
				i += 1
			elif i == 2:
				if elem.text() != '':
					match.append(str(elem.text()))
				i += 1
			elif i == 6:
				if elem.text() != '':
					match.append(str(elem.text()))
				break
			else:
				if elem.text() != '':
					match.append(str(elem.text()))
				i += 1
		for elem in match:
			if elem != 'no matches found':
				sys.stdout.write(elem + ', ')
		sys.stdout.write('\n')