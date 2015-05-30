#!/usr/bin/env python
# coding: utf-8

import grab
import os
import time
import csv
import sys
import argparse
from grab.spider import Spider, Task

parser = argparse.ArgumentParser()
parser.add_argument("-c", type=str, default='m', help="m - for male, f - for female")
parser.add_argument("-t", type=str, default='l', help="l - for live rating, o - for oficcial")
args = parser.parse_args()

class RanksSpider(Spider):
	initial_urls = ['http://live-tennis.eu/']
	def task_initial(self, grab, task):
		'''
		'''
		filename = os.getenv('FILENAME')
		self.base_url = self.initial_urls[0]
		if args.c == 'm':
			if args.t == 'l':
				yield Task('get_ranks', url='http://live-tennis.eu/')
			elif args.t == 'o':
				yield Task('get_ranks', url='http://live-tennis.eu/official_atp_ranking')
		elif args.c == 'f':
			if args.t == 'l':
				yield Task('get_ranks', url='http://live-tennis.eu/wta-live-ranking')
			elif args.t == 'o':
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
def main():
    spider = RanksSpider(thread_number=2)
    spider.run()

main()
