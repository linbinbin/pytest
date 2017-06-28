# -*- coding: utf-8 -*-
import random

def change(car, select):
    lt = [1, 2, 3, 4]
    if lt[car - 1] == lt[select - 1]:
        del lt[car - 1]
        return lt[0]
    else:
        return car

if __name__ == '__main__':
    right = 0
    n_right = 0
    for i in range(1000):
        car = random.randint(1, 4)
        select = random.randint(1, 4)
        if change(car, select) == car:
            right += 1
        if car == select:
            n_right += 1
    print("no_change = {}%".format(n_right / 1000))
    print("change = {}%".format(right / 1000))
