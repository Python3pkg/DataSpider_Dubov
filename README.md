# DataSpider_Dubov
The utility for parcing information about finished matches in live tennis tournaments, ranks, and schedule. 
##Preparing for using
###Python Installation
install python: https://www.python.org/downloads/
###Grab Installation
install python module Grab: http://docs.grablib.org/en/latest/usage/installation.html
##Use of utility
In utility there are 4 files: main.py, Class_RankSpider.py, Class_ResultsSpider.py, Class_ScheduleSpider.py
By using utility you can select three names of option -u: f - for finished results, r - for ranks, s - for schedule.
If you select f or r, you need to indicate the name of file (in format csv) you will save the information to with the option of command line FILNAME.
So for parsing results your command will look like:
```
$ FILENAME=results.csv python3 ranks.py -u f
```
If you select option r, you also can select two other options -c: m - for male ranks, f - for female ranks, and -t: o - for official ranks, and l - for live ranks.
So for parsing e.g. live female ranks your command will look like:
```
$ FILENAME=wta_live_ranks.csv python3 ranks.py -u r -c f -t l
```
If you select option -u s, you can also indicate, where to write stdout. Example of command:
```
$ python3 ranks.py -u s > schedule.txt
```
