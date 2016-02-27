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



class csvConfig(object):
    def csv_open(self, filename, filedir='./', open_type=False):
        """
        @filename
        """
        if not os.path.isdir(filedir):
            os.makedirs(filedir)

        fullpath = os.path.join(filedir, filename)
        if open_type:
            self.csv_file = open(fullpath, open_type) #ab wb
        else:
            if os.path.isfile(fullpath):
                open_type = 'ab'                
            else:
                open_type = 'wb'

        self.csv_file = open(fullpath, open_type)
        if open_type.startswith('w'):
            self.csv_file.write('\xEF\xBB\xBF')
        self.csv_writer = csv.writer(self.csv_file)#, dialect='excel')
       
    
    def csv_write(self,*args):
        """
        recursion
        """
        try:
            for arg in args:
                if isinstance(arg, (tuple, list)):
                    for i in arg:
                        if isinstance(i, (tuple, list)):
                            self.csv_write(i)
                        else:
                            # print '-', arg
                            self.csv_writer.writerow(arg)
                            break
                else:
                    self.csv_writer.writerow(args)
                    # print '-', args
                    break
        except:
            self.csv_close()
            raise

    def csv_close(self):
        self.csv_file.close()



if __name__ == '__main__':
    """test"""
    app = csvConfig() 
    app.csv_open(filename='test.csv', filedir='./test')
    app.csv_write([1,2,3,4])
    app.csv_write([u'测试', u'中文'])
    app.csv_close()




