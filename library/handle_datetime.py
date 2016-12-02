import time , datetime , re

from library.log import write_log

def time2stamp(timestr):
    # 时间转化为时间戳
    try :
        (convert_after, old_format) = time2format(timestr)
    except :
        return timestr
    
    try :
        strptimes = time.strptime(convert_after, old_format)
    except Exception as e :
        write_log('warning' , '', '时间转化元组失败' + convert_after + '  ' + str(e))
        return timestr
    
    '''
    if len(timestr) <= 10 :
        timestr = timestr + ' 00:00:00'
    
    if '-' in timestr:
        try :
            strptimes = time.strptime(timestr, '%Y-%m-%d %H:%M:%S')
        except Exception as e :
            write_log('warning' , '', '时间转化失败' + timestr + '  ' + str(e))
            return 'Error:' + e
    
    if '/' in timestr :
        try :
            strptimes = time.strptime(timestr, '%Y/%m/%d %H:%M:%S')
        except Exception as e :
            write_log('warning' , '', '时间转化失败' + timestr + '  ' + str(e))
            return 'Error:' + e
    '''
    
    try :
        return time.mktime(strptimes)
    except Exception as e :
        write_log('warning' , '', '时间元组转化时间戳失败' + convert_after + '  ' + str(e))
        return timestr


def stamp2time(stamp , newformat):
    # 时间戳转化新的时间格式
    try :
        strptimes = time.localtime(stamp)
        return time.strftime(newformat , strptimes)
    except Exception as e :
        write_log('warning' , '', '时间戳转化时间失败' + stamp + '  ' + newformat + ' ' + str(e))
        return stamp


def time2format(timestr):
    # 提供时间字符转化为固定格式时间格式
    full_year = '^[0-9]{4}'
    full_month = '[0-9]{2}'
    full_date = '[0-9]{2}'
    date_line = full_year + '-' + full_month + '-' + full_date
    date_backslash = full_year + '/' + full_month + '/' + full_date
    date_hanzi = full_year + '年' + full_month + '月' + full_date + '日'
    full_time = ' [0-9]{2}:[0-9]{2}:[0-9]{2}'
    
    if re.search(date_line, timestr) :
        date = date_line
    elif re.search(date_backslash, timestr) :
        date = date_backslash
    elif re.search(date_hanzi, timestr) :
        date = date_hanzi
    else :
        return timestr
        
    if re.search(date + '$' , timestr) :
        convert_after = timestr + ' 00:00:00'
    elif re.search(date + full_time + '$' , timestr) :
        convert_after = timestr
    elif re.search(date + full_time + '.[0-9]{1,6}$', timestr) :
        convert_after = re.split('\.' , timestr)[0] 
    elif re.search(date + full_time + '.[0-9]{1,6}+[0-9][0-9]:[0-9][0-9]$', timestr) :
        convert_after = re.split('\.' , timestr)[0] 
    
    if re.search(date_line, timestr) :
        old_format = '%Y-%m-%d %H:%M:%S'
    elif re.search(date_backslash, timestr) :
        old_format = '%Y/%m/%d %H:%M:%S'
    elif re.search(date_hanzi, timestr) :
        old_format = '%Y年%m月%d日 %H:%M:%S'
    
    return (convert_after, old_format)


def date_convert(timestr , newformat):
    # 时间字符转化为新时间格式
    try :
        stamp = time2stamp(timestr)
        newvalue = stamp2time(stamp, newformat)
        return newvalue
    except Exception as e :
        write_log('warning' , '', '时间转化失败' + stamp + '  ' + newformat + '  ' + str(e))
        return timestr
