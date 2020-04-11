#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 19:39:50 2020

@author: jcespedes
"""


from crontab import CronTab

my_cron=CronTab(user='jcespedes')
my_cron.remove_all()
my_cron.write()