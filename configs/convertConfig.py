# -*- coding:utf8 -*-
"""
Class function: convert var to target type
Dont change anything
Author: wlf
Time: 20160224
""" 
from decimal import Decimal
def convertDictValueToList(value_name, *args, **kwargs):
    """
    Func to return values where key==value_name
    There are 2 algrithm: simple one and greedy one
    simple one works in default
    if you set greedy=True in kwargs the greedy one will works
    set greedy==True will spend more Time, make sure you need it else you should
    use simple func, eg:
        test_dict3 = {'1':{'id':1}, '2':{'id':2}, '3':{'id':3},}
        greedy convertDictValueToList('id',test_dict3, greedy=True)
        simple convertDictValueToList('id',test_dict3) 
        simple convertDictValueToList('id',test_dict3, greedy=False)

    """

    if (not args):
        print """Error use!
Here is an example that you can follow in your project:
response_list = convertDictValueToList('id',dict1,dict2)
        """
        return None


    collector = []  
    collect_with_value_name = False if value_name in (None, False, 0) else True

    def convert_with_value_name_simple(value_name, arg):
        """
        Simple algrithm, it will not loop all the keys, if you use this func,
        args must be a or a list of dict where must fullfil all the follow:
            1,all dicts has the same format
            2,in one dict, dict.values() should be in same type(dict or not 
                dict, but can't exist both), eg:
                Wrong: args={'1':{'id':{'id':1}}, '2':{'id':2}, '3':{'id':3},}
                Right: args={'1':{'id':1}, '2':{'id':2}, '3':{'id':3},}

                Wrong: args=({'id':1},{'id':{'id':2}},{'id':3})
                Right: args=({'id':1},{'id':2},{'id':3})


        test_dict3 = {'1':{'id':1}, '2':{'id':2}, '3':{'id':3},}
        >>>convertDictValueToList('id',test_dict3)
        [1, 3, 2]
        >>>convertDictValueToList('id',{'id':1},{'id':2},{'id':3})
        [1, 2, 3]
        """
        if isinstance(arg, dict):
            try:
                value = arg[value_name]
                if isinstance(value, dict):
                    for value in arg.values():
                        convert_with_value_name_simple(value_name, value)
                else:
                    collector.append(value)
            except KeyError, e:
                for value in arg.values():
                    if isinstance(value, dict):
                        convert_with_value_name_simple(value_name, value)
                    else:
                        return None
        else:
            return None

    def convert_with_value_name_greedy(value_name, arg, key=False):
        '''
        Greedy algrithm: 
        loop all keys in dict and return value_list where:
        key == value_name and (not isinstance(value, dict))
        '''
        if isinstance(arg, dict):
            for arg_key in arg:
                convert_with_value_name_greedy(value_name, arg[arg_key], 
                    key=arg_key)
        else:
            if collect_with_value_name and (key == value_name):
                collector.append(arg)

    if kwargs and kwargs['greedy']:
        for arg in args:
            convert_with_value_name_greedy(value_name, arg)
    else:
        for arg in args:
            # convert_with_value_name_greedy(value_name, arg)
            convert_with_value_name_simple(value_name, arg)

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
    """test"""
    # test_dict = {'aa':'6','bb':{'id':7}}
    # test_dict2 = {'dd':{'id':{'id':'1','bb':{'id':2}},'bb':{'id':3}},'ee':{'id':'4','bb':{'id':5}}}
    # print convertDictValueToList('id',test_dict,test_dict2)


    test_dict3 = {'1':{'id':1}, '2':{'id':2}, '3':{'id':3},}
    print convertDictValueToList('id',test_dict3, greedy=True)
    print convertDictValueToList('id',test_dict3)
    print convertDictValueToList('id',test_dict3, greedy=False)
    # print convertDictValueToList('id',{'id':1},{'id':2},{'id':3})
    # print convertDictValueToList('id',{'we':1},{'we':2},{'we':3})
    # test_dict4 = {'1':{'id':1}, '2':{'id':2}, '3':{'id':3},}

    # print convertDictValueToList(test_dict,test_dict2)
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
    



