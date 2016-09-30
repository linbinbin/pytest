#!/usr/bin/env python
# -*- coding: utf-8 -*-
from optparse import OptionParser, OptionValueError
from xml.etree.ElementTree import *
import codecs
import base64
import os
import sys

def read(fname):
    prm_start = 0
    with codecs.open(fname, 'r' ,encoding='utf8') as f:
        for line in f.readline():
            if prm_start == 0:
                pass
def chg_path(contents, dmpath):
    pass
