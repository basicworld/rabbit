# -*- coding:utf8 -*-
"""
Class function: connect and close mysql connections
Dont change anything
Author: wlf
Time: 20160222
"""
import MySQLdb
import sys


class mysqlConfig(object):
    def __init__(self):
        # super(mysqlConfig, self).__init__()
        pass

    def mysql_connect(self,host,user,passwd,db, port=3306, charset='utf8'):
        """
        Recommand func to connect mysql
        """
        self.conn = MySQLdb.connect(host=host,user=user,passwd=passwd,\
                    db=db, port=port, charset=charset) 
        self.curs = self.conn.cursor()

    def mysql_connect_default_host(self, host):
        """
        host must be in config

        Warning: whis is not a good func
        we suggest you using mysql_connect() func instead

        """
        try:
            from privateConfigs.companyInfo import companyInfoGetHost
            host_info = companyInfoGetHost(host)
            self.conn = MySQLdb.connect(host=host_info['host'], 
                user=host_info['user'], 
                passwd=host_info['passwd'], 
                db=host_info['db'], 
                port=3306, charset='utf8')
            self.curs = self.conn.cursor()
        except ImportError as e:

            print """ImportError: 
you must create a file in: ./privateConfigs/companyInfo.py 
add write at lest the follwwing:

def companyInfoGetHost(host):
    host_info = companyInfo().company_infos['host_info']
    try:
        return host_info[host]
    except:
        print "Error: host must in %s" % host_info.keys()
        raise KeyError
class companyInfo(object):
    def __init__(self):
        self.company_infos = {
            'host_info': {
                'host_01': {
                    'host': '0.0.0.0',
                    'user': 'username',
                    'passwd': 'passwd',
                    'db': 'database'},
            },
        }       
            """
            raise
            

    def mysql_close(self):
        """
        close mysql if possible
        """
        try:
            self.curs.close()
            self.conn.close()
        except:
            pass

    def mysql_curs_execute(self, sql, debug=False, **kwargs):
        """
        execute a typed sql
        @sql: a sql or sql model with dict, eg:
            sql = "select * from user_base;"
            sql_model = "select * from user_base where %(id_config)s"

            if you transport in sql, just use this func as you imaging, eg:
                app.mysql_curs_execute(sql)

            if you transport in sql_model , then you must add kwargs, eg:
                app.mysql_curs_execute(sql_model, id_config="id=1024")

        @debug: True to print sql, False to not print sql
        """
        try:
            sql = sql % kwargs
            if debug:
                print '-'*10, 'test mode start', '-'*10
                print sql
                print '-'*10, 'test mode start', '-'*10
            self.curs.execute(sql)
            return self.curs.fetchall()
        except AttributeError as e:
            print """Error: you must connect to mysql first!\n
Here is an example that you can follow in your project:
app = mysqlConfig()
app.mysql_connect(host,user,passwd,db, port=3306, charset='utf8')
app.mysql_curs_execute('select * from ord_base')
app.mysql_curs_execute('select * from ord_base where %(select_days)s', 
    select_days="updatetime>'20160222'")
app.mysql_close()
            """
            raise
        except:
            self.mysql_close()
            raise
# def mysqlDoctest():
#     """
#     # doctest
#     >>> app = mysqlConfig()
#     >>> app.mysql_curs_execute('select * from ord_base where %(select_days)s', \
#         debug=True, select_days="updatetime>'20160222'")
#     >>> app.mysql_close()

#     """
#     app = mysqlConfig()
#     # app.mysql_connect_default_host(host='host_01')
#     # app.mysql_curs_execute('select * from ord_base', debug=True)
#     app.mysql_curs_execute('select * from ord_base where %(select_days)s', 
#         debug=True, select_days="updatetime>'20160222'")
#     app.mysql_close()   

if __name__ == '__main__':
    """
    doctest test
    """
    pass
    # print "If doctest passed, this will be the only one output."
    # import doctest
    # doctest.testmod()
    # mysqlDoctest()
