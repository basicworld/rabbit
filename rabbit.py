# -*- coding:utf8 -*-
"""
Usage:
  rabbit.py imgetter <url> [<savedir>]
  rabbit.py test_func <args>

Arguments:
  url       url
  savedir   dirpath

Options:
  -h --help
"""
# todo: url2ip() to convert url to ip

import csv
import carrot
import datetime
import glob
import imaplib
import logging
import logging.config
import mailer  # pip
import mimetypes
import MySQLdb  # pip / easy_install
import os
import purl  # pip
import re
import sys
import time
import requests  # pip
import xlrd  # pip
import xlwt  # pip
import zipfile
from cStringIO import StringIO
from decimal import Decimal
from docopt import docopt  # pip
from multiprocessing import Pool
from multiprocessing import cpu_count
from urlparse import urljoin
from urlparse import urlparse
from urlparse import urlunparse
from posixpath import normpath
from PIL import Image  # pip
reload(sys)
sys.setdefaultencoding('utf8')
BASE_DIR = os.path.split(os.path.realpath(__file__))[0]


def xurljoin(base, url):
    """
    xurljoin(base, url)
    improved func for uelpsrse.urljoin
    article from: http://www.coder4.com/archives/2674
    """
    url1 = urljoin(base, url)
    arr = urlparse(url1)
    path = normpath(arr[2])
    return urlunparse((arr.scheme, arr.netloc, path,
                       arr.params, arr.query, arr.fragment))


def imgetter(url, savedir=''):
    """
    download img from url, save to savedir
    @savedir path to save img

    usage:
    >>> url = 'http://www.itprofessor.cn/media/media.jpg'
    >>> imgetter(url)
    """
    url = url.strip()
    url_resp = requests.get(url)
    img = Image.open(StringIO(url_resp.content)) if url_resp.ok else None
    if isinstance(img, Image.Image):
        parse = purl.URL(url)
        imgname = os.path.splitext(parse.path().strip('/').
                                   replace('/', '_'))[0]
        savedir = savedir if savedir else ''
        img.save(filer('%s.%s' % (imgname, img.format.lower()),
                 savedir))
        return True
    else:
        raise TypeError('not a image url: %s' % url)


class PoolManager(object):
    def __init__(self, args):
        """
        PoolManager(args)

        usage:
        >>> jobs = [(func1, args1), (func2, args2)]
        >>> p = PoolManager(jobs)
        >>> p.run()
        """
        self.pool = Pool(cpu_count())
        self.args = [i for i in args]

    def add(self, args):
        self.args += [i for i in args]

    def run(self):
        self.collector = []
        for func, argv in self.args:
            result = self.pool.apply_async(func, (argv, ))
            self.collector.append([func.__name__, argv, result])
        self.pool.close()
        self.pool.join()

        # num of jobs in pool
        jobs_num = len(self.collector)
        jobs_successful = 0
        bar_length = 30
        while jobs_successful < jobs_num:
            for index, job in enumerate(self.collector):
                if jobs_num > 1:
                    percent = index / float(jobs_num - 1) * 100
                    hashes = '#' * int(percent / 100.0 * bar_length)
                    spaces = ' ' * (bar_length - len(hashes))
                    sys.stdout.write("\r%s: [%s] %d%%" % ('Percent',
                                                          hashes + spaces,
                                                          percent))
                    sys.stdout.flush()

                result = job[-1]
                if not isinstance(result, list) and result.successful():
                    del self.collector[index][-1]
                    self.collector[index].append(result.get())
                    jobs_successful += 1
        sys.stdout.write('\n')
        sys.stdout.flush()
        return self.collector


def filer(filename='', filedir='./'):
    """
    filer(filename='', filedir='./')
    return fullpath
    auto create filedir
    if filename is null, only filedir be created
    """
    filedir = os.path.abspath(filedir)
    os.makedirs(filedir) if not os.path.isdir(filedir) else None
    return (os.path.join(filedir, filename) if filename else filedir)


