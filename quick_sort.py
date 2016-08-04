
# coding: utf-8

# In[8]:

#!/usr/bin/env python

"""
This is a Flask web app controller for the cars with rasberrypi.
"""
import random
def quick_sort(a):
    b1=[]
    b2=[]
    b3=[]
#    c=[]
    if len(a)>1:
        val = a[random.randrange(0, len(a))]
        for i in len(a):
            if a[i] < val:
                b1.append(a[i])
            elif a[i] > val:
                b3.append(a[i])
            else:
                b2.append(a[i])
        if len(b1):
            b1=quick_sort(b1)
        if len(b2):
            b2=quick_sort(b2)
        if len(b3):
            b3=quick_sort(b3)
        return b1+b2+b3
    else:
        return a

merge_sort([2,3,1,6,5,4])


# In[7]:

merge_sort([3,2])


# In[ ]:



