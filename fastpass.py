#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 15:17:54 2019

@author: grahamkaluzny
"""

import pandas as pd
from itertools import permutations

waits_all = pd.read_csv('/Users/grahamkaluzny/Documents/avg_waits_9_11.csv')
waits_filled = waits_all.fillna(5)

waits = waits_filled[['Big Thunder Mountain Railroad',
                   'Splash Mountain',
                   'Pirates of the Caribbean',
                   'Jungle Cruise', 
                   'The Haunted Mansion',
                   'Peter Pan\'s Flight',
                   'Seven Dwarfs Mine Train',
                   'Buzz Lightyear\'s Space Ranger Spin',
                   'Space Mountain'                   
                   ]]

loc = [0, 0, 2, 2, 5, 7, 7, 10, 10]

waits = waits + 5

names = list(waits)

sequence = range(len(list(waits)))

perms = list(permutations(sequence))

possible_waits = []
for i in perms:
    ride_wait = waits.iloc[0, i[0]]
    total_ride_wait = ride_wait + 5
    old_loc = loc[i[0]]
    for j in i[1:len(i)-3]:
        new_loc = loc[j]
        walk_time = abs(new_loc - old_loc)
        total_ride_wait = total_ride_wait + walk_time
        total_ride_wait_round = int(round(total_ride_wait/10))
        ride_wait = waits.iloc[total_ride_wait_round, j]
        total_ride_wait = total_ride_wait + ride_wait
        old_loc = new_loc
    possible_waits.append(total_ride_wait)
    
minimum_wait = min(possible_waits)
optimal_num = [i for i,j in enumerate(possible_waits) if j==minimum_wait]
optimal = [perms[i] for i in optimal_num]
optimal_rides = [[names[i] for i in j] for j in optimal]

## With fastpasses excluded
waits_all = pd.read_csv('/Users/grahamkaluzny/Documents/avg_waits_9_11.csv')
waits_filled = waits_all.fillna(5)

waits = waits_filled[['Big Thunder Mountain Railroad',
                   'Splash Mountain',
                   'Pirates of the Caribbean',
                   'Jungle Cruise', 
                   'The Haunted Mansion',
                   'The Many Adventures of Winnie the Pooh',
                   'Under the Sea - Journey of the Little Mermaid',
                   'Tomorrowland Transit Authority PeopleMover',
                   'Buzz Lightyear\'s Space Ranger Spin',
                   ]]

loc = [0, 0, 2, 2, 5, 7, 7, 10, 10]

waits = waits + 5

names = list(waits)

sequence = range(len(list(waits)))

perms = list(permutations(sequence))

possible_waits = []
for i in perms:
    ride_wait = waits.iloc[0, i[0]]
    total_ride_wait = ride_wait + 5
    old_loc = loc[i[0]]
    for j in i[1:]:
        new_loc = loc[j]
        walk_time = abs(new_loc - old_loc)
        total_ride_wait = total_ride_wait + walk_time
        total_ride_wait_round = int(round(total_ride_wait/10))
        ride_wait = waits.iloc[total_ride_wait_round, j]
        total_ride_wait = total_ride_wait + ride_wait
        old_loc = new_loc
    possible_waits.append(total_ride_wait)
    
minimum_wait = min(possible_waits)
optimal_num = [i for i,j in enumerate(possible_waits) if j==minimum_wait]
optimal = [perms[i] for i in optimal_num]
optimal_rides = [[names[i] for i in j] for j in optimal]