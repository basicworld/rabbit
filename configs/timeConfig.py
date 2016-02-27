# -*- coding:utf8 -*-
"""
Class function: create time
Dont change anything
Author: wlf
Time: 20160223
"""
import datetime
import time


def timeConfig(base_day=False, days_before=0, detail='day'):
    '''
    return days before base_day
    default return today, eg, 2016-02-23
    base_day should like: '20160223', '2016-02-23'
    detail: year, day, start_day_of_month, month

    >>> timeConfig(base_day='20160123')
    2016-01-23

    '''

    if base_day:
        base_day = str(base_day)
        base_day = base_day.replace("-", "")
        try:
            base_day = time.strptime(base_day, '%Y%m%d')
            base_day = datetime.datetime(*base_day[:3])
        except:
            print r'Error: base_day must be False or %Y%m%d or %Y-%m-%d'
            raise ValueError
    else:
        base_day = datetime.datetime.now()

    oneday = datetime.timedelta(days=1)
    time_type = {
        'year': '%Y',
        'day': '%Y-%m-%d',
        'month': '%Y-%m',
        'start_day_of_month': '%Y-%m-01',
    }
    target_time = base_day + oneday*days_before
    return datetime.datetime.strftime(target_time, time_type[detail])

if __name__ == '__main__':
    print timeConfig()
    print timeConfig(days_before=1, base_day=False, detail='day')
    print timeConfig(days_before=-1, base_day=False, detail='day')
    print timeConfig(days_before=0, base_day=20160530, detail='day')
    print timeConfig(detail='year')
    print timeConfig(days_before=1, base_day=False, detail='year')
    print timeConfig(days_before=-1, base_day=False, detail='year')
    print timeConfig(days_before=300, base_day=20160530, detail='year')
    print timeConfig(20161001, -300)
    print timeConfig(days_before=1, base_day=False, detail='day')
    print timeConfig(days_before=-1, base_day='20160514', detail='day')
    print timeConfig(days_before=-300, base_day=20160530, detail='day')
    print timeConfig(days_before=-300, base_day=20160530, detail='start_day_of_month')
    print timeConfig()
    print timeConfig(days_before=1, base_day=False, detail='start_day_of_month')
    print timeConfig(days_before=-1, base_day=False, detail='start_day_of_month')
    print timeConfig(days_before=0, base_day=20160530, detail='start_day_of_month')
    print timeConfig(detail='year')
    print timeConfig(days_before=1, base_day=False, detail='year')
    print timeConfig(days_before=-1, base_day=False, detail='year')
    print timeConfig(days_before=300, base_day=20160530, detail='year')
    print timeConfig(20161001, -300)
    print timeConfig(days_before=1, base_day=False, detail='start_day_of_month')
    print timeConfig(days_before=-1, base_day='20160514', detail='start_day_of_month')
    print timeConfig(days_before=-300, base_day=20160530, detail='start_day_of_month')

