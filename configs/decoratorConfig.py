# -*- coding:utf8 -*-
"""
Class function: test the performance of a func
Dont change anything
Author: wlf
Time: 20160222
"""
import datetime
def decoratorConfig(func):
    '''装饰器，用于测试运行性能'''
    def wrapper(*args, **kwargs):
        print '-'*20
        print '[+] call : %s()' % func.__name__
        start_time = datetime.datetime.now()
        func(*args, **kwargs)
        end_time = datetime.datetime.now()
        print '    spend %s' % (end_time - start_time)
    return wrapper

