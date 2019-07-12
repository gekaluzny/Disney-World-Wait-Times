#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 21:28:12 2019

@author: grahamkaluzny
"""

import pandas as pd
import numpy as np
from itertools import permutations

waits = pd.read_csv('/Users/grahamkaluzny/Documents/magic_kingdom_avgwaits.csv')
waits = waits.fillna(1)

waits_sel = waits[['Seven Dwarfs Mine Train', 'Space Mountain', 'Splash Mountain',
                   'Big Thunder Mountain Railroad', 'Jungle Cruise', 'Peter Pan’s Flight',
                   'Buzz Lightyear’s Space Ranger Spin', 'Haunted Mansion',
                   'Pirates of the Caribbean']]
waits_red = np.ceil(waits_sel/15)
names = list(waits_red)

sequence = range(len(list(waits_red)))

perms = list(permutations(sequence))

possible_waits = list()
for i in perms:
    ride_wait = int(waits_red.iloc[0, i[0]])
    all_ride_wait = [ride_wait]
    total_ride_wait = ride_wait
    for j in i[1:]:
        ride_wait = int(waits_red.iloc[total_ride_wait, j])
        all_ride_wait.append(ride_wait)
        total_ride_wait = sum(all_ride_wait)
    possible_waits.append(all_ride_wait)

summed_waits = list()
for i in possible_waits:
    x = sum(i)
    summed_waits.append(x)
    
minimum_wait = min(summed_waits)
optimal_num = [i for i, e in enumerate(summed_waits) if e == minimum_wait]
optimal = [perms[index] for index in optimal_num]

optimal_rides = list()
for i in optimal:
    temp = [names[j] for j in i]
    optimal_rides.append(temp)