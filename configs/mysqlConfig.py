# -*- coding:utf8 -*-
"""
Class function: connect and close mysql connections
Dont change anything
Author: wlf
Time: 20160222
"""
import MySQLdb


class mysqlConfig(object):
    def __init__(self):
        # super(mysqlConfig, self).__init__()
        pass

    def mysql_connect(self,host,user,passwd,db, port=3306, charset='utf8'):
        """
        connect
        """
        self.conn = MySQLdb.connect(host=host,user=user,passwd=passwd,
                    db=db, port=port, charset=charset) 
        self.curs = self.conn.cursor()

    def mysql_connect_default_host(self, host):
        """host must be in config"""
        from privateConfigs.companyInfo import companyInfoGetHost
        host_info = companyInfoGetHost(host)
        self.conn = MySQLdb.connect(host=host_info['host'], user=host_info['user'], 
                    passwd=host_info['passwd'], db=host_info['db'], port=3306, charset='utf8')
        self.curs = self.conn.cursor()

    def mysql_close(self):
        """
        close
        """
        try:
            self.curs.close()
            self.conn.close()
        except:
            pass

    def mysql_curs_execute(self, sql, debug=False, *args, **kwargs):
        """
        execute a typed sql
        """
        try:
            sql = sql % kwargs
            if debug:
                print sql
            self.curs.execute(sql)
            return self.curs.fetchall()
        except:

            self.mysql_close()
            print sql
            raise

if __name__ == '__main__':
    

    app = mysqlConfig()
    app.mysql_connect_default_host(host='host_119')
    app.mysql_close()

