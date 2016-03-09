# -*- coding:utf8 -*-
"""
Class function: test the performance of a func
Dont change anything
Author: wlf
Time: 20160222
"""
import datetime
import time
import sys
def decoratorConfig(func):
    def _wrapper(*args, **kwargs):
        _start_time = datetime.datetime.now()
        _resp = func(*args, **kwargs)
        _end_time = datetime.datetime.now()
        print (u"<%s> spend %s \u03bcs." % (func.__name__, (_end_time - _start_time).microseconds))
        return _resp
    return _wrapper

@decoratorConfig
def decoratorTest(*args, **kwargs):
    """test"""
    if args:
        print args
    if kwargs:
        print kwargs

if __name__ == '__main__':
    decoratorTest(1,2,3)
    decoratorTest(1,1,3)
    decoratorTest(1,3,3)

