#!/usr/bin/env python
# coding: utf-8

import time
import grab
import os
import csv
import sys
import argparse
import getting_time
from getting_time import get_time, get_date
from grab.spider import Spider, Task



class ResultsSpider(Spider):
    initial_urls = ['http://www.tennislive.net/',]
    def task_initial(self, grab, task):
        '''
        '''
        self.base_url = self.initial_urls[0]
        date = ''
        n = self.args.n
        if n:
            t = get_time()
            date = get_date(t[0], t[1], t[2], n)
        else:
            if os.getenv('TENNIS_DATE'):
                date = os.getenv('TENNIS_DATE')
        atp_url = ('http://www.tennislive.net/atp-men/{}'.format(date))
        wta_url = ('http://www.tennislive.net/wta-women/{}'.format(date))
        yield Task('atp_tournament_list', url=atp_url)
        yield Task('wta_tournament_list', url=wta_url)


    def task_atp_tournament_list(self, grab, task):
        '''
        Get the list of atp tournaments.
        '''
        civility = "male"
        xpath = "//div[@class='tour_box']/ul/li[@class='menu_main']/a"
        for tournament in grab.doc.select(xpath):
            tournament_url = tournament.attr('href')
            tournament_name = tournament.attr('title')
            if tournament_name not in ["ATP ranking", "WTA ranking", "ALL TOURNAMENTS"]:
                yield Task('tournament_info', tournament_url, tournament_name=tournament_name, civility=civility)   
    
    def task_wta_tournament_list(self, grab, task):
        '''
        Get the list of wta tournaments.
        '''
        civility = "female"
        xpath = "//div[@class='tour_box']/ul/li[@class='menu_main']/a"
        for tournament in grab.doc.select(xpath):
            tournament_url = tournament.attr('href')
            tournament_name = tournament.attr('title')
            if tournament_name in ["ATP ranking", "WTA ranking", "ALL TOURNAMENTS"]:
                yield Task('tournament_info', tournament_url, tournament_name=tournament_name, civility=civility)   

    def task_tournament_info(self, grab, task):
        '''
        Get the site with all finished mathes in tournament
        '''
        xpath ='//ul[@id = "topmenu_full"]/li/a'
        for elem in grab.doc.select(xpath):
            if elem.text() == 'Finished':
                fin_url = elem.attr('href')
                yield Task('get_pairs', fin_url, civility=task.civility)
        
    def task_get_pairs(self, grab, task):
        '''
        Iterate on the list of finished mathes in tournament
        '''
        xpath = '//tr[@class="pair" or @class="unpair"]/td[@class!="beg"] | tr[@class="pair" or @class="unpair"]/td[@class="detail"]/div[@class="head2head"]'
        for elem in grab.doc.select(xpath):
            if elem.attr('class') == "head2head":
                el = elem.select('a')
                stats_url = el.attr('href')
                yield Task('get_stats', stats_url, civility=task.civility)



    def task_get_stats(self, grab, task):
        '''
        Get all infromation about the finished matches, including stats and info about players.
        '''
        NUM_OF_COLUMN = 6
        NUM_OF_COLUMN_IN_STATS_TABLE = 3
        COLUMN_AFTER_MATCH_INFO = 7
        COLUMS_FOR_PLAYERS_INFO = 36
        NAME_PLAYER1 = 3
        COLUMS_IN_PLAYER_INFO = 9
        COLUMS_AFTER_STATS = 23
        COLUMS_AFTER_STATS_AND_PLAYER1 = 32
        COLUMS_AFTER_STATS_AND_PAIR1 = 41
        COLUMS_AFTER_STATS_AND_PAIR1_AND_PLAYER3 = 50

        row = []
        
        xpath = '//div[@class="player_matches"]/table/tr/td' #данные о матче - дата, раунд, имена, счет
        
        i = 0
        for elem in grab.doc.select(xpath):
            if i < NUM_OF_COLUMN and i != 2:
                row.append(str(elem.text()))
                i += 1
            elif i == 2:
                row.append(str(task.civility))
                row.append(str(elem.text()))
                i += 1
            elif i == NUM_OF_COLUMN:
                row.append(str(elem.text()))
                break

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
                if i % NUM_OF_COLUMN_IN_STATS_TABLE == 2:
                    i += 1
                    flag = False
                else:
                    i += 1
            else:
                if i % NUM_OF_COLUMN_IN_STATS_TABLE != 0:
                    row[dic[stat] * 2 - (i % NUM_OF_COLUMN_IN_STATS_TABLE)%2 + COLUMN_AFTER_MATCH_INFO] = str(elem.text())
                    i += 1
                else:
                    stat = elem.text()
                    i += 1

        for j in range(COLUMS_FOR_PLAYERS_INFO):
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

        if "/" not in row[NAME_PLAYER1]:
            last = 0
            position = ''
            xpath = '//div[@class="player_comp_info_left"]/a'
            for elem in grab.doc.select(xpath):
                position = elem.text()
            xpath = '//div[@class="player_comp_info_left"]/text() | //div[@class="player_comp_info_left"]/a'
            for elem in grab.doc.select(xpath):
                if not last:
                    row[COLUMS_AFTER_STATS + dic['Country']] = elem.text()
                    last = dic['Country']
                elif 'years' in elem.text():
                    row[COLUMS_AFTER_STATS + dic['Birthdate']] = elem.text()
                    last = dic['Birthdate']
                elif 'cm' in elem.text():
                    row[COLUMS_AFTER_STATS + dic['Height']] = elem.text()
                    last = dic['Height']
                elif 'kg' in elem.text():
                    row[COLUMS_AFTER_STATS + dic['Weight']] = elem.text()
                    last = dic['Weight']
                elif 'handed' in elem.text():
                    row[COLUMS_AFTER_STATS + dic['Play']] = elem.text()
                    last = dic['Play']
                elif '$' in elem.text():
                    row[COLUMS_AFTER_STATS + dic['Prize money']] = elem.text()
                    last = dic['Prize money']
                else:
                    try:
                        int(elem.text())
                        if elem.text() != position and last != 7:
                            row[COLUMS_AFTER_STATS + dic['Profi since']] = elem.text()
                            last = dic['Profi since']
                        elif elem.text() == position:
                            row[COLUMS_AFTER_STATS + dic["Ranking's position"]] = elem.text()
                            last = dic["Ranking's position"]
                        elif last == 7:
                            row[COLUMS_AFTER_STATS + dic['Points']] = elem.text()
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
                    row[COLUMS_AFTER_STATS_AND_PLAYER1 + dic['Country']] = elem.text()
                    last = dic['Country']
                elif 'years' in elem.text():
                    row[COLUMS_AFTER_STATS_AND_PLAYER1 + dic['Birthdate']] = elem.text()
                    last = dic['Birthdate']
                elif 'cm' in elem.text():
                    row[COLUMS_AFTER_STATS_AND_PLAYER1 + dic['Height']] = elem.text()
                    last = dic['Height']
                elif 'kg' in elem.text():
                    row[COLUMS_AFTER_STATS_AND_PLAYER1 + dic['Weight']] = elem.text()
                    last = dic['Weight']
                elif 'handed' in elem.text():
                    row[COLUMS_AFTER_STATS_AND_PLAYER1 + dic['Play']] = elem.text()
                    last = dic['Play']
                elif '$' in elem.text():
                    row[COLUMS_AFTER_STATS_AND_PLAYER1 + dic['Prize money']] = elem.text()
                    last = dic['Prize money']
                else:
                    try:
                        int(elem.text())
                        if elem.text() != position and last != 7:
                            row[COLUMS_AFTER_STATS_AND_PLAYER1 + dic['Profi since']] = elem.text()
                            last = dic['Profi since']
                        elif elem.text() == position:
                            row[COLUMS_AFTER_STATS_AND_PLAYER1 + dic["Ranking's position"]] = elem.text()
                            last = dic["Ranking's position"]
                        elif last == 7:
                            row[COLUMS_AFTER_STATS_AND_PLAYER1 + dic['Points']] = elem.text()
                            last = dic['Points']
                    except ValueError:
                        pass
        else:
            xpath = '//div[@class="player_comp_info_left"]/text()'
            num = 0
            flag = True
            for elem in grab.doc.select(xpath):
                if flag:
                    row[COLUMS_AFTER_STATS + dic['Country']] = elem.text()
                    flag = False
                else:
                    if 'years' in elem.text():
                        row[COLUMS_AFTER_STATS + COLUMS_IN_PLAYER_INFO * num + dic['Birthdate']] = elem.text()
                    elif 'cm' in elem.text():
                        row[COLUMS_AFTER_STATS + COLUMS_IN_PLAYER_INFO * num + dic['Height']] = elem.text()
                    elif 'kg' in elem.text():
                        row[COLUMS_AFTER_STATS + COLUMS_IN_PLAYER_INFO * num + dic['Weight']] = elem.text()
                    elif 'handed' in elem.text():
                        row[COLUMS_AFTER_STATS + COLUMS_IN_PLAYER_INFO * num + dic['Play']] = elem.text()
                    else:
                        if elem.text().isnumeric():
                            row[COLUMS_AFTER_STATS + COLUMS_IN_PLAYER_INFO * num + dic['Profi since']] = elem.text()                                            
                        elif elem.text() != '':
                            row[COLUMS_AFTER_STATS + dic['Country']] = elem.text()
                            num += 1

            xpath = '//div[@class="player_comp_info_right"]/text()'
            num = 0
            flag = True
            for elem in grab.doc.select(xpath):
                if flag:
                    row[COLUMS_AFTER_STATS_AND_PAIR1 + dic['Country']] = elem.text()
                    flag = False
                else:
                    if 'years' in elem.text():
                        row[COLUMS_AFTER_STATS_AND_PAIR1 + COLUMS_IN_PLAYER_INFO * num + dic['Birthdate']] = elem.text()
                    elif 'cm' in elem.text():
                        row[COLUMS_AFTER_STATS_AND_PAIR1 + COLUMS_IN_PLAYER_INFO * num + dic['Height']] = elem.text()
                    elif 'kg' in elem.text():
                        row[COLUMS_AFTER_STATS_AND_PAIR1 + COLUMS_IN_PLAYER_INFO * num + dic['Weight']] = elem.text()
                    elif 'handed' in elem.text():
                        row[COLUMS_AFTER_STATS_AND_PAIR1 + COLUMS_IN_PLAYER_INFO * num + dic['Play']] = elem.text()
                    else:
                        if elem.text().isnumeric():
                            row[COLUMS_AFTER_STATS_AND_PAIR1 + COLUMS_IN_PLAYER_INFO * num + dic['Profi since']] = elem.text()                                            
                        elif elem.text() != '':
                            row[COLUMS_AFTER_STATS_AND_PAIR1_AND_PLAYER3 + dic['Country']] = elem.text()
                            num += 1
        
        filename = os.getenv('TENNIS_FILENAME')
        with open('%s' %filename, 'a') as res:
            writer = csv.writer(res)
            writer.writerow(row)