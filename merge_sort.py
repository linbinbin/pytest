#!/usr/bin/env python

"""
This is a Flask web app controller for the cars with rasberrypi.
"""
def merge_sort(a):
    b1=[]
    b2=[]
    c=[]
    if len(a)>1:
        b1=merge_sort(a[:int(len(a)/2)])
        b2=merge_sort(a[int(len(a)/2):])
        i=0
        j=0
        for k in range(len(a)):
            if i < len(b1) and j < len(b2):
                if b1[i] < b2[j]:
                    c.append(b1[i])
                    i += 1
                else:
                    c.append(b2[j])
                    j += 1
            elif i >= len(b1):
                c.append(b2[j])
                j += 1
            else:
                c.append(b1[i])
                i += 1
        return c
    else:
        return a

merge_sort([2,3,1,6,5,4])
