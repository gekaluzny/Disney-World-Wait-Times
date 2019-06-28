# -*- coding: utf-8 -*-
import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime

os.chdir('/Users/grahamkaluzny/Documents')

## Download URL and feed it into Beautiful Soup
url = 'https://www.laughingplace.com/w/p/magic-kingdom-current-wait-times/'
response = requests.get(url)
soup = BeautifulSoup(response.text)

## Get text from first table on page, the table with wait times
tables = soup.find('table')
text = tables.get_text()

## Split and clean text
split = text.split('\n')
split_cleaned = list(filter(None, split))

## Divide them into ride and wait times lists
ride = split_cleaned[0:len(split_cleaned):2]
wait = split_cleaned[1:len(split_cleaned)+1:2]

## Create a datetime row
now = str(datetime.datetime.now())
wait.insert(0, now)
ride.insert(0, 'datetime')

## Turn into dataframe
df = pd.DataFrame(wait).T
df.columns = ride

## Import old csv, append, then rewrite csv
old = pd.read_csv('disney.csv')
full = old.append(df)
full.to_csv('disney.csv', index = False)

