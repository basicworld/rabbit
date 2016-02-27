# -*- coding:utf8 -*-
"""
Class function: create time
Dont change anything
Author: wlf
Time: 20160223
"""
import datetime
import time

def timeConfig(base_day='', days_before=0, detail='day'):
    '''
    return days before base_day
    default return today, eg, 2016-02-23
    base_day should like: '20160223', '2016-02-23'
    detail: year, day, start_day_of_month, month

    # doctest
    >>> timeConfig(base_day='20160123')
    '2016-01-23'
    >>> timeConfig('20160123')
    '2016-01-23'
    >>> timeConfig(base_day='20160123')
    '2016-01-23'
    >>> timeConfig(base_day='20160123',days_before=1)
    '2016-01-24'
    >>> timeConfig(base_day='20160123',days_before=-1)
    '2016-01-22'
    >>> timeConfig(base_day='20160123',days_before=1,detail='month')
    '2016-01'
    >>> timeConfig(base_day='20160123',days_before=1,detail='year')
    '2016'
    >>> timeConfig(base_day='20160123',days_before=1,detail='month_start')
    '2016-01-01'
    >>> timeConfig(base_day='20160123',days_before=1,detail='month_start1')
    Error: `detail` must in ['month_start', 'month', 'day', 'year']
    False
    '''

    if base_day:
        # base_day = str(base_day)
        base_day = str(base_day).replace("-", "")
        try:
            base_day = time.strptime(base_day, '%Y%m%d')
            base_day = datetime.datetime(*base_day[:3])
        except:
            print r'Error: base_day must be '' or %Y%m%d or %Y-%m-%d'
            return False
    else:
        base_day = datetime.datetime.now()

    oneday = datetime.timedelta(days=1)
    time_type = {
        'year': '%Y',
        'day': '%Y-%m-%d',
        'month': '%Y-%m',
        'month_start': '%Y-%m-01',
    }
    target_time = base_day + oneday*days_before
    try:
        return datetime.datetime.strftime(target_time, time_type[detail])
    except KeyError as e:
        print "Error: `detail` must in %s" % time_type.keys()
        return False

if __name__ == '__main__':
    """
    doctest test
    """
    print "If doctest passed, this will be the only one output."
    import doctest
    doctest.testmod()
    