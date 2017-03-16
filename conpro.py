# -*- coding: utf-8 -*-
#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time

def consumer():
    r = ''
    while True:
        n = yield r
        if not n:
            print('n is None.')
            return
        print('Consume running %s...' % n)
        time.sleep(1)
        r = '200 OK'

def produce(c):
    next(c)
    n = 0
    while n < 5:
        n = n + 1
        print('[Produce] running %s...' % n)
        r = c.send(n)
        print('[Consumer] return: %s' % r)
    c.close()

if __name__=='__main__':
    c = consumer()
    produce(c)