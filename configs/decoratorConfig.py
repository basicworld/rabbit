# -*- coding:utf8 -*-
"""
Class function: test the performance of a func
Dont change anything
Author: wlf
Time: 20160222
"""
import datetime
def decoratorConfig(func):
    '''
    Wlf: this is a decorator used for testing your function
    how to use:
    
    from configs.decoratorConfig import decoratorConfig
    @decoratorConfig
    def you_func_name(*args, kwargs):
        pass
    '''
    def wrapper(*args, **kwargs):
        print '-'*20
        print '[+] call : %s()' % func.__name__
        start_time = datetime.datetime.now()
        func(*args, **kwargs)
        end_time = datetime.datetime.now()
        print '    spend time %s' % (end_time - start_time)
    return wrapper

@decoratorConfig
def decoratorTest(*args, **kwargs):
    """test"""
    if args:
        print args
    if kwargs:
        print kwargs

if __name__ == '__main__':
    decoratorTest(1,2,3)

