#!/usr/bin/env python
# coding: utf-8

import grab
import os
import time
import csv
import sys
import argparse
from grab.spider import Spider, Task

class RanksSpider(Spider):
	initial_urls = ['http://live-tennis.eu/']
	def task_initial(self, grab, task):
		'''
		'''
		filename = os.getenv('FILENAME')
		self.base_url = self.initial_urls[0]
		if self.args.c == 'm':
			if self.args.t == 'l':
				yield Task('get_ranks', url='http://live-tennis.eu/')
			elif self.args.t == 'o':
				yield Task('get_ranks', url='http://live-tennis.eu/official_atp_ranking')
		elif self.args.c == 'f':
			if self.args.t == 'l':
				yield Task('get_ranks', url='http://live-tennis.eu/wta-live-ranking')
			elif self.args.t == 'o':
				yield Task('get_ranks', url='http://live-tennis.eu/official-wta-ranking')

	def task_get_ranks(self, grab, task):
		'''
		'''
		filename = os.getenv('FILENAME')
		xpath = '//tr/td'
		res = open('%s' %(filename), 'a')
		writer = csv.writer(res)
		row = []
		flag = False
		for elem in grab.doc.select(xpath):
			if not flag:
				if elem.text() == '1':
					j = 1
					row.append(elem.text())
					flag = True
			else:
				if j < 5500:
					if j % 11 == 10:
						row.append(elem.text())
						row.append(time.ctime())
						writer.writerow(row)
						row = []
						j += 1

					else:
						row.append(elem.text())
						j += 1
				else:
					break
			
		res.close()