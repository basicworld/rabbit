# -*- coding:utf8 -*-
"""
Class function: convert var to target type
Dont change anything
Author: wlf
Time: 20160224
""" 
from decimal import Decimal
def convertDictValueToList(value_name, *args):
    if not args:
        return None

    collector = []  
    collect_with_value_name = False if value_name in (None, False, 0) else True

    def convert_with_value_name_greedy(value_name, arg, key=False):
        '''greedy algrithm: loop all keys in dict'''
        if isinstance(arg, dict):
            for arg_key in arg:
                convert_with_value_name_greedy(value_name, arg[arg_key], key=arg_key)
        else:
            if collect_with_value_name and (key == value_name):
                collector.append(arg)

    def loop_with_value_name_simple(value_name, arg, key=False):
        pass
    for arg in args:
        convert_with_value_name_greedy(value_name, arg)

    return collector


def convertToList(var_type,*args):
    """
    var_type should be int float str decimal
    if you convert a var to a cant_be_type, it will return default var
    """
    if not args:
        return None

    convertable = False if var_type in (None, False, 0) else True
        
    collector = []
    def convert_with_var_type_greedy(var_type, args):
        '''greedy algrithm: get all keys in args'''
        for arg in args:
            if not isinstance(arg, (tuple, list, set)):
                try:
                    collector.append(var_type(arg)) if convertable else \
                        collector.append(arg)
                except ValueError, e:
                    collector.append(arg)
            else:
                convert_with_var_type_greedy(var_type, arg)

    convert_with_var_type_greedy(var_type, args)
    
    # return collector
    if len(collector) == 1:
        return collector[0]
    else:
        return collector

if __name__ == '__main__':
    test_dict = {'aa':'6','bb':{'id':7}}
    test_dict2 = {'dd':{'id':{'id':'1','bb':{'id':2}},'bb':{'id':3}},'ee':{'id':'4','bb':{'id':5}}}
    print convertDictValueToList('id',test_dict,test_dict2)
    # convertDictValueToList('id',{'bb':7})

    # print convertToList(int, 1.2,1.3)
    # print convertToList(Decimal, 1.2,1.3)
    # print convertToList(str, 1.2,1.3)
    # print convertToList(int, 1.2)
    # print convertToList(Decimal, 1.2)
    # print convertToList(float, 1.2)
    # print convertToList(float, 'aaa','b')
    # print convertToList(str, ([1,[2,3,[4,5],[6,None,'a',7,[8]]]],))
    # print convertToList(0, 1.2,1.3)
    # print convertToList(0, 1.2,1.3)
    # print convertToList(0, 1.2,1.3)
    # print convertToList(0, 1.2)
    # print convertToList(0, 1.2)
    # print convertToList(0, 1.2)
    # print convertToList(0, 'aaa','b')
    # print convertToList(0, ([1,[2,3,[4,5],[6,None,'a',7,[8]]]],))
    