def logger(name, logname, logdir='./'):
    """
    logger(name, logname, logdir='./')
    high level logging

    how to use:
    alog = logger('default', 'log13.txt')
    alog.debug('debug message!')
    alog.info('info message!')
    alog.error('error message')
    alog.critical('critical message')
    alog.warning('warning message')
    """
    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'default': {'format': '%(asctime)s %(levelname)s %(message)s',
                        'datefmt': '%Y-%m-%d %H:%M:%S',
                        },
            'verbose': {'format': '%(asctime)s %(levelname)s %(module)s \
                %(process)d %(thread)d %(message)s',
                        'datefmt': '%Y-%m-%d %H:%M:%S',
                        },
            'simple': {'format': '%(levelname)s %(message)s',
                       'datefmt': '%Y-%m-%d %H:%M:%S'
                       },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'stream': 'ext://sys.stdout',
            },
            'file': {
                'level': 'INFO',
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'default',
                'filename': filer(logname, logdir),
                'maxBytes': 1024000,
                'backupCount': 3,
                'encoding': 'utf8',
            },
        },
        'loggers': {
            'default': {
                'level': 'DEBUG',
                'handlers': ['console', 'file'],
            },
            'file': {
                'level': 'INFO',
                'handlers': ['file'],
            }
        },
        # 'disable_existing_loggers': False,
    })
    return logging.getLogger(name)


def func_monitor(trace_this=True):
    """
    func_monitor(trace_this=True)
    A decorator to show running time of a func
    @trace_this: print running_time or not

    eg:
    @func_monitor(trace_this=True)
    def func...
    """
    from functools import wraps
    if trace_this:
        def _time_decorator(func):
            @wraps(func)
            def _wrapper(*args, **kwargs):
                _start_time = datetime.datetime.now()
                _resp = func(*args, **kwargs)
                _end_time = datetime.datetime.now()
                _time_diff = (_end_time - _start_time).total_seconds()
                print (u"<%s> used %s s." % (func.__name__, _time_diff))
                return _resp
            return _wrapper
    else:
        @wraps(func)
        def _time_decorator(func):
            return func
    return _time_decorator


def time_builder(basetime='', timedelta=0, target_type='day'):
    """
    time_builder(basetime='', timedelta=0, target_type='day')
    Generate time with target_type
    @basetime: input a time or None by default
    @timedelta: basetime + timedelta = target_time
    @target_type: day, month, year, month_start

    # doctest
    >>> time_builder(basetime='20160310')
    '2016-03-10'
    >>> time_builder(basetime='20160310', target_type='month_start')
    '2016-03-01'
    >>> time_builder(basetime='20160310', target_type='year')
    '2016'
    >>> time_builder(basetime='20160310', timedelta=-1, target_type='day')
    '2016-03-09'
    >>> time_builder(basetime='20160310', timedelta=30, target_type='month')
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
        'dbYHMS/': '%d/%b/%Y:%H:%M:%S',
        'dbY/': '%d/%b/%Y',  # '27/Mar/2016'
        'dbY-': '%d-%b-%Y',  # '27-Mar-2016'
        'mdYHMS/': '%m/%d/%Y:%H:%M:%S',
        'mdY000/': '%m/%d/%Y:00:00:00',
        'full_time': "%a, %d %b %Y %H:%M:%S %z",
    }
    _target_time = basetime + _oneday * timedelta
    try:
        return datetime.datetime.strftime(_target_time,
                                          _target_type_dict[target_type])
    except KeyError as e:
        raise KeyError("`target_type` must in %s" % _target_type_dict.keys())


def lister(*args, **kwargs):
    """
    lister(*args, **kwargs)
    Convert int, tuple, etc to list with target type if it can be
    @kwargs['target_type']<var_type>: int, str(unicode), unicode,
                                      float, Deciaml

    # doctest
    >>> lister(1, 2, 3)
    [1, 2, 3]
    >>> lister(1, 2, 3, target_type=float)
    [1.0, 2.0, 3.0]
    >>> lister(1, 2, 3, target_type=str)
    [u'1', u'2', u'3']
    >>> lister('a', 'b', '3', target_type=int)
    ['a', 'b', 3]
    >>> lister(1, 2, (3, 4), [[[5], 6], 7], )
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


def distinct(*args):
    """
    distinct(*args)
    return distinct items
    """
    items = lister(args)
    func = lambda x, y: x if y in x else x + [y]
    return reduce(func, [[], ] + items)


