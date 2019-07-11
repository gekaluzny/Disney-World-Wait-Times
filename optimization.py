#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 14:33:54 2019

@author: m1gek00
"""

import pandas as pd
import numpy as np
from itertools import permutations

waits = pd.read_csv('/href/scratch3/m1gek00/project/waits.csv')

waits_sel = waits[['Seven Dwarfs Mine Train', 'Space Mountain', 'Splash Mountain',
                   'Big Thunder Mountain Railroad', 'Jungle Cruise', 'Peter Pan’s Flight']]
waits_red = np.ceil(waits_sel/15)

sequence = range(len(list(waits_red)))

perms = list(permutations(sequence))

possible_waits = list()
for i in perms:
    for j in i:
        if i[0]==j:
            ride_wait = int(waits_red.iloc[0, j])
            all_ride_wait = [ride_wait]
            total_ride_wait = ride_wait
        else:
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