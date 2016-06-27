#!/usr/bin/env python
# -*- coding: utf-8 -*-

def makeHtmlTag(tag, *args, **kwds):
    def real_decorator(fc):
        css_class = " class='{0}'".format(kwds["css_class"]) \
                                     if "css_class" in kwds else ""
        def wrapped(*args, **kwds):
            return "<"+tag+css_class+">" + fc(*args, **kwds) + "</"+ args[0] + tag+">"
        return wrapped
    return real_decorator
 
@makeHtmlTag(tag="b", css_class="bold_css")
@makeHtmlTag(tag="i", css_class="italic_css")
def hello(name):
    return "hello world " + name
 
print (hello('lin'))