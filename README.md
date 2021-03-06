# DataSpider_Dubov
The utility for parcing information about finished matches in live tennis tournaments, ranks, and schedule.
##Preparing for using
###Python Installation
install python3: https://www.python.org/downloads/
###Grab Installation
install python module Grab: http://docs.grablib.org/en/latest/usage/installation.html
##Use of utility
In utility there are 4 files: *main.py*, *Class_RankSpider.py*, *Class_ResultsSpider.py*, *Class_ScheduleSpider.py*. All files need to be in one folder.

By using utility you can select three names of option **-u**: **f** - for finished results, **r** - for ranks, **s** - for schedule.

If you select **f** or **r**, you need to indicate the name of file (in format *csv*) you will save the information to with the option of command line **TENNIS_FILENAME**. Also you can indicate the date, from when you want to get results with the option **TENNIS_DATE**. The date must look like: **"2013-03-02"**.

So for parsing results from 7 June 2015, your command will look like:

```
$ TENNIS_DATE='2015-06-07' TENNIS_FILENAME=results.csv python3 main.py -u f
```
Or you can indicate option **-n** with an integer number, to get finished results or schedule by the date n days from today.

If you select option **r**, you also can select two other options **-c**: **m** - for male ranks, **f** - for female ranks, and **-t**: **o** - for official ranks, and **l** - for live ranks.
So for parsing e.g. live female ranks your command will look like:

```
$ TENNIS_FILENAME=wta_live_ranks.csv python3 main.py -u r -c f -t l
```

If you select option **-u s**, you can also indicate, where to write *stdout*, and the date from when to take the schedule with option **TENNIS_DATE**, as by parsing finished results (default it is nowaday). Example of command:

```
$ TENNIS_DATE='2015-06-07' python3 main.py -u s > schedule.txt
```

Without indicating where to write *stdout*, it will be showed in your terminal.