def xls2dict(filename):
    """
    xls2dict(filename)
    get a xls or xlsx, return a list
    """
    collector = []
    _full_filename = os.path.abspath(filename)
    try:
        data = xlrd.open_workbook(_full_filename)
    except:
        raise ValueError('%s is not a xls_type file' % filename)

    for table in data.sheets():
        table_collector = []
        nrows = table.nrows
        ncols = table.ncols
        if not (nrows and ncols):
            continue
        for row in range(nrows):
            table_collector.append(table.row_values(row))
        table_info = {
            'name': table.name,
            'data': table_collector,
            'rows': nrows,
            'cols': ncols,
            'title': table.row_values(0)
        }
        collector.append(table_info)
    return collector


def csv2xls(filename):
    """
    csv2xls(filename)
    given a csv file, convert to xls and save at the same dir
    warning: maxline_of_csvfile <=65535
    """
    _full_filename = os.path.abspath(filename)
    try:
        _csv_reader = csv.reader(open(_full_filename))
    except:
        raise ValueError('%s is not a csv_type file' % filename)
    _xls_name = re.sub('\..*$', '.xls', _full_filename, 1)
    _xlsapp = XlsManager(_xls_name)
    for row in _csv_reader:
        _xlsapp.writerow(row)

    _xlsapp.close()
    return True


def imager(url, **kwargs):
    """
    default url
    """
    pass


class CsvManager(object):
    def __init__(self, filename, mode='wb', filedir='./'):
        """
        CsvManager(filename, mode='wb', filedir='./')
        <class>: wrapper csv model, adapt to Chinese
        @filename<str>: file name
        @mode<str>: open_mode
        @filedir<str>: filedir to save file
        """
        # makedirs if not exsit
        filedir = os.path.abspath(filedir)
        os.makedirs(filedir) if not os.path.isdir(filedir) else True
        # create csv file
        filename = unicode(filename)
        filename += '.csv' if not filename.endswith('.csv') else ''
        self._full_filename = os.path.join(filedir, filename)
        _write_bom = False if os.path.isfile(self._full_filename) else True
        try:
            self._file = open(self._full_filename, mode)
        except IOError as e:
            raise IOError("Permission denied: close file %s and try again" % self._full_filename)

        # adapt to Chinese
        if _write_bom or mode.startswith('w'):
            self._file.write('\xEF\xBB\xBF')

        self._writer = csv.writer(self._file)

    def writerow(self, *args):
        items = lister(args)
        if items:
            self._writer.writerow(items)

    def close(self):
        """
        use it when you want to close it manually
        """
        if not self._file.closed:
            self._file.close()

    def csv2xls(self, delete_csv=False):
        """
        convert csv file to xls file
        must be used after csv file closed
        """
        self.close()
        resp = csv2xls(self._full_filename)
        if delete_csv:
            os.remove(self._full_filename)

    def __del__(self):
        if not self._file.closed:
            self._file.close()

    def __enter__(self):
        return self

    def __exit__(self, *unused):
        pass


class XlsManager(object):
    def __init__(self, filename, mode='w', filedir='./'):
        """
        XlsManager(filename, mode='w', filedir='./')
        write xls
        todo: read xls
        """
        self._file = xlwt.Workbook()
        self._is_open = True
        # makedirs if not exsit
        filedir = os.path.abspath(filedir)
        os.makedirs(filedir) if not os.path.isdir(filedir) else True
        # create csv file
        filename += '.xls' if not filename.endswith('.xls') else ''
        self._full_filename = os.path.join(filedir, filename)

        self._style = xlwt.XFStyle()
        _font = xlwt.Font()
        _font.name = "SimSun"  # 'Times New Roman'
        _font.height = 220
        _font.charset = xlwt.Font.CHARSET_SYS_DEFAULT
        self._style.font = _font

        # num of sheet
        self._sheet_count = 0

        # create default sheet
        self._sheet_count += 1
        # add_sheet(sheetname, cell_overwrite_ok=False)
        self._sheet = self._file.add_sheet('sheet%s' % self._sheet_count,
                                           cell_overwrite_ok=True)
        self._row = 0
        self._col = 0

    def add_sheet(self):
        """
        sheet name start from sheet2
        """
        self._sheet_count += 1
        self._sheet = self._file.add_sheet('sheet%s' % self._sheet_count,
                                           cell_overwrite_ok=True)
        self._row = 0
        self._col = 0

    def writerow(self, *args):
        # write(r, c, label='', style=<xlwt.Style.XFStyle object>)
        items = lister(args, target_type=unicode)
        if items:
            for col, item in enumerate(items):
                self._sheet.write(self._row, col, item, self._style)
        self._row += 1
        self._col = col + 1

    def close(self):
        """
        save manually
        """
        # save(filename_or_stream)
        if self._is_open:
            self._file.save(self._full_filename)
            self._is_open = False

    def __del__(self):
        # save(filename_or_stream)
        if self._is_open:
            self._file.save(self._full_filename)
            self._is_open = False

    def __enter__(self):
        return self

    def __exit__(self, *unused):
        pass


