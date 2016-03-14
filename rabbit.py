# -*- coding:utf8 -*-
"""
Intro: tool kit
Author: basicworld@163.com

function_performance_statistics(): decorator
time_generator(): create time
list_converter(): convert to list
CsvManager(): wrapper csv model
MySQLManager(): wrapper MySQLdb
ZipManager(): wrapper zipfile
EmailSender(): wrapper mailer
test_func(): inner test function

todo: auto set a carrot.py when run rabbit for the first time
"""

import os
import re
import sys
import csv
import glob
import time
import datetime
import mimetypes
import MySQLdb
import zipfile
import mailer
from carrot import EmailConfig as _EmailConfig
from carrot import Pop3SmtpImap
from decimal import Decimal

reload(sys)
sys.setdefaultencoding('utf8')
BASE_DIR = os.path.split(os.path.realpath(__file__))[0]


def function_performance_statistics(trace_this=True):
    """
    function_performance_statistics(trace_this=True)
    A decorator to show running time of a func
    @trace_this: print running_time or not

    eg:
    @function_performance_statistics(trace_this=True)
    def func...
    """
    from functools import wraps
    if trace_this:
        def time_decorator(func):
            @wraps(func)
            def _wrapper(*args, **kwargs):
                _start_time = datetime.datetime.now()
                _resp = func(*args, **kwargs)
                _end_time = datetime.datetime.now()
                _time_diff = (_end_time - _start_time).microseconds / 1000
                print (u"<%s> used %s ms." % (func.__name__, _time_diff))
                return _resp
            return _wrapper
    else:
        @wraps(func)
        def time_decorator(func):
            return func
    return time_decorator


def time_generator(basetime='', timedelta=0, target_type='day'):
    """
    time_generator(basetime='', timedelta=0, target_type='day')
    Generate time with target_type
    @basetime: input a time or None by default
    @timedelta: basetime + timedelta = target_time
    @target_type: day, month, year, month_start

    # doctest
    >>> time_generator(basetime='20160310')
    '2016-03-10'
    >>> time_generator(basetime='20160310', target_type='month_start')
    '2016-03-01'
    >>> time_generator(basetime='20160310', target_type='year')
    '2016'
    >>> time_generator(basetime='20160310', timedelta=-1, target_type='day')
    '2016-03-09'
    >>> time_generator(basetime='20160310', timedelta=30, target_type='month')
    '2016-04'
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

    _oneday = datetime.timedelta(days=1)
    _target_type_dict = {
        'year': '%Y',
        'month': '%Y-%m',
        'month_start': '%Y-%m-01',
        'day': '%Y-%m-%d',
        'hour': '%Y-%m-%d %H:00:00',
        'minute': '%Y-%m-%d %H:%M:00',
        'second': '%Y-%m-%d %H:%M:%S',
        'email_time': "%a, %d %b %Y %H:%M:%S %z",
    }
    _target_time = basetime + _oneday * timedelta
    try:
        return datetime.datetime.strftime(_target_time,
                                          _target_type_dict[target_type])
    except KeyError as e:
        raise KeyError("`target_type` must in %s" % _target_type_dict.keys())


def list_converter(*args, **kwargs):
    """
    list_converter(*args, **kwargs)
    Convert int, tuple, etc to list with target type if it can be
    @kwargs['target_type']<var_type>: int, str(unicode), unicode,
                                      float, Deciaml

    # doctest
    >>> list_converter(1, 2, 3)
    [1, 2, 3]
    >>> list_converter(1, 2, 3, target_type=float)
    [1.0, 2.0, 3.0]
    >>> list_converter(1, 2, 3, target_type=str)
    [u'1', u'2', u'3']
    >>> list_converter('a', 'b', '3', target_type=int)
    ['a', 'b', 3]
    >>> list_converter(1, 2, (3, 4), [[[5], 6], 7], )
    [1, 2, 3, 4, 5, 6, 7]
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


