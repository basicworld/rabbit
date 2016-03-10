# -*- coding:utf8 -*-
"""
Intro: tool kit
Author: basicworld@163.com

timeDecorator(): decorator
timeGenerator(): create time
listConverter(): convert to list
csvManager(): wrapper csv model
mysqlManager(): wrapper MySQLdb
testFunc(): inner test function
"""

import os
import sys
import csv
import glob
import time
import datetime
import MySQLdb
import zipfile
from decimal import Decimal

reload(sys)
sys.setdefaultencoding('utf8')
BASE_DIR = os.path.split(os.path.realpath(__file__))[0]


def timeDecorator(func):
    """
    timeDecorator(func)
    A decorator to show running time of a func
    eg:
    @timeDecorator
    def func():
        ....
    """
    def _wrapper(*args, **kwargs):
        _start_time = datetime.datetime.now()
        _resp = func(*args, **kwargs)
        _end_time = datetime.datetime.now()
        _time_diff = (_end_time - _start_time).microseconds
        print (u"<%s> spend %s \u03bcs." % (func.__name__, _time_diff))
        return _resp
    return _wrapper


def timeGenerator(basetime='', timedelta=0, target_type='day'):
    """
    timeGenerator(basetime='', timedelta=0, target_type='day')
    Generate time with target_type
    @basetime: input a time or None by default
    @timedelta: basetime + timedelta = target_time
    @target_type: day, month, year, month_start
    eg:
    target_time = timeGenerator('2016-01-19', timedelta=-1, target_type='day')
    """
    if basetime:
        basetime = unicode(basetime).replace("-", "")
        try:
            basetime = time.strptime(basetime, '%Y%m%d')
            basetime = datetime.datetime(*basetime[:3])
        except:
            raise ValueError(r'basetime should be None or an exsit day')
            # return False
    else:
        basetime = datetime.datetime.now()

    oneday = datetime.timedelta(days=1)
    target_type_dict = {
        'year': '%Y',
        'month': '%Y-%m',
        'month_start': '%Y-%m-01',
        'day': '%Y-%m-%d',
    }
    target_time = basetime + oneday*timedelta
    try:
        return datetime.datetime.strftime(target_time,
                                          target_type_dict[target_type])
    except KeyError as e:
        raise KeyError("`target_type` must in %s" % target_type_dict.keys())


def listConverter(*args, **kwargs):
    """
    listConverter(*args, **kwargs)
    Convert int, tuple, etc to list with target type if it can be
    @kwargs['target_type']<var_type>: int, str, unicode, float, Deciaml
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


@timeDecorator
def testFunc(*args, **kwargs):
    """Test"""
    return listConverter(1, 2, 3, 4, 5, (6, 7), ['a', 'b', 8],
                         target_type=float)


class csvManager(object):
    def __init__(self, filename, mode='wb', filedir='./'):
        """
        csvManager(self, filename, filedir='./', mode='wb')
        wrapper csv model, adapt to Chinese
        @filename<str>: file name
        @mode<str>: open_mode
        @filedir<str>: filedir to save file

        """
        # makedirs if not exsit
        os.makedirs(filedir) if not os.path.isdir(filedir) else True
        # create csv file
        filename += '.csv' if not filename.endswith('.csv') else ''
        _full_filename = os.path.join(filedir, filename)
        _write_bom = False if os.path.isfile(_full_filename) else True
        self._file = open(_full_filename, mode)

        # adapt to Chinese
        self._file.write('\xEF\xBB\xBF') if _write_bom else None

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
        """
        mysqlManager(self, host, user, passwd, db, port=3306, charset='utf8')
        Connect to mysql
        @host<str>
        @user<str>
        @passwd<str>
        @db<str>
        @port<int>
        @charset<str>: same in MySQLdb.connect
        """
        try:
            self._conn = MySQLdb.connect(host=host, user=user, passwd=passwd,
                                         db=db, port=port, charset=charset)
            self._curs = self._conn.cursor()
        except:
            raise

    @timeDecorator
    def execute(self, sql, debug=False, **kwargs):
        """
        execute(self, sql, debug=False, **kwargs)
        Generate and execute sql
        @sql<str>: sql or sql model
        @kwargs<dict>: dict to decorate sql
        """
        sql = sql % kwargs
        try:
            self._curs.execute(sql)
            resp = self._curs.fetchall()
            if debug:
                print '<debug>', '\nresp:', resp, '\nsql:', sql
            return resp
        except:
            print sql
            raise

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


class zipManager(object):
    def __init__(self, filename, mode='r', filedir='./', pwd=''):
        """
        zipManager(filename, mode='w', filedir='./')
        read, write, or rewrite zipfile
        @filedir + @filename = abspath of zipfile to save zipfile in r_mode
        @filename<str>: *.zip
        @mode<str>: r, w, a
        @pwd<str>: password
        """
        _full_filename = os.path.join(filedir, filename)
        self._mode = mode
        self._pwd = pwd
        if self._mode in ('w', 'a'):
            os.path.makedirs(filedir) if not os.path.isdir(filedir) else None
            self._file = zipfile.ZipFile(_full_filename, self._mode,
                                         zipfile.ZIP_DEFLATED)
        elif self._mode in ('r',):
                self._file = zipfile(_full_filename, self._mode, pwd) if\
                    self._pwd else zipfile(_full_filename, self._mode)
        else:
            raise TypeError("zipfile model has no open_mode: %s" % self._mode)

    # def read(self):
    #     if self._mode in ('w', 'a'):
    #         raise TypeError("zipManager have no write_function with \
    #                         open_mode: %s" % self._mode)
    #     pass

    def extractall(self, todir='./'):
        if self._mode in ('w', 'a'):
            raise TypeError("zipManager have no extract_function with \
                            open_mode: %s" % self._mode)
        os.makedirs(todir) if not os.path.isdir(todir) else None
        #todo

    def write(self, fromname=None, fromdir='./'):
        """
        write(self,fromdir='./', fromname=None)
        write target file(s) to zip
        @fromname<str>: from file(s), it can be re_type such as *.csv
        @fromdir<str>: from dir
        """
        if self._mode in ('r',):
            raise TypeError("zipManager have no write_function with \
                            open_mode: %s" % self._mode)

        for _item in glob.glob(fromdir+fromname):
            self._file.write(_item)

    def __del__(self):
        try:
            self._file.close()
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
    # csvapp = csvManager('csvtest.csv', mode='ab')
    # csvapp.writerow(1, 2, 3, 4, 5, '动物', )

    # mysqlapp = mysqlManager('', '', '', '')
    # print mysqlapp.execute("select * from  u where u.id=")
    # with mysqlManager('', '', '', '') as mysqlapp:
    #     mysqlapp.execute("select * from  u where u.id=", debug=True)

    # print timeGenerator(target_type='month')
    # print timeGenerator(20160201, target_type='year')
    # print timeGenerator('2016-01-19', timedelta=-1)
    # print timeGenerator(20160244)

    # zipapp = zipManager('testzip.zip', 'w')
    # zipapp.write('*.csv')
    # with zipManager('testzip.zip', 'a') as zipapp:
    #     zipapp.write('*.csv')
    pass
