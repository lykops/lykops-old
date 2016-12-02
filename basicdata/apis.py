from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls.base import reverse


from library.db_page import Operate_Models
from library.log import write_log
from lykops.settings import STATIC_ROOT


class App_Operate_Models(Operate_Models):
    def list(self, request):
        if request.method == 'POST':
            # 该部分用于导入数据
            try :
                context = self.import_model(request)
                return render(request, 'result.html', {'context':context})
            except :
                return HttpResponseRedirect(reverse('list_' + self.model_name)) 
            
        if hasattr(self, 'forgkey_field_list') :
            (query_set , url_search) = self.list_sqlquery(request)
        else :
            (q, url_search) = self.list_search(request)
            if self.model_name == 'provider' :
                try :
                    query_set = self.import_models.objects.using('mysql_read').filter(q).values_list('id' , 'name' , 'tel', 'website'  , 'type' , 'customer' , 'tech').distinct()
                except:
                    query_set = self.import_models.objects.using('mysql_read').filter().values_list('id' , 'name' , 'tel', 'website'  , 'type' , 'customer' , 'tech').distinct()
            
            if self.model_name == 'wechat_pubno' :
                try :
                    query_set = self.import_models.objects.using('mysql_read').filter(q).values_list('id' , 'name' , 'wxno', 'status'  , 'type' , 'appid' , 'start_time').distinct()
                except:
                    query_set = self.import_models.objects.using('mysql_read').filter().values_list('id' , 'name' , 'wxno', 'status'  , 'type' , 'appid' , 'start_time').distinct()
            
        request_dict = self.list_display(request , query_set, url_search)
        return render(request, 'list.html', request_dict)

        
    def import_model(self , request) :
        if request.method == 'POST':
            file = request.FILES['file']
            filename = str(request.FILES['file'])

        from library.handle_file import Import_File
        from library.webpage import uploadfile
        filename = uploadfile(file, filename, STATIC_ROOT + '/upload/')
        uploaded = Import_File(file, filename)
        insertdata_list = uploaded.import2db()

        if not insertdata_list :
            write_log('warning' , self.op_user , self.model_cnname + '导入数据失败，文件为空')
            return '文件为空'

        insert_result = ''
        succ_no = 0
        fail_no = 0
        dupl_no = 0

        def get_fk_id(fk_table, id_name) :
            name = insertdict[id_name]
            if name == '' or not name :
                name_id = ''
                # 允许外键字段为空
            else :
                try :
                    name_id = fk_table.objects.using('mysql_read').filter(name=name).values_list('id').distinct()[0][0]
                except :
                    name_id = 0
                    # 允许外键字段为空
            return str(name_id)

        for insertdata in insertdata_list :
            no = insertdata_list.index(insertdata) + 1
            no = str(no)
            try : 
                insertdict = dict(zip(self.detail_field_list, insertdata))

                if hasattr(self, 'forgkey_field_list') :
                    # 这段代码用于字符转化为外键表id
                    if self.model_name in ['idc', 'bandwidth', 'hardware' , 'software', 'third_service'] :
                        from .models import Provider as fk_table
                        id_name = 'provider_id'
                        insertdict[id_name] = get_fk_id(fk_table, id_name)
    
                    if self.model_name in [ 'hardware_brand', 'software_type', 'third_service']:
                        from .models import Provider as fk_table
                        id_name = 'manufacturer_id'
                        insertdict[id_name] = get_fk_id(fk_table, id_name)
    
                    if self.model_name in ['rack' , 'ip_segment', 'bandwidth'] :
                        from .models import Idc as fk_table
                        id_name = 'idc_id'
                        insertdict[id_name] = get_fk_id(fk_table, id_name)
    
                    if self.model_name in [ 'position'  , 'person']:
                        from .models import Department as fk_table
                        id_name = 'department_id'
                        insertdict[id_name] = get_fk_id(fk_table, id_name)
    
                    if self.model_name in [ 'ip_segment']:
                        from .models import Bandwidth as fk_table
                        id_name = 'bandwidth_id'
                        insertdict[id_name] = get_fk_id(fk_table, id_name)
    
                    if self.model_name in [ 'domain']:
                        from .models import Provider as fk_table
                        for id_name in ['provider_id', 'dns_provider_id', 'icp_provider_id'] :
                            insertdict[id_name] = get_fk_id(fk_table, id_name)
                            
                    if self.model_name in ['hardware']:
                        from .models import Hardware_Brand as fk_table
                        id_name = 'type_id'
                        insertdict[id_name] = get_fk_id(fk_table, id_name)
    
                    if self.model_name in ['software']:
                        from .models import Software_Type as fk_table
                        id_name = 'type_id'
                        insertdict[id_name] = get_fk_id(fk_table, id_name)
    
                    if self.model_name in [ 'person']:
                        from .models import Person as fk_table
                        id_name = 'leaders_id'
                        insertdict[id_name] = get_fk_id(fk_table, id_name)
    
                        from .models import Position as fk_table
                        id_name = 'position_id'
                        insertdict[id_name] = get_fk_id(fk_table, id_name)
                        
                    if self.model_name in [ 'department']:
                        from .models import Department as fk_table
                        id_name = 'supervising_authority_id'
                        insertdict[id_name] = get_fk_id(fk_table, id_name)
    
                    if self.model_name in [ 'business_system']:
                        from .models import Person as fk_table
                        for id_name in ['project_manager_id' , 'developer_manager_id' , 'test_manager_id' , 'operate_manager_id'] :
                            insertdict[id_name] = get_fk_id(fk_table, id_name)
                        
                        from .models import Business_System as fk_table_1
                        id_name = 'belong2project_id'  
                        insertdict[id_name] = get_fk_id(fk_table_1, id_name)
                        
                self.import_models.objects.create(**insertdict)
                # insert_result = insert_result + '<div class="alert alert-success text-center">第' + no + "行：导入成功</div></br>"
                succ_no += 1
            except Exception as e :
                write_log('warning' , self.op_user, self.model_cnname + '导入数据失败 ' + str(insertdata) + ' ' + str(e))
                if 'Duplicate entry' in str(e) :
                    # insert_result = insert_result + '<div class="alert alert-danger text-center">第' + no + "行：插入数据重复</div>"
                    dupl_no += 1
                    fail_no += 1
                else :
                    insert_result = insert_result + '<div class="alert alert-danger text-center">第' + no + "行：插入数据失败" + str(e) + "</div>"
                    fail_no += 1
        
        insert_result = insert_result + '</br>' + '<div class="alert alert-danger text-center">失败数为' + str(fail_no) + '</div>' + '<div class="alert alert-danger text-center">其中重复数为' + str(dupl_no) + '</div><div class="alert alert-success text-center">成功数为' + str(succ_no) + '</div>'
        return insert_result
