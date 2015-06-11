#!/usr/bin/env python
# coding: utf-8

import grab
import os
import csv
import sys
import argparse
import getting_time
from Class_ResultsSpider import ResultsSpider
from Class_ScheduleSpider import ScheduleSpider
from Class_RanksSpider import RanksSpider
from grab.spider import Spider, Task
#add option for parcing previous day
parser = argparse.ArgumentParser()
parser.add_argument("-u", type=str, default='f', help="f - for finished results ,s - for schedule, r - for getting ranks")
parser.add_argument("-c", type=str, default='m', help="m - for male, f - for female")
parser.add_argument("-t", type=str, default='l', help="l - for live rating, o - for official")
parser.add_argument("-n", type=int, default='0', help="input integer number, for getting results or schedule in n days from today")
args = parser.parse_args()

def main():
	if args.u == 'f':
		spider = ResultsSpider(thread_number=2, args=args)
		spider.run()
	elif args.u == 's':
		spider = ScheduleSpider(thread_number=2)
		spider.run()
	elif args.u == 'r':
		spider = RanksSpider(thread_number=2, args=args)
		spider.run()
	else:
		sys.stderr.write('Unvalid input of option -u\n')

main()
