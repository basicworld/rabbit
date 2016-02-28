# -*- coding:utf8 -*-
"""
Class function: convert var to target type
Dont change anything
Author: wlf
Time: 20160224
"""
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def convertDictValueToList(value_name, *args, **kwargs):
    """
    Func to return values where key==value_name

    There are 2 algrithm: simple one and greedy one
    simple one works in default
    @greedy=True
    @greedy=False

    if you set greedy=True in kwargs the greedy one will works
    set greedy==True will spend more Time, make sure you need it else you should
    use simple func, eg:
        test_dict3 = {'1':{'id':1}, '2':{'id':2}, '3':{'id':3},}
        greedy convertDictValueToList('id',test_dict3, greedy=True)
        simple convertDictValueToList('id',test_dict3) 
        simple convertDictValueToList('id',test_dict3, greedy=False)

    # doctest
    >>> test_dict3 = {'1':{'id':1}, '2':{'id':2}, '3':{'id':3},}
    >>> convertDictValueToList('id',test_dict3, greedy=True)
    [1, 3, 2]
    >>> test_dict3 = {'1':{'id':1}, '2':{'aid':2}, '3':{'id':3},}
    >>> convertDictValueToList('id',test_dict3, greedy=True)
    [1, 3]
    >>> test_dict3 = {'1':{'id':1}, '2':{'aid':2}, '3':{'id':3},}
    >>> convertDictValueToList(None,test_dict3, greedy=True)
    [1, 3, 2]
    >>> test_dict3 = {'1':{'id':1}, '2':{'aid':2}, '3':{'id':3},}
    >>> convertDictValueToList(False,test_dict3, greedy=True)
    [1, 3, 2]
    >>> test_dict3 = {'1':{'id':1}, '2':{'id':2}, '3':{'id':3, '4':{'id':4}},}
    >>> convertDictValueToList('id',test_dict3, greedy=True)
    [1, 3, 4, 2]
    >>> test_dict3 = {'1':{'id':1}, '2':{'id':2}, '3':{'id':3, '4':{'id':4}},}
    >>> convertDictValueToList('id',test_dict3, greedy=False)
    [1, 3, 2]
    >>> test_dict3 = {'1':{'id':1,'name':'cang'}, '2':{'id':2}, \
        '3':{'id':3, '4':{'id':4}},}
    >>> convertDictValueToList('id',test_dict3)
    [1, 3, 2]
    """

    if (not args):
        print """Error use!
Here is an example that you can follow in your project:
response_list = convertDictValueToList('id',dict1,dict2)
        """
        return False

    _collector = []  
    _collect_with_value_name = False if value_name in (None, False) else True
    if not _collect_with_value_name:
        kwargs = {'greedy': True}

    # @decoratorConfig
    def _convert_with_value_name_simple(value_name, arg):
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
                        _convert_with_value_name_simple(value_name, value)
                else:
                    _collector.append(value)
            except KeyError, e:
                for value in arg.values():
                    if isinstance(value, dict):
                        _convert_with_value_name_simple(value_name, value)
                    else:
                        return False
        else:
            return False

    # @decoratorConfig
    def _convert_with_value_name_greedy(value_name, arg, key=False):
        '''
        Greedy algrithm: 
        loop all keys in dict and return value_list where:
        key == value_name and (not isinstance(value, dict))
        '''
        if isinstance(arg, dict):
            for arg_key in arg:
                _convert_with_value_name_greedy(value_name, arg[arg_key], 
                    key=arg_key)
        else:
            if _collect_with_value_name and (key == value_name):
                _collector.append(arg)

    # @decoratorConfig
    def _convert_without_value_name_greedy(value_name, arg, key=False):
        '''
        Greedy algrithm: 
        loop all keys in dict and return value_list where:
        (not isinstance(value, dict))
        '''
        if isinstance(arg, dict):
            for arg_key in arg:
                _convert_without_value_name_greedy(value_name, arg[arg_key], 
                    key=arg_key)
        else:
            _collector.append(arg)

    def _loop(value_name, args, func):
        for arg in args:
            func(value_name, arg)

    if kwargs and kwargs['greedy'] and _collect_with_value_name:
        _loop(value_name, args, _convert_with_value_name_greedy)
    elif kwargs and kwargs['greedy'] and not _collect_with_value_name:
        _loop(value_name, args, _convert_without_value_name_greedy)
    else:
        _loop(value_name, args, _convert_with_value_name_simple)

    if _collector:
        return _collector
    else:
        return False

