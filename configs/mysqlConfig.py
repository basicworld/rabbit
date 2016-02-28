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
    # def __init__(self):
    #     # super(mysqlConfig, self).__init__()
    #     pass

    def __init__(self,host,user,passwd,db, port=3306, charset='utf8'):
        """
        Recommand func to connect mysql
        """
        self._conn = MySQLdb.connect(host=host,user=user,passwd=passwd,\
                    db=db, port=port, charset=charset) 
        self._curs = self._conn.cursor()

    def __del__(self):
        """
        close mysql if possible
        """
        try:
            self._conn.commit()
            self._curs.close()
            self._conn.close()
        except:
            pass

    def __enter__(self):
        return self.mysql_curs_execute

    def __exit__(self, *unused):
        try:
            self._conn.commit()
            # self._curs.close()
            # self._conn.close()
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
                print sql
            if self._curs.execute(sql) and not "insert" in sql.lower():
                return self._curs.fetchall()

        except AttributeError as e:
            print """Error: you must connect to mysql first!\n
                Here is an example that you can follow in your project:
                app = mysqlConfig(host,user,passwd,db, port=3306, charset='utf8')
                app.mysql_curs_execute('select * from ord_base')
                app.mysql_curs_execute('select * from ord_base where 
                    %(select_days)s', 
                    select_days="updatetime>'20160222'")
            """
            raise 

if __name__ == '__main__':
    """
    doctest test
    """

    app = mysqlConfig(host='1',user='reader',passwd='123456',
        db='test', port=3306, charset='utf8')
    print app.mysql_curs_execute(r'select * from MOVIE_STAR limit 1;')
    # app.mysql_curs_execute(r"""INSERT INTO MOVIE_STAR(USER_NAME) VALUES('da;niao');""")

    # with mysqlConfig(host='1',user='reader',passwd='123456',
    #     db='test', port=3306, charset='utf8') as curs:
    #     print curs(r'select * from MOVIE_STAR limit 1;')