class CsvManager(object):
    def __init__(self, filename, mode='wb', filedir='./'):
        """
        CsvManager(self, filename, filedir='./', mode='wb')
        <class>: wrapper csv model, adapt to Chinese
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
        items = list_converter(args)
        if items:
            self._writer.writerow(items)

    def close(self):
        """
        use it when you want to close it manually
        """
        if not self._file.closed:
            self._file.close()

    def __del__(self):
        if not self._file.closed:
            self._file.close()

    def __enter__(self):
        return self

    def __exit__(self, *unused):
        pass


class MySQLManager(object):
    def __init__(self, host, user, passwd, db, port=3306, charset='utf8'):
        """
        MySQLManager(self, host, user, passwd, db, port=3306, charset='utf8')
        <class>: Connect to mysql
        @host<str>
        @user<str>
        @passwd<str>
        @db<str>
        @port<int>
        @charset<str>: same in MySQLdb.connect
        """
        try:
            self._conn = MySQLdb.connect(host=host,
                                         user=user,
                                         passwd=passwd,
                                         db=db,
                                         port=port,
                                         charset=charset)
            self._curs = self._conn.cursor()
        except:
            raise

    @function_performance_statistics()
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

    def close(self):
        """
        use it when you want to close it manually
        """
        try:
            self._conn.commit()
            self._curs.close()
            self._conn.close()
        except:
            pass

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


class ZipManager(object):
    def __init__(self, filename, mode='r', filedir='./', pwd=''):
        """
        ZipManager(filename, mode='w', filedir='./')
        <class>: read, write, or rewrite zipfile
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
            self._file = zipfile.ZipFile(_full_filename,
                                         self._mode,
                                         zipfile.ZIP_DEFLATED)
        elif self._mode in ('r',):
                self._file = zipfile(_full_filename, self._mode, pwd) if\
                    self._pwd else zipfile(_full_filename, self._mode)
        else:
            raise TypeError("zipfile model has no open_mode: %s" % self._mode)

    # def read(self):
    #     if self._mode in ('w', 'a'):
    #         raise TypeError("ZipManager have no write_function with \
    #                         open_mode: %s" % self._mode)
    #     pass

    # def extractall(self, todir='./'):
    #     if self._mode in ('w', 'a'):
    #         raise TypeError("ZipManager have no extract_function with \
    #                         open_mode: %s" % self._mode)
    #     os.makedirs(todir) if not os.path.isdir(todir) else None
    #     # todo

    def write(self, zipfile='.*', zipdir='./', zipfolder=False):
        """
        write(self, zipdir='./', zipfile=None)
        write target file(s) to zip
        @zipfile<str>: from file(s), it can be re_type such as .*\.csv
        @zipdir<str>: from dir
        @zipfolder<bool>: zip folder or not
        """
        if self._mode in ('r',):
            raise TypeError("ZipManager have no write_function with \
                            open_mode: %s" % self._mode)

        # zip folder
        if zipfolder:
            zipdir_len = len(zipdir.rstrip(os.sep)) + 1
            for dirname, subdirs, files in os.walk(zipdir):
                for filename in files:
                    if re.search(zipfile, filename):
                        path = os.path.join(dirname, filename)
                        entry = path[zipdir_len:]
                        self._file.write(path, entry)

        #not zip folder
        else:
            for _item in glob.glob(os.path.join(zipdir, '*')):
                if re.search(zipfile, _item) and os.path.isfile(_item):
                    self._file.write(_item)

    def close(self):
        """
        use it when you want to close it manually
        """
        try:
            self._file.close()
        except:
            pass

    def __del__(self):
        try:
            self._file.close()
        except:
            pass

    def __enter__(self):
        return self

    def __exit__(self, *unused):
        pass


