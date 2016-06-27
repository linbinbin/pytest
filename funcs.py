# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 13:58:02 2016

@author: H8324261
"""

import random
from functools import reduce
 
names = ['Mary', 'Isla', 'Sam']
 
secret_names = map(lambda x: random.choice(['Mr. Pink',
                                            'Mr. Orange',
                                            'Mr. Blonde']),
                   names)
print(list(secret_names))

sentences = ['Mary read a story to Sam and Isla.',
             'Isla cuddled Sam.',
             'Sam chortled.']
 
sam_count = reduce(lambda a, x: a + x.count('Sam'),
                   sentences,
                   0)
#print(sam_count)

people = [{'name': 'Mary', 'height': 160},
    {'name': 'Isla', 'height': 80},
    {'name': 'Sam'}]
sl = map(lambda x: x['height'], filter(lambda x: 'height' in x, people))
ll = list(sl)
al = reduce(lambda a, x: a + x, ll, 0)
print(al/len(ll))

def move_cars(car_positions):
    return map(lambda x: x + 1 if random.random() > 0.3 else x,
               car_positions)
 
def output_car(car_position):
    return '-' * car_position
 
def run_step_of_race(state):
    return {'time': state['time'] - 1,
            'car_positions': list(move_cars(state['car_positions']))}
 
def draw(state):
    print('')
    print('\n'.join(map(output_car, state['car_positions'])))
 
def race(state):
    draw(state)
    print(state['time'])
    if state['time']:
        race(run_step_of_race(state))
 
race({'time': 5,
      'car_positions': [1, 1, 1]})     