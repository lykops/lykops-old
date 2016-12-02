import time, os, sys, re
from lykops.settings import BASE_DIR, DEBUG

def write_log(log_level , op_user , message):        
    '''
        log_level : 日志级别
        op_user : 操作者
        message : 日志内容
    '''
    if not message :
        return 'no message'

    if not op_user :
        op_user = 'system'

    error_level_list = ('debug' , 'info' , 'warning' , 'error')

    if log_level in error_level_list[2:] :
        log_file = 'error.log'
    elif log_level in error_level_list[:2] :
        log_file = 'info.log'
        #if DEBUG == False  and log_level == 'debug':
        #    print('NO')
        #    return 'NO'
            # 如果没有开启debug，将不记录info和debug日志
    else :
        log_level = 'unknown'
        log_file = 'info.log'
        
    curl_time = time.strftime('%Y年%m月%d日%H:%M:%S' , time.localtime())
    log_dir = BASE_DIR + '/logs/'
    if not os.path.exists(log_dir) :
        os.mkdir(log_dir)
            
    if not re.search('.log$' , log_file) :
        log_file = log_dir + log_file + '.log'
    else :
        log_file = log_dir + log_file
        
    import traceback
    caller_list = traceback.extract_stack()
    caller_str = ''
    for caller in caller_list[:-1] :
        if BASE_DIR in caller[0] :
            caller_file = caller[0].replace(BASE_DIR + '/' , '')
            caller_fun = caller[2]
            if caller_str :
                caller_str = caller_str + '=>' + caller_file + ':' + caller_fun
            else:
                caller_str = caller_file + ':' + caller_fun
                
    message = curl_time + '    [' + log_level + ']    [' + op_user + ']    [' + caller_str + ']    ' + message + '\n'
    
    try :
        open_logfile = open(log_file , 'a')
        open_logfile.writelines(message)
        open_logfile.close
        return 'OK'
    except Exception as e:
        print(str(e))
        return 'NG'