class EmailSender(object):
    def __init__(self, **kwargs):
        """
        easy to use mail
        @To<str_list>: list of users you want to send email
        @Subject<str>
        @Body<str or fileObject>
        @attach<None or str or filename>
        @html_model<fileObject>: a html file, default use model in parrot
        @body_wrapper<dict>: use to pack html_model
        @show_warning<str>: show warning msg or not
        """
        params = {}
        for key, value in kwargs.items():
            params[key.lower()] = value

        # message setting
        self._to               = params.get('to', None)
        self._subject          = params.get('subject', None)
        self._body             = params.get('body', None)
        self._attach           = params.get('attach', None)
        # self._date           = params.get('date', None)
        # self._html           = params.get('html', None)
        # self._from           = params.get('from', None)
        # self._rto            = params.get('rto', None)
        # self._cc             = params.get('cc', None)
        # self._bcc            = params.get('bcc', None)
        # self._charset        = params.get('charset', None)
        # self._headers        = params.get('headers', None)
        self._html_model       = params.get('html_model', None)
        self._body_wrapper     = params.get('body_wrapper', None)

        # mailer setting
        self._host             = params.get('host', None)
        self._port             = params.get('port', None)
        self._use_ssl          = params.get('use_ssl', None)
        self._usr              = params.get('usr', None)
        self._pwd              = params.get('pwd', None)
        # self._use_tls        = params.get('use_tls', False)
        # self._use_plain_auth = params.get('use_plain_auth', False)
        # self._timeout        = params.get('timeout', None)

        # signature
        self._signature        = params.get('signature', None)
        self._show_warning     = params.get('show_warning', False)

        # load config data from carrot
        self._emailconfig      = _EmailConfig()
        self._serverconfig     = Pop3SmtpImap().server

    @function_performance_statistics(True)
    def send(self):
        """send email"""
        if not self.check():
            return False

        self._build_message()
        _sender = mailer.Mailer(host=self._host,
                                usr=self._usr,
                                port=self._port,
                                use_ssl=self._use_ssl,
                                pwd=self._pwd)
        _sender.send(self._message)
        return True

    @property
    def pwd(self):
        print self._pwd

    @pwd.setter
    def pwd(self, value):
        """todo"""
        pass

    @property
    def usr(self):
        return self._usr, self._pwd, self._signature

    @usr.setter
    def usr(self, value):
        try:
            _server       = re.findall('@(.*)\.', value)[0]
            self._host    = self._serverconfig[_server]['smtp']['host']
            self._port    = self._serverconfig[_server]['smtp']['port'][0]
            self._use_ssl = self._serverconfig[_server]['smtp']['ssl']
        except:
            print "[Warning] Invalid usr, or mail server not config in carrot"
            return False
        usr_in_carrot = False
        for acc in self._emailconfig.account:
            if value in acc['usr']:
                usr_in_carrot   = True
                self._usr       = acc['usr']
                self._pwd       = acc['pwd']
                self._signature = acc['signature']

        if not usr_in_carrot:
            self._usr = value

    @property
    def attach(self):
        return self._attach

    @attach.setter
    def attach(self, value):
        """append attach one by one"""
        if not os.path.isfile(value):
            print('Attach %s not exsit' % value)
        else:
            self._attach = (value)

    @property
    def to(self):
        return self._to

    @to.setter
    def to(self, value):
        if isinstance(value, (str, unicode)):
            value = [value]
        self._to = self._setter(value, check_type=('@', list))

    @property
    def subject(self):
        return self._subject

    @subject.setter
    def subject(self, value):
        self._subject = self._setter(value, check_type=(str, unicode))

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, value):
        self._body = self._setter(value, check_type=(str, unicode))

    @property
    def body_wrapper(self):
        return self._body_wrapper

    @body_wrapper.setter
    def body_wrapper(self, value):
        self._body_wrapper = self._setter(value, check_type=dict)

    @property
    def html_model(self):
        return self._html_model

    @html_model.setter
    def html_model(self, value):
        self._html_model = self._setter(value, check_type='file')

    @staticmethod
    def _body_convert(body):
        _collector = ""
        if os.path.isfile(body):
            for line in open(body):
                _collector += '<p>%s</p>' % line
        else:
            for line in body.replace('    ', '').split('\n'):
                _collector += '<p>%s</p>' % line
        return _collector

    def check(self):
        need_set_para = 0

        # usr pwd to must be set
        error_msg = ""
        if not (self._usr):
            error_msg     += '[Error] usr is empty%s' % os.linesep
            need_set_para += 1
        if not (self._pwd):
            error_msg     += '[Error] pwd is empty%s' % os.linesep
            need_set_para += 1
        if not (self._to):
            error_msg     += '[Error] To(reciever) is empty%s' % os.linesep
            need_set_para += 1

        # use default if not exit
        warning_msg = ""
        if not (self._html_model):
            warning_msg += """[Warning] HTML_model is empty, using \
                default%s""" % os.linesep
            self._html_model = self._emailconfig.html_model
        if not (self._body):
            warning_msg += """[Warning] body is empty, using default%s""" \
                % os.linesep
            self._body = self._emailconfig.body
        if not (self._subject):
            warning_msg += """[Warning] subject is empty, using default%s""" \
                % os.linesep
            self._subject = "Hello world from rabbit"

        if need_set_para:
            print 'At least %s parameters should be set:' % need_set_para
            print error_msg
            if self._show_warning:
                print warning_msg
            return False
        return True

    def _build_message(self):
        """build mesage"""
        self._message         = mailer.Message(charset="utf-8")
        self._message.From    = self._usr
        self._message.To      = self._to
        self._message.Subject = self._subject

        if not self._body_wrapper:
            self._body_wrapper = {
                'body': self._body_convert(self._body),
                'signature': self._signature,
                'send_time': '',
            }

        for key, value in self._body_wrapper.items():
            self._html_model = self._html_model.replace('<!--%s-->' %
                                                        key, value)
        self._message.Html = self._html_model
        if self._attach:
            ext = os.path.splitext(self._attach)[-1]
            mtype = mimetypes.types_map[ext]
            self._message.attach(filename=self._attach,
                                 cid=None,
                                 mimetype=mtype,
                                 content=None,
                                 charset=None)

    @staticmethod
    def _setter(value, check_type=False):
        """for *.setter"""
        try:
            if check_type:
                if check_type in ('@', 'email'):
                    if not (isinstance(value, (str, unicode)) and
                            '@' in value):
                        raise ValueError
                    return value
                elif check_type in (('@', list), ('email', list)):
                    for val in value:
                        if not (isinstance(val, (str, unicode)) and
                                '@' in val):
                            raise ValueError
                    return value
                elif check_type in ('file', ):
                    if not os.path.isfile(value):
                        raise ValueError
                    return open(value).read()
                else:
                    if not isinstance(value, check_type):
                        raise ValueError
                    return value
            else:
                return value
        except ValueError as e:
            return None


@function_performance_statistics(True)
def test_func(x, y):
    return x + y


if __name__ == '__main__':
    a        = EmailSender()
    a.usr    = '@itprofessor.cn'
    a.to     = ['basicworld@126.com']
    a.attach = './rabbit.zip'
    # a.attach = './carrot.py'
    a.send()
