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
date = pd.date_range(start = '2019-06-09', end = '2019-06-30')

## Loop for each date
for d in date:
    date_str = str(d.date())
    url = "https://touringplans.com/magic-kingdom/wait-times/date/" + date_str
    html = get(url)
    
    ## Turn in to BeautifulSoup and find scripts
    soup = BeautifulSoup(html.text)
    script = soup.find_all('script', type = 'text/javascript')
    
    for i in script:
        ## Only look at scripts that are rides
        if re.search('title: \"(.*) -', i.text) != None:
            ## Find and clean the title
            title = re.findall('title: \"(.*) -', i.text)[0]
            title = title.replace('\\','').replace('~', '-')
            
            ## Find the column for recorded wait
            time_wait = re.findall(
                    'new Date\((.+)\),,,,,,,,(\d+),,,,,null,,null', i.text)
            
            ## Find the dates and wait, replacing month with June because of
            ##      error that says May
            datetime = [j[0].replace('2019,5', '2019,6') for j in time_wait]
            wait = [j[1] for j in time_wait]
            
            ## Put in dataframe and write to csv
            df = pd.DataFrame({'datetime': datetime, 'wait': wait})
            name = ('/Users/grahamkaluzny/Documents/magic_kingdom/' + title + 
                    '_' + date_str + '.csv')
            df.to_csv(name, index = False)
        
    
    ## Find opening, closing, and EMH times
    table = soup.find('table').getText()
    times = re.findall('\d*:\d*[ap]m', table)
    hours = pd.DataFrame({'opening': [times[0]], 'closing': [times[1]]})
    name = ('/Users/grahamkaluzny/Documents/magic_kingdom/hours_' + date_str + 
            '.csv')
    hours.to_csv(name, index = False)
    

    
    
        
    
    
