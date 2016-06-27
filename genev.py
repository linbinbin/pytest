#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on Mon Jun 20 17:07:59 2016

@author: H8324261
"""

import random
from time import sleep
from greenlet import greenlet
import queue

q = queue.Queue()

@greenlet
def producer():
    chars = ['a', 'b', 'c', 'd', 'e']
    global q
    while True:
        char = random.choice(chars)
        q.put(char)
        print("Produced: {}".format(char))
        sleep(1)
        consumer.switch()

@greenlet
def consumer():
    global q
    while True:
        char = q.get()
        print("Consumed: {}".format(char))
        sleep(1)
        producer.switch()

if __name__ == "__main__":
    producer.run()
    consumer.run()