from decimal import Decimal
def convertToList(*args, **kwargs):
    """
    var_type should be int float str decimal
    if you convert a var to a cant_be_type, it will return default var

    use func like:
    convertToList(*args, var_type=str)
    convertToList(*args)

    #doctest
    # 不支持中文测试
    >>> convertToList(1,2,3)
    [1, 2, 3]
    >>> convertToList(None)
    
    >>> convertToList(False)
    False
    >>> convertToList('a',1,1.1,'string', var_type=int)
    ['a', 1, 1, 'string']
    >>> convertToList('a',1,1.1,'string', var_type=Decimal)
    ['a', Decimal('1'), Decimal('1.100000000000000088817841970012523233890533447265625'), 'string']
    >>> convertToList(1, {'id':2})
    [1, 2]
    >>> convertToList(1.2, {'id':2.6}, var_type=int)
    [1, 2]
    >>> convertToList(1,2,3,[4,[5],[[6],7],8],9,10,(11))
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    >>> convertToList(1,2,3,[4,[5],[[6],7],8],9,10,(11), var_type=str)
    ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']
    """

    if not args:
        return False

    from decimal import InvalidOperation
    var_type = kwargs['var_type'] if (kwargs and kwargs['var_type']) else False
    convertable = False if var_type in (None, False) else True

    _collector = []

    def convert_with_var_type_greedy(var_type, args):
        '''greedy algrithm: get all keys in args'''
        for arg in args:
            if isinstance(arg, (tuple, list, set, dict)):
                if isinstance(arg, dict):
                    arg = convertDictValueToList(None, arg, greedy=True)
                convert_with_var_type_greedy(var_type, arg)
            else:
                try:
                    _collector.append(var_type(arg)) if convertable else \
                        _collector.append(arg)
                except ValueError, e:
                    _collector.append(arg)
                except InvalidOperation, e:
                    _collector.append(arg)

    convert_with_var_type_greedy(var_type, args)
    
    # return _collector
    if not _collector:
        return False
    elif len(_collector) == 1:
        return _collector[0]
    else:
        return _collector

if __name__ == '__main__':
    """
    doctest test
    """
    import doctest
    doctest.testmod(verbose=True)
    convertToList([[["中国","China",,,2],[,,"Zhōngguó","ˈCHīnə"]],[["名词",["中国","华","中华"],[["中国",["China"],,0.57875562],["华",["China","flower","flora"],,0.0083855102],["中华",["China"],,0.0038996246]],"China",1],["形容词",["中国的"],[["中国的",["Chinese","China"]]],"China",3]],"en",,,[["China",32011,[["中国",1000,true,false],["瓷器",0,true,false]],[[0,5]],"China",0,0]],0.77380955,,[["en"],,[0.77380955],["en"]],,,[["名词",[[["porcelain"],"m_en_us1232692.002"],[["dishes","plates","cups and saucers","tableware","chinaware","dinner service","crockery"],"m_en_us1232692.002"],[["chinaware"],""]],"china"]],[["名词",[["a country in eastern Asia, the third largest and most populous in the world; population 1,338,613,000 (est. 2009); capital, Beijing; language, Chinese (Mandarin is the official form).","m_en_us1232690.001"]],"China"],["名词",[["a fine white or translucent vitrified ceramic material.","m_en_us1232692.001","a plate made of china"]],"china"]],[[["they're going to \u003cb\u003eChina\u003c/b\u003e",,,,3,"neid_3491"],["\u003cb\u003eChina\u003c/b\u003e won 2-0",,,,3,"neid_3491"],["he's from \u003cb\u003eChina\u003c/b\u003e",,,,3,"neid_3491"],["she lives in \u003cb\u003eChina\u003c/b\u003e",,,,3,"neid_3491"],["the capital of \u003cb\u003eChina\u003c/b\u003e",,,,3,"neid_3491"]]],[["china","People's Republic of China","made in China","Republic of China","Bank of China","Communist Party of China","South China Sea","China Daily","Great Wall of China","East China Sea","China ink"]]])
