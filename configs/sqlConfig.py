# -*- coding:utf8 -*-
"""
Class function: save sql models
Author: wlf
Time: 20160222
"""
def sqlConfigGetItem(passport):
    app = sqlConfig()
    return app.sql_get(passport)
    
class sqlConfig(object):
    def sql_get(self, *args):
        try:
            return self.model[args]
        except:
            raise
            
    def __init__(self):
        self.model = {
            ('sql',): # you can insert ps here
                r""" 
                test
                """,

        }


if __name__ == '__main__':
    app = sqlConfig()
    print app.sql_get('sql')
