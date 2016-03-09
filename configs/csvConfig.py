# -*- coding:utf8 -*-
"""
Class function: create csv file
Dont change anything
Author: wlf
Time: 20160222
"""
import os
import csv
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from timeConfig import timeConfig
from convertConfig import convertToList


class csvConfig(object):
    def __init__(self, filename, filedir='./', open_type='wb'):
        """
        @filename
        """
        if not os.path.isdir(filedir):
            os.makedirs(filedir)

        _fullpath = os.path.join(filedir, filename)
        if open_type:
            pass # todo: test open_type
        else:
            open_type = 'ab' if os.path.isfile(_fullpath) else 'wb'

        _write_bom = False if os.path.isfile(_fullpath) else True
        self._csv_file = open(_fullpath, open_type)

        # write BOM to adapt Chinese
        if open_type.startswith('w') or _write_bom:
            self._csv_file.write('\xEF\xBB\xBF')
        self._csv_writer = csv.writer(self._csv_file)#, dialect='excel')
       
    def csv_write(self,*args):
        """
        write all args in one line
        """
        _resp_list = convertToList(args)
        if _resp_list and not self._csv_file.closed:
            self._csv_writer.writerow(_resp_list)


    def __del__(self):
        if not self._csv_file.closed:
            self._csv_file.close()


    def __enter__(self):
        return self.csv_write

    def __exit__(self, *unused):
        if not self._csv_file.closed:
            self._csv_file.close()

if __name__ == '__main__':
    """test"""
    app = csvConfig(filename='test2.csv', filedir='./test', open_type='wb')
    app.csv_write([1,2,3,4])
    app.csv_write([u'测试', u'中文'],[u'测试', u'中文'])

    with csvConfig(filename='test.csv', filedir='./test', open_type='wb') as csv_write:
        csv_write([1,2,3,4])
        csv_write([u'测试', u'中文'],[u'测试', u'中文'])



