from .log import write_log

def operate_nativesql(query_sql):
    if not query_sql :
        return 'SQL为空'
    
    try :
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute(query_sql) 
        query_set = cursor.fetchall()
        return query_set
    except Exception as e :
        write_log('warning' , '', '执行SQL失败，SQL命令：' + query_sql + '原因如下：\n' + str(e))
        return '查询错误，错误内容为' + str(e)
