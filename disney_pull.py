#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 13 16:35:10 2019

@author: grahamkaluzny
"""

from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import re

## Set dates we want to pull from touringplans.com
date = pd.date_range(start = '2019-06-01', end = '2019-06-02')

## Loop for each date
for d in date:
    date_str = str(d.date())
    url = "https://touringplans.com/magic-kingdom/wait-times/date/" + date_str
    html = get(url)
    
    ## Turn in to BeautifulSoup and find scripts
    soup = BeautifulSoup(html.text)
    script = soup.find_all('script')
    
    ## Find ride titles
    title = [re.findall('title: \"(.*) -', i.text) for i in script]
    title = list(filter(None, title))
    
    ## Find time and wait times
    time_wait = [re.findall('new Date\((.+)\),,,,,,,,(\d+),,,,,null,,null', i.text) 
        for i in script]
    time_wait = list(filter(None, time_wait))
    
    ## Create separate csv for each ride on each day
    for i, j in enumerate(time_wait):
        df = pd.DataFrame(j, columns = ['time', 'wait'])
        name = title[i][0] + '_' + date_str + '.csv'
        df.to_csv('/Users/grahamkaluzny/Documents/magic_kingdom/' + name)
        
    
    
