#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 11:43:11 2020

@author: jcespedes
"""


from crontab import CronTab

my_cron=CronTab(user='jcespedes')
job = my_cron.new(command='/Users/jcespedes/anaconda3/bin/python /Users/jcespedes/Documents/GitHub/dividends/Get_dividends.py')

job.hour.every(24)
my_cron.write()
print("Cron Modified")