class MySQLManager(object):
    def __init__(self, host, user, passwd, db, port=3306, charset='utf8'):
        """
        MySQLManager(host, user, passwd, db, port=3306, charset='utf8')
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
    def __init__(self, filename, mode='w', filedir='./', pwd=''):
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
        @attach<filename or filename_list>
        @debug<str>: show warning msg or not
        @retype_body: if True, your body will be retype: line --> <p>line</p>
        """
        log_time = str(time.time())[:6]
        self.logger = logger('file', 'log_email_%s.log' % log_time, './tmp')
        self.logger.info('%s%s' % ('-' * 20, 'email start'))
        self.logger.info('%s%s' % ('-' * 20, time.ctime()))
        params = {}
        for key, value in kwargs.items():
            params[key.lower()] = value

        # message setting
        self._to        = params.get('to', [])
        self._subject   = params.get('subject', None)
        self._body      = params.get('body', None)
        self._attach    = params.get('attach', [])
        self._retype_body = params.get('retype_body', False)

        # mailer setting
        self._host      = params.get('host', None)
        self._usr       = params.get('usr', None)
        self._pwd       = params.get('pwd', None)

        # signature
        self._signature = params.get('signature', None)
        self._debug     = params.get('debug', False)

        # message
        _date           = time_builder(target_type='full_time')
        self._message   = mailer.Message(Date=_date, charset="utf-8")

    def send(self):
        """send email"""
        if not self._check():
            return False

        self._build_message()
        _sender = mailer.Mailer(host=self._host,
                                usr=self._usr,
                                port=self._port,
                                use_ssl=True,
                                pwd=self._pwd)
        try:
            _sender.send(self._message)
        except:
            self.logger.error("[Error] Something wrong when sending email")
            print ("[Error] Something wrong when sending email")
            raise
        self.logger.info('%s%s' % ('-' * 20, time.ctime()))
        self.logger.info('%s%s' % ('-' * 20, 'email end with success'))
        return True

    @property
    def pwd(self):
        return self._pwd

    @pwd.setter
    def pwd(self, value):
        if isinstance(value, (str, unicode)):
            self._pwd = str(value)
        else:
            self.logger.error("Str or unicode anticipated, \
                got %s" % type(value))
            raise TypeError("Str or unicode anticipated, got %s" % type(value))

    @property
    def usr(self):
        return self._usr

    @usr.setter
    def usr(self, value):
        """
        @value: usrname
        """
        # parse email server
        _resp = re.search("@(.*)", value.strip())
        if _resp:
            _server = _resp.group(1)
            # get server host and port
            _resp = carrot.EMAIL_SERVER.get(_server)
            if _resp:
                self._host = _resp['smtp']['host']
                self._port = _resp['smtp']['port'][0]
            else:
                self.logger.error("server error: %s" % _resp)
                raise KeyError("Email server not in carrot.py")
        else:
            self.logger.error("email error: %s" % value)
            raise KeyError("Invalid email address")

        _resp = carrot.EMAIL_ACCOUNT.get(value, None)
        if _resp:
            self._usr       = _resp['usr']
            self.logger.info('get usr: %s' % self._usr)
            self._pwd       = _resp['pwd']
            self.logger.info('get pwd from file')
            self._signature = _resp['signature']
        else:
            self._usr       = value
            self.logger.info('get usr: %s' % self._usr)
            self._pwd       = raw_input("Insert your email pwd:")
            self.logger.info('get pwd from input')
            self._signature = value

    @property
    def attach(self):
        return self._attach

    @attach.setter
    def attach(self, *args):
        """
        add attach to Mesage directly
        @args: filenames
        """
        for filename in lister(args):
            if os.path.isfile(filename):
                ext   = os.path.splitext(filename)[-1]
                mtype = mimetypes.types_map.get(ext)
                self.logger.info('get attach: %s' % filename)
                self._message.attach(filename=filename,
                                     cid=None,
                                     mimetype=(mtype if mtype else None),
                                     content=None,
                                     charset=None)
            else:
                self.logger.warning("%s is not a file" % value)
                print ("%s is not a file" % value)

    @property
    def to(self):
        return self._to

    @to.setter
    def to(self, *args):
        """
        @args: email address
        """
        for email in lister(args):
            if isinstance(email, (str, unicode)) and '@' in email:
                self._to.append(email)
                self.logger.info('get receiver: %s' % email)
            else:
                self.logger.error("Invalid email address: %s" % email)
                raise KeyError("Invalid email address: %s" % email)

    @property
    def subject(self):
        return self._subject

    @subject.setter
    def subject(self, value):
        if isinstance(value, (str, unicode)):
            self._subject = value
            self.logger.info('get subject: %s' % value)
        else:
            self.logger.error("Str or unicode anticipated, \
                got %s" % type(value))
            raise TypeError("Str or unicode anticipated, got %s" % type(value))

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, value):
        if isinstance(value, (str, unicode)):
            if os.path.isfile(value):
                value = open(value).read()
            if self._retype_body:
                self._body = '\n'.join(['<p>' + i.strip() + '</p>'
                                       for i in value.split('\n')])
            else:
                self._body = unicode(value)
            self.logger.info('get body: %s...' % value[:10])
        else:
            self.logger.error("Str or unicode anticipated, \
                got %s" % type(value))
            raise TypeError("Str or unicode anticipated, got %s" % type(value))

    def _check(self):
        error = 0
        # usr pwd to must be set
        error_msg = ""
        if not (self._pwd):
            error_msg += '[Error] pwd is empty%s' % os.linesep
            error += 1
        if not (self._to):
            error_msg += '[Error] To(reciever) is empty%s' % os.linesep
            error += 1

        if error:
            self.logger.error('At least %s parameters should be set: \
                %s' % (error, error_msg))
            print ('At least %s parameters should be set:' % error)
            print error_msg
            return False
        else:
            self.logger.info('check pwd and receiver down')
            return True

    def _build_message(self):
        """build mesage"""
        try:
            self._message.From    = self._usr
            self._message.To      = self._to
            self._message.Subject = self._subject
            _body_wrapper = {
                'body': self._body,
                'signature': self._signature,
            }
            _html_model = carrot.EMAIL_HTML_MODEL
            for key, value in _body_wrapper.items():
                _html_model = _html_model.replace('<!--%s-->' % key, value)
            self._message.Html = _html_model
            self.logger.info('build message down')
        except:
            self.logger.error('fail to build message')
            raise


