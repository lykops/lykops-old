import  re

from django.db.models import Q
from django.forms.forms import Form
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls.base import reverse

from lykops.settings import STATIC_ROOT, BASE_DIR, MEDIA_ROOT

from .database import operate_nativesql
from .log import write_log

class Operate_Models():
    def add(self, request):
        title_name = "新增" + self.model_cnname + "信息："
        if request.method == 'POST':
            post_form = self.import_forms(request.POST, request.FILES)
            if post_form.is_valid():
                # 这段代码完全是为了处理字段类型为filefiled，如果不需要使用filefiled的话，直接post_form.save()
                new_value = {}
                media_dir = MEDIA_ROOT.replace(BASE_DIR + '/', '')
                for key in self.detail_field_list :
                    post_key = key.replace('_id' , '')
                    # 对于外键来说，字段名是以_id结尾的，但forms提交是不带_id的，需要根据外键表的名字查找外键表的ID，然后判断和数据库是否一致，如果一致不修改。让request.POST字典的key和detail_field_list相同，让新字典的key值等于post的post_key相等
                    
                    if hasattr(self, 'filefield_dict') and key in self.filefield_dict :
                        # 处理filefield
                        filename = key + '_' + str(request.FILES[key])
                        # 文件名，字段名+上传文件名
                        file = request.FILES[key]
                        upload_dir = MEDIA_ROOT + '/upload/' + self.app_name + '/' + self.model_name + '/' + request.POST.get('name') + '/'
                        # 上传目录，MEDIA_ROOT/upload/app名/modles名/字段name的值/
                                
                        from .webpage import uploadfile
                        fullfilename = uploadfile(file, filename, upload_dir)
                        # 最终目录为MEDIA_ROOT.replace(BASE_DIR,'')/upload/app名/modles名/字段name的值/字段名_上传文件名，防止出现重复替换操作
                        value = media_dir + '/upload/' + self.app_name + '/' + self.model_name + '/' + request.POST.get('name') + '/' + filename
                        # 数据库中写相对路径
                    else :
                        value = request.POST.get(post_key)
                        value_str = str(value)
                    
                        # 日期转换
                        if re.search('^[0-9][0-9][0-9][0-9]/[0-1][0-9]', value_str) :
                            from .handle_datetime import date_convert
                            value = date_convert(value_str , '%Y-%m-%d')
                        
                        new_value[key] = value
    
                try :
                    self.import_models.objects.create(**new_value)
                except Exception as e :
                    write_log('warning' , self.op_user, self.model_cnname + '新增数据失败，' + str(new_value) + '，原因如下：\n' + str(e))
                    
                # post_form.save()
                return HttpResponseRedirect(reverse('list_' + self.model_name))
            else :
                errors_message = post_form.errors
                write_log('warning' , self.op_user, self.model_cnname + '新增失败' + str(post_form) + '，原因如下：\n' + str(errors_message))
                return render(request, 'result.html', {'error_message': str(errors_message)})
        else :
            get_form = self.import_forms()
            request_dict = {'title_name' : title_name , 'get_form': get_form} 
            return render(request, 'add_edit.html', request_dict)


    def detail(self, request):
        request_dict = {}
        detail_id = request.GET.get('id')
        
        if hasattr(self, 'forgkey_field_list') :
            query_sql = self.detail_basic_querysql + 'where ' + self.model_name + '.id=' + detail_id
            query_set = operate_nativesql(query_sql)[0]
        else :
            try :
                query_set = self.import_models.objects.using('mysql_read').filter(id=detail_id).values_list().distinct()
                query_set = query_set[0]
            except Exception as e:
                write_log('warning' , self.op_user, self.model_cnname + '查看详细数据失败 ' + detail_id + '不存在或者其他原因' + str(e))
                return HttpResponseRedirect(reverse('list_' + self.model_name))
        
        request_dict['title_name'] = self.model_cnname + '【' + query_set[1] + '】详细信息：'
        http_referer = request.META.get('HTTP_REFERER')
        if not http_referer :
            http_referer = reverse('list_' + self.model_name)
        
        query_set = list(zip(self.detail_title_list, query_set[1:]))
        request_dict['url_front'] = self.app_basedir + self.model_name
        request_dict['id'] = detail_id
        request_dict['http_referer'] = http_referer
        
        request_dict['query_set'] = query_set
        return render(request, 'detail.html', request_dict)


    def list_sqlquery(self , request):
        # 这里是处理外键表的展示页面【使用原生SQL查询】
        try :
            if hasattr(self.import_models, 'name') :
                sql_where = 'WHERE 1=1 AND ' + self.model_name + '.name NOT LIKE \"  %  %  \" '
            else :
                sql_where = 'WHERE 1=1 '
            
            url_search = ''
            try :
                if 'type' in request.GET :
                    if request.GET.get('type'):
                        search_type = request.GET.get('type')
                        sql_where = sql_where + ' AND ' + self.model_name + '.type = \"' + search_type + '\"'
                            
                        if url_search != '' :
                            url_search = url_search + 'type=' + search_type
                        else :
                            url_search = 'type=' + search_type
            except :
                pass
                
            # 使用状态没有选择时，不显示到期，只有在到期时，才显示
            try :
                if 'status' in request.GET :
                    if request.GET.get('status'):
                        search_status = request.GET.get('status')
                        sql_where = sql_where + ' AND ' + self.model_name + '.status = \"' + search_status + '\"'
                                
                        if url_search != '' :
                            url_search = url_search + 'status=' + search_status
                        else :
                            url_search = 'status=' + search_status
                    else :
                        if hasattr(self, 'status_list') and self.status_list != [] :
                            sql_where = sql_where + ' AND ' + self.model_name + '.status NOT LIKE \'%到期%\''
                else :
                    # 如果没有status这个字段，where中不含status查询
                    if hasattr(self, 'status_list') and self.status_list != [] :
                        sql_where = sql_where + ' AND ' + self.model_name + '.status NOT LIKE \'%到期%\''
            except :
                # 如果没有status这个字段，where中不含status查询
                if hasattr(self, 'status_list') and self.status_list != [] :
                    sql_where = sql_where + ' AND ' + self.model_name + '.status NOT LIKE \'%到期%\''
                    
            try :
                if 'keyword' in request.GET  :
                    if request.GET.get('keyword'):
                        search_keyword = request.GET.get('keyword')
                        sql_where = sql_where + ' AND ' + self.model_name + '.name LIKE \"%' + search_keyword + '%\"'
                                
                        if url_search != '' :
                            url_search = url_search + 'keyword=' + search_keyword
                        else :
                            url_search = 'keyword=' + search_keyword
            except :
                pass
            
            query_sql = self.list_basic_querysql + sql_where
        except :
            query_sql = self.list_basic_querysql
            url_search = ''
    
        query_set = operate_nativesql(query_sql)
        # 结果为((1, '广东省', (3, '富国'), (4, '广市'))
        return (query_set , url_search)
        
        
    def list_display(self, request , query_set, url_search):
        from library.webpage import paginator_options
        title_name = self.model_cnname + '列表：'
        request_dict = paginator_options(request , query_set)
        request_dict['list_title_list'] = self.list_title_list
        request_dict['title_name'] = title_name
        if hasattr(self, 'status_list') :
            request_dict['status_list'] = self.status_list
            
        if hasattr(self, 'type_list') :
            request_dict['type_list'] = self.type_list
            
        request_dict['url_search'] = url_search
        request_dict['url_front'] = self.app_basedir + self.model_name
        
        return request_dict


    def list_search(self, request):
        # 这部分用于展示页面的搜索页面展示
        try :
            q = ''
            url_search = ''
            try :
                if 'type' in request.GET :
                    if request.GET.get('type'):
                        search_type = request.GET.get('type')
                        if q != '' :
                            q = q & Q(type__contains=search_type)
                        else :
                            q = Q(type__contains=search_type)
                            
                        if url_search != '' :
                            url_search = url_search + 'type=' + search_type
                        else :
                            url_search = 'type=' + search_type
            except :
                pass
                
            try :
                if 'status' in request.GET :
                    if request.GET.get('status'):
                        search_status = request.GET.get('status')
                        if q != '' :
                            q = q & Q(status__contains=search_status)
                        else :
                            q = Q(status__contains=search_status)
                                
                        if url_search != '' :
                            url_search = url_search + 'status=' + search_status
                        else :
                            url_search = 'status=' + search_status
            except :
                pass
                        
            try :
                if 'keyword' in request.GET  :
                    if request.GET.get('keyword'):
                        search_keyword = request.GET.get('keyword')
                        if q != '' :
                            q = q & Q(name__contains=search_keyword)
                        else :
                            q = Q(name__contains=search_keyword)
                                
                        if url_search != '' :
                            url_search = url_search + 'keyword=' + search_keyword
                        else :
                            url_search = 'keyword=' + search_keyword
            except :
                pass
        except :
            q = ''
            url_search = ''

        return (q , url_search)


    def edit(self, request):
        edit_id = request.GET.get('id')
        query_set = self.import_models.objects.select_related().using('mysql_read').filter(id=edit_id).values().distinct()
        query_set = list(query_set)[0]
        
        if request.method == 'GET':
            url_front = self.app_basedir + self.model_name
            title_name = '编辑' + self.model_cnname + '【' + query_set['name'] + '】信息：'

            try :
                instance = self.import_models.objects.select_related().using('mysql_read').get(id=edit_id)
                get_form = self.import_forms(instance=instance)
                request_dict = {'title_name' : title_name , 'get_form': get_form , 'url_front' : url_front}
                return render(request, 'add_edit.html', request_dict)
            except Exception as e :
                write_log('warning' , self.op_user , self.model_cnname + '编辑:' + str(edit_id) + '失败' + str(e))
                return HttpResponseRedirect(reverse('list_' + self.model_name))
    
        if request.method == 'POST':
            new_value = {}
            
            media_dir = MEDIA_ROOT.replace(BASE_DIR + '/', '')
            
            for key in self.detail_field_list :
                post_key = key.replace('_id' , '')
                query_value = query_set[key]
                query_value = str(query_value)
                if not query_value :
                    query_value = ''
                
                if hasattr(self, 'filefield_dict') and key in self.filefield_dict :
                    # 这个if的内容主要处理文件上传，即字段类型为filefiled的。
                    try :
                        # 使用try是因为在编辑时，不上传图片，导致报错
                        filename = key + '_' + str(request.FILES[key])
                        # 文件名，字段名+上传文件名
                        file = request.FILES[key]
                        upload_dir = MEDIA_ROOT + '/upload/' + self.app_name + '/' + self.model_name + '/' + request.POST.get('name') + '/'
                        # 上传目录，MEDIA_ROOT/upload/app名/modles名/字段name的值/
                                    
                        from library.webpage import uploadfile
                        fullfilename = uploadfile(file, filename, upload_dir)
                        # 最终目录为MEDIA_ROOT.replace(BASE_DIR,'')/upload/app名/modles名/字段name的值/字段名_上传文件名，防止出现重复替换操作
                        new_value[key] = media_dir + '/upload/' + self.app_name + '/' + self.model_name + '/' + request.POST.get('name') + '/' + filename
                        # 数据库中写相对路径
                    except :
                        # 如果没有上传文件，把新值等于数据库中的值
                        new_value[key] = query_value
                elif hasattr(self, 'deny_edit_list') and key in self.deny_edit_list : 
                    # 属于禁止修改的字段，不允许修改
                    pass
                elif hasattr(self, 'forgkey_field_list') and post_key in self.forgkey_field_list :
                    # 对于外键来说，数据库中的字段名是以_id结尾的，但forms提交是不带_id的，需要根据外键表的名字查找外键表的ID，然后判断和数据库是否一致，如果一致不修改
                    post_value = request.POST.get(post_key)

                    if query_value != str(post_value) :
                        if post_value == '' :
                            new_value[key] = ''
                        else :
                            new_value[key] = int(post_value)
                else :
                    value = request.POST.get(key)
                    value_str = str(value)

                    if re.search('^[0-9][0-9][0-9][0-9]/[0-1][0-9]', value_str) :
                        from library.handle_datetime import date_convert
                        value = date_convert(value_str , '%Y-%m-%d')
                        
                    if query_value != str(value):
                        new_value[key] = value

            if new_value :
                try :
                    self.import_models.objects.filter(id=edit_id).update(**new_value)
                except Exception as e :
                    write_log('warning' , self.op_user, self.model_cnname + '修改ID:' + edit_id + '失败，' + str(new_value) + '，原因如下：\n' + str(e))
            else :
                write_log('debug' , self.op_user , self.model_cnname + '无需修改ID:' + edit_id + '，数据没有更新')

            return HttpResponseRedirect(reverse('list_' + self.model_name))


    def export(self, request):
        # '导出完成90% ,  根据搜索条件等进行导出，office2016电脑无法打开文件，报内存不足或者空间不够，需要先保存，然后右击属性，解除锁定；在2016年12月1日的更新解决该问题，如果有上述问题，更新office'
        if hasattr(self, 'forgkey_field_list') :
            query_sql = self.detail_basic_querysql
            query_set = operate_nativesql(query_sql)
        else :
            query_set = self.import_models.objects.using('mysql_read').values_list().distinct()
            query_set = list(query_set)
        
        from library.webpage import Export_File_Html
        export_file = Export_File_Html(self.model_name , self.detail_title_list, query_set)
        return export_file.xls(request)

