# -*- coding:utf8 -*-
"""
Intro: tool kit
Author: basicworld@163.com
Functions:
<timeDecorator>: decorator
<testFunc>: inner test function
"""

import os
import sys
import csv
import time
import datetime
import MySQLdb
from decimal import Decimal

reload(sys)
sys.setdefaultencoding('utf8')
BASE_DIR = os.path.split(os.path.realpath(__file__))[0]


def timeDecorator(func):
    """A decorator to show running time of a func"""
    def _wrapper(*args, **kwargs):
        _start_time = datetime.datetime.now()
        _resp = func(*args, **kwargs)
        _end_time = datetime.datetime.now()
        _time_diff = (_end_time - _start_time).microseconds
        print (u"<%s> spend %s \u03bcs." % (func.__name__, _time_diff))
        return _resp
    return _wrapper


def listConverter(*args, **kwargs):
    """
    Convert int, tuple, etc to list with target type if it can be
    @target_type
    1、字符串
    2、布尔类型
    3、整数
    4、浮点数
    5、数字
    6、列表
    7、元组
    8、字典
    9、日期
    """
    target_type = kwargs['target_type'] if kwargs else None
    target_type = unicode if target_type in (str,) else target_type
    _collector = []

    def _iterator(items, target_type):
        for item in items:
            if isinstance(item, (list, tuple, set,)):
                _iterator(item, target_type)
            else:
                try:
                    _collector.append(target_type(item))
                except (ValueError, TypeError) as e:
                    _collector.append(item)
    _iterator(args, target_type)
    return _collector


def timeGenerator(basetime='', timedelta=0, timetype='day'):
    pass


@timeDecorator
def testFunc(*args, **kwargs):
    """Test"""
    return listConverter(1, 2, 3, 4, 5, (6, 7), ['a', 'b', 8],
                         target_type=float)


class csvManager(object):
    def __init__(self, filename, savedir='./', mode='wb'):
        # makedirs if not exsit
        os.makedirs(savedir) if not os.path.isdir(savedir) else True
        # create csv file
        filename += '.csv' if not filename.endswith('.csv') else ''
        _full_filename = os.path.join(savedir, filename)
        self._file = open(_full_filename, mode)
        if mode.startswith('w'):
            self._file.write('\xEF\xBB\xBF')
        self._writer = csv.writer(self._file)

    def writerow(self, *args):
        items = listConverter(args)
        if items:
            self._writer.writerow(items)

    def __del__(self):
        if not self._file.closed:
            self._file.close()

    def __enter__(self):
        return self

    def __exit__(self, *unused):
        pass


class mysqlManager(object):
    def __init__(self, host, user, passwd, db, port=3306, charset='utf8'):
        try:
            self._conn = MySQLdb.connect(host=host, user=user, passwd=passwd,
                                         db=db, port=port, charset=charset)
            self._curs = self._conn.cursor()
        except:
            raise

    def execute(self, sql, debug=False, **kwargs):
        sql = sql % kwargs
        if sql:
            self._curs.execute(sql)
            return self._curs.fetchall()
        else:
            raise ValueError('execute(self, sql, **kwargs) got wrong value')

    def __del__(self):
        try:
            self._conn.commit()
            self._curs.close()
            self._conn.close()
        except:
            pass

    def __enter__(self):
        return self

    def __exit__(self, *unused):
        pass


if __name__ == '__main__':
    # print testFunc('adsf')
    # with csvManager('csvtest.csv', mode='ab') as csvapp:
    #     csvapp.writerow(1, 2, 3, 4, 5, '动物', )
    csvapp = csvManager('csvtest.csv', mode='ab')
    csvapp.writerow(1, 2, 3, 4, 5, '动物', )