def email_parser(raw_email):
    """parse email and return dict
    @raw_email str
    """
    import email
    msg = email.message_from_string(raw_email)
    # print msg.keys()
    return {
        'subject': msg.get("subject"),
        'from': msg.get('from'),
        'to': msg.get('to'),
        'date': msg.get('Date')
    }


class EmailGetter(object):

    def __init__(self, **kwargs):
        """receive email"""
        log_time = str(time.time())[:6]
        self.logger = logger('file', 'log_email_%s.log' % log_time, './tmp')
        self.logger.info('%s%s' % ('-' * 20, 'email start'))
        self.logger.info('%s%s' % ('-' * 20, time.ctime()))
        params = {}
        for key, value in kwargs.items():
            params[key.lower()] = value
        self._usr = params.get('usr', None)
        self._pwd = params.get('pwd', None)

    @property
    def usr(self):
        return self._usr

    @usr.setter
    def usr(self, value):
        """
        @value: usrname
        """
        # parse email server
        _resp = re.search("@(.*)", value.strip())
        if _resp:
            _server = _resp.group(1)
            # get server host and port
            _resp = carrot.EMAIL_SERVER.get(_server)
            if _resp:
                self._host = _resp['imap']['host']
                self._port = _resp['imap']['port'][0]
            else:
                self.logger.error("server error: %s" % _resp)
                raise KeyError("Email server not in carrot.py")
        else:
            self.logger.error("email error: %s" % value)
            raise KeyError("Invalid email address")

        _resp = carrot.EMAIL_ACCOUNT.get(value, None)
        if _resp:
            self._usr = _resp['usr']
            self.logger.info('get usr: %s' % self._usr)
            self._pwd = _resp['pwd']
            self.logger.info('get pwd from file')
        else:
            self._usr = value
            self.logger.info('get usr: %s' % self._usr)
            self._pwd = raw_input("Insert your email pwd:")
            self.logger.info('get pwd from input')

    @property
    def pwd(self):
        return self._pwd

    @pwd.setter
    def pwd(self, value):
        if isinstance(value, (str, unicode)):
            self._pwd = str(value)
        else:
            self.logger.error("Str or unicode anticipated, \
                got %s" % type(value))
            raise TypeError("Str or unicode anticipated, got %s" % type(value))

    def get(self):
        """
        return email list
        """
        self.logger.info("connect to host %s: %s" % (self._host, self._port))
        self.M = imaplib.IMAP4_SSL(self._host, self._port)
        self.logger.info("login with usr %s" % self._usr)
        try:
            self.M.login(self._usr, self._pwd)
        except:
            raise
        self.logger.info("use INBOX")
        self.M.select("INBOX")
        self.logger.info("search new email %s" % self._usr)
        # typ, data = self.M.uid("SEARCH", "UNSEEN")
        typ, data = self.M.search(None, "UNSEEN")
        # time_builder(timedelta=-10, target_type='dbY-'))
        if typ == "OK":
            for uid in data[0].split():
                result, raw_email = self.M.fetch(uid, "(RFC822)")
                    # uid("FETCH", uid, "ALL")
                          # "(FLAGS BODY.PEEK[HEADER] BODYSTRUCTURE)")
                if result:
                    # self.M.store(uid, '+FLAGS', '\\Seen')  # mark as read
                    print email_parser(raw_email[0][1])
                    # for i in raw_email:
                    #     print i
        # print self._usr, self._pwd, self._host, self._port

    def close(self):
        try:
            self.M.logout()
        except:
            raise

    def mark(self, select_day, status):
        """todo use to mark emails"""
        pass
        # typ, data = M.search(None, '(BEFORE 01-Jan-2009)')
        # for num in data[0].split():
        #    M.store(num, '+FLAGS', '\\Seen')


@func_monitor(True)
def test_func(x, y):
    time.sleep(5)
    return x + y


if __name__ == '__main__':
    args = docopt(__doc__)
    if args.get('imgetter'):
        imgetter(args.get('<url>'), args.get('<savedir>'))
    # url = 'http://www.itprofessor.cn/media/media.jpg'
    # url = 'http://pic38.nipic.com/20140228/2531170_213554844000_2.jpg'
    # resp = imgetter(url)
    # print resp
    # test_func(1, 2)
    # emailget = EmailGetter()
    # emailget.usr = 'test@itprofessor.cn'
    # emailget.get()
    # emailget.close()

    # from optparse import OptionParser
    # usage = """%prog [-e <email>]"""
    # version = "%prog 1.0"
    # parser = OptionParser(usage=usage)
    # parser.add_option('-e', '--email',
    #                   dest='email',
    #                   help="-e usrname@example.com",
    #                   action="store_true")
    # (options, args) = parser.parse_args()
    # if options.email and args:
    #     a    = EmailSender()
    #     a.to = args
    #     # a.attach = './carrot.py'
    #     # a.attach = './rabbit.py'
    #     a.send()
    # else:
    #     raise ValueError("python rabbit.py -e <your_email>")
    # xlsapp = XlsManager('test.xls', 'w')
    # xlsapp.writerow(1, 2, 3, 4, 5)
    # xlsapp.close()

    # emailapp         = EmailSender()
    # emailapp.usr     = 'test@itprofessor.cn'
    # emailapp.to      = ['admin@wlfei.com', 'basicworld@163.com']
    # emailapp.subject = 'hello you'
    # emailapp.body    = """abc"""
    # emailapp.attach = ('rabbit.py', 'carrot.py')
    # emailapp.send()

    # csvapp = CsvManager('test.csv')
    # csvapp.writerow('122', '2')
    # csvapp.writerow('中文', 1, 2, 3)
    # csvapp.csv2xls()
    pass
