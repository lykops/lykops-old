from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .apis import App_Operate_Models


global App_Name , App_Basedir
App_Name = 'basicdata'
App_Basedir = '/' + App_Name + '/'


'''
下面的函数实现的功能类似于：
def add_provider(request):
    from .forms import Forms_Provider
    if request.method == 'POST':
        post_form = Forms_Provider(request.POST)
        if post_form.is_valid():
            post_form.save()
            return HttpResponseRedirect(reverse('list_provider'))
        else :
            errors_message = post_form.errors
            return render(request, 'result.html', {'context': errors_message})
    else :
        get_form = Forms_Provider()
        return render(request, 'add_provider.html', {'get_form': get_form})

def list_provider(request):
    from .models import Provider
    query_set = Provider.objects.using('mysql_read').values_list('id' , 'short_name' , 'tel_no', 'website' , 'customer' , 'customer_tel' , 'support' , 'support_tel').distinct()
    return_list = Paginator_Options(request , query_set)
    return render(request, 'list_provider.html', return_list)

def detail_provider(request):
    from .models import Provider
    provider_id = request.GET.get('providerid')
    query_set = Provider.objects.using('mysql_read').filter(id=provider_id).values_list().distinct()
    query_set = query_set[0][1:]
    field_cnname_list = ['简称' , '全称' , '地址' , '网址' , '电话' , '姓名' , '电话' , '邮箱' , '微信' , 'QQ' , '姓名' , '电话' , '邮箱' , '微信' , 'QQ' , '姓名' , '电话' , '邮箱' , '微信' , 'QQ'  , '描述' ]
    # 表列名
    title_name = query_set[1]
    # 标题名
    http_referer = request.META.get('HTTP_REFERER')
    
    result_list = list(zip(field_cnname_list , query_set))
    
    return render(request, 'detail_provider.html', {'title_name' : title_name , 'result_list' : result_list, 'http_referer':http_referer , 'provider_id' : provider_id})

def edit_provider(request):
    from .models import Provider
    field_list_list = [['short_name' , 'full_name' , 'location' , 'website' , 'tel_no'] , ['salesman' , 'salesman_tel' , 'salesman_mail' , 'salesman_wx' , 'salesman_qq'] , ['customer' , 'customer_tel' , 'customer_mail' , 'customer_wx' , 'customer_qq'] , ['support' , 'support_tel' , 'support_mail' , 'support_wx' , 'support_qq'] , ['description']]
    cnname_list_list = [['简称' , '全称' , '地址' , '网址' , '电话'] , ['姓名' , '电话' , '邮箱' , '微信' , 'QQ' ], ['姓名' , '电话' , '邮箱' , '微信' , 'QQ'] , ['姓名' , '电话' , '邮箱' , '微信' , 'QQ' ] , ['描述']]
    deny_edit_list = ['short_name' , 'full_name']
    provider_id = request.GET.get('providerid')
    
    field_name_list = []
    for field_list in field_list_list :
        if type(field_list) != type('aa') :
            for key in field_list :
                field_name_list.append(key)
        else :
            field_name_list.append(field_list)
            
    field_cnname_list = []
    for cnname_list in cnname_list_list :
        if type(cnname_list) != type('aa') :
            for key in cnname_list :
                field_cnname_list.append(key)
        else :
            field_cnname_list.append(cnname_list)
            
    field_name_dict = dict(zip(field_name_list, field_cnname_list))
    
    
    if request.method == 'POST':
        new_value = {}
        for key in field_name_list :
            new_value[key] = request.POST.get(key)
            
        Provider.objects.filter(id=provider_id).update(**new_value)
        return HttpResponseRedirect(reverse('list_provider'))
    else :
        query_set = Provider.objects.using('mysql_read').filter(id=provider_id).values().distinct()
        query_set = list(query_set)[0]
        title_name = query_set['full_name']
        # 标题名
        http_referer = request.META.get('HTTP_REFERER')
        return render(request, 'edit_provider.html', {'title_name' : title_name , 'field_list_list' :field_list_list , 'field_name_dict' : field_name_dict , 'query_set' : query_set , 'http_referer':http_referer, 'deny_edit_list' : deny_edit_list})
'''


class Provider(App_Operate_Models):
    def __init__(self):
        from .forms import Forms_Provider as import_forms
        from .models import Provider as import_models
        self.import_forms = import_forms
        self.import_models = import_models
        self.model_cnname = '服务供应商'
        self.model_name = 'provider'
        self.detail_title_list = ['简称' , '全称' , '类型' , '官方联系方式' , '地址' , '网址' , '销售联系方式' , '客服联系方式' , '技术联系方式' , '描述']
        # 详细页面、导出的中文标题，该文件中下同
        self.list_title_list = ['ID' , '简称' , '联系方式' , '网址' , '类型' , '客服联系方式' , '技术联系方式' , '操作']
        # 列表页面的中文标题，该文件中下同
        self.deny_edit_list = ['name' , 'full_name']
        # 编辑时拒绝修改的字段，该文件中下同
        self.detail_field_list = ['name' , 'full_name' , 'type' , 'tel', 'location' , 'website'  , 'salesman' , 'customer'  , 'tech' , 'description']
        # 展示详细页面、导出的字段名，该文件中下同
        self.type_list = ['' , '服务供应商'  , '电信运营商', '机房供应商', '硬软件供应商', '硬件制造商' , '软件开发商']
        # 用于列表展示页面上方，type字段（中文名为类型）搜索选择，如果为空，直接不显示搜索，该文件中下同
        self.app_name = App_Name
        # 本app名，用于记日志
        self.app_basedir = App_Basedir
        # 本app目录，用于记日志
        self.op_user = ''
        # 操作员

class Idc(App_Operate_Models):
    def __init__(self):
        from .forms import Forms_Idc as import_forms
        from .models import Idc as import_models
        self.import_forms = import_forms
        self.import_models = import_models
        self.model_cnname = '机房'
        self.model_name = 'idc'
        self.status_list = ['' , '使用中' , '到期']
        self.type_list = ['' , '公有云' , '自建' , '托管']
        self.list_title_list = ['id' , '名称' , '类型' , '使用状态' , '供应商' , '值班电话' , '机房地址', '描述' , '操作']
        self.detail_title_list = ['名称' , '类型' , '使用状态' , '供应商' , '值班电话' , '机房地址', '描述']
        self.forgkey_field_list = ['provider'] 
        self.detail_field_list = ['name', 'type', 'status', 'provider_id', 'tel', 'location', 'description']
        self.detail_basic_querysql = '''
            SELECT
                idc.id,
                idc.name,
                idc.type,
                idc.status,
                provider.name,
                idc.tel,
                idc.location,
                idc.description
            FROM
                lykops.basicdata_idc AS idc
            LEFT JOIN lykops.basicdata_provider AS provider ON provider_id = provider.id
        '''
        
        self.list_basic_querysql = self.detail_basic_querysql
        self.app_name = App_Name
        self.app_basedir = App_Basedir
        self.op_user = ''


class Rack(App_Operate_Models):
    def __init__(self):
        from .forms import Forms_Rack as import_forms
        from .models import Rack as import_models
        self.import_forms = import_forms
        self.import_models = import_models
        self.model_cnname = '机柜'
        self.model_name = 'rack'
        self.status_list = ['' , '使用中' , '到期' , '空闲']
        self.list_title_list = ['id', '名称' , '使用状态' , '归属机房' , '使用时间' , '到期时间', '操作']
        self.detail_title_list = ['名称' , '使用状态' , '归属机房' , '编号' , '使用时间', '到期时间' , '价格'  , '最大电流（A）' , '最大设备数', '描述' ]
        self.forgkey_field_list = ['idc'] 
        self.detail_field_list = ['name', 'status' , 'idc_id', 'fixed_no', 'start_time', 'expired_time', 'price' , 'max_power' , 'max_device' , 'description']
        self.list_basic_querysql = '''
            SELECT
                rack.id,
                rack.name,
                rack.status,
                idc.name,
                rack.start_time,
                rack.expired_time
            FROM
                lykops.basicdata_rack AS rack
            LEFT JOIN lykops.basicdata_idc AS idc ON idc_id = idc.id
        '''
        
        self.detail_basic_querysql = '''
            SELECT
                rack.id ,
                rack.name,
                rack.status,
                idc.name,
                rack.fixed_no,
                rack.start_time,
                rack.expired_time,
                rack.price,
                rack.max_power,
                rack.max_device,
                rack.description
            FROM
                lykops.basicdata_rack AS rack
            LEFT JOIN lykops.basicdata_idc AS idc ON idc_id = idc.id
        '''
        
        self.app_name = App_Name
        self.app_basedir = App_Basedir
        self.op_user = ''
        

class Bandwidth(App_Operate_Models):
    def __init__(self):
        from .forms import Forms_Bandwidth as import_forms
        from .models import Bandwidth as import_models
        
        self.import_forms = import_forms
        self.import_models = import_models
        self.model_cnname = '带宽'
        self.model_name = 'bandwidth'
        self.type_list = [ '' , '单线' , '多线多IP' , '双线BGP', '三线BGP' , '多线BGP' , '专线' , 'E1线路']
        self.status_list = ['' , '使用中' , '暂停使用', '到期']
        self.forgkey_field_list = ['idc' , 'provider'] 
        self.list_title_list = ['id', '名称' , '类型' , '使用状态', '供应商' , '归属机房', '到期时间', '带宽（M）' , '操作']
        self.detail_title_list = ['名称' , '类型' , '使用状态' , '供应商' , '归属机房', '开通时间' , '到期时间', '价格（元/月）', '带宽（M）' , '装机地点', '描述']
        
        self.detail_field_list = ['name', 'type' , 'status' , 'provider_id' , 'idc_id', 'start_time', 'expired_time', 'price' , 'rate' , 'location' , 'description']
        self.list_basic_querysql = '''
            SELECT
                bandwidth.id,
                bandwidth.name,
                bandwidth.type,
                bandwidth.status,
                (
                    SELECT
                        name
                    FROM
                        lykops.basicdata_provider
                    WHERE
                        id = bandwidth.provider_id
                ) as provider_name,
                idc.name as idc_name,
                bandwidth.expired_time,
                bandwidth.rate
            FROM
                lykops.basicdata_bandwidth AS bandwidth
            LEFT JOIN lykops.basicdata_idc AS idc ON idc_id = idc.id
        '''
        
        self.detail_basic_querysql = '''
            SELECT
                bandwidth.id,
                bandwidth.name,
                bandwidth.type,
                bandwidth.status,
                (
                    SELECT
                        name
                    FROM
                        lykops.basicdata_provider
                    WHERE
                        id = bandwidth.provider_id
                ) AS provider_name,
                idc.name AS idc_name,
                bandwidth.start_time,
                bandwidth.expired_time,
                bandwidth.price,
                bandwidth.rate,
                bandwidth.location,
                bandwidth.description
            FROM
                lykops.basicdata_bandwidth AS bandwidth
            LEFT JOIN lykops.basicdata_idc AS idc ON idc_id = idc.id
        '''
        
        self.app_name = App_Name
        self.app_basedir = App_Basedir
        self.op_user = ''
        

class Ip_Segment(App_Operate_Models):
    def __init__(self):
        from .forms import Forms_Ip_Segment as import_forms
        from .models import Ip_Segment as import_models
        from .models import Idc
        self.import_forms = import_forms
        self.import_models = import_models
        self.model_cnname = '网段'
        self.model_name = 'ip_segment'
        self.status_list = ['' , '使用中' , '到期' , '空闲']
        self.list_title_list = ['id', '名称' , '使用状态' , '归属机房' , '归属带宽'  , '网段' , '操作']
        self.detail_title_list = ['名称' , '使用状态' , '类型' , '归属机房' , '归属带宽' , '网段' , '掩码' , '网关' , '价格' , '使用时间', '到期时间' , '描述' ]
        self.forgkey_field_list = ['idc', 'bandwidth'] 
        self.detail_field_list = ['name', 'status' , 'type' , 'idc_id', 'bandwidth_id' , 'net_address', 'net_mask' , 'gateway'  , 'price' , 'start_time', 'expired_time', 'description']
        self.list_basic_querysql = '''
            SELECT
                ip_segment.id,
                ip_segment.name,
                ip_segment.status,
                idc.name as idcname,
                (
                    SELECT
                        name
                    FROM
                        lykops.basicdata_bandwidth
                    WHERE
                        id = ip_segment.bandwidth_id
                ) AS bandwidth_name,
                ip_segment.net_address
            FROM
                lykops.basicdata_ip_segment AS ip_segment
            LEFT JOIN lykops.basicdata_idc AS idc ON idc_id = idc.id
        '''
        
        self.detail_basic_querysql = '''
            SELECT
                ip_segment.id,
                ip_segment.name,
                ip_segment.status,
                ip_segment.type,
                idc.name as idcname,
                (
                    SELECT
                        name
                    FROM
                        lykops.basicdata_bandwidth
                    WHERE
                        id = ip_segment.bandwidth_id
                ) AS bandwidth_name,
                ip_segment.net_address,
                ip_segment.net_mask,
                ip_segment.gateway,
                ip_segment.price,
                ip_segment.start_time,
                ip_segment.expired_time,
                ip_segment.description
            FROM
                lykops.basicdata_ip_segment AS ip_segment
            LEFT JOIN lykops.basicdata_idc AS idc ON idc_id = idc.id
        '''
        
        self.app_name = App_Name
        self.app_basedir = App_Basedir
        self.op_user = ''
        

class Domain(App_Operate_Models):
    def __init__(self):
        from .forms import Forms_Domain as import_forms
        from .models import Domain as import_models
        self.import_forms = import_forms
        self.import_models = import_models
        self.model_cnname = '域名'
        self.model_name = 'domain'
        self.status_list = ['' , '使用中' , '备案未用' , '未备案', '到期']
        self.forgkey_field_list = ['dns_provider' , 'icp_provider' , 'provider'] 
        self.list_title_list = ['id' , '名称' , '使用状态' , '域名供应商' , '域名到期时间' , 'DNS解析供应商', '解析到期时间' , '备案号' , '操作']
        self.detail_title_list = [ '名称' , '使用状态' , '域名供应商' , '域名注册时间' , '域名到期时间' , '域名价格【元/年】' , 'DNS解析供应商', '解析开始时间' , '解析到期时间' , '解析服务费用[元/年]' , '域名备案者' , '备案号' , '描述']
        self.detail_field_list = ['name', 'status', 'provider_id', 'start_time', 'expired_time', 'price' , 'dns_provider_id' , 'dns_start_time' , 'dns_expired_time' , 'dns_price' , 'icp_provider_id' , 'icp_id' , 'description']
        self.list_basic_querysql = '''
            SELECT
                domain.id,
                domain.name,
                domain.status,
                provider.name,
                domain.expired_time,
                (
                    SELECT
                        name
                    FROM
                        lykops.basicdata_provider
                    WHERE
                        id = domain.dns_provider_id
                ) AS dns_provider,
                domain.dns_expired_time,
                domain.icp_id
            FROM
                lykops.basicdata_domain AS domain
            LEFT JOIN lykops.basicdata_provider AS provider ON provider_id = provider.id
        '''
        
        self.detail_basic_querysql = '''
            SELECT
                domain.id,
                domain.name,
                domain.status,
                provider.name,
                domain.start_time,
                domain.expired_time,
                domain.price,
                (
                    SELECT
                        name
                    FROM
                        lykops.basicdata_provider
                    WHERE
                        id = domain.dns_provider_id
                ) AS dns_provider,
                domain.dns_start_time,
                domain.dns_expired_time,
                domain.dns_price,
                (
                    SELECT
                        name
                    FROM
                        lykops.basicdata_provider
                    WHERE
                        id = domain.icp_provider_id
                ) AS icp_provider,
                domain.icp_id,
                domain.description
            FROM
                lykops.basicdata_domain AS domain
            LEFT JOIN lykops.basicdata_provider AS provider ON provider_id = provider.id
        '''
        self.app_name = App_Name
        self.app_basedir = App_Basedir
        self.op_user = ''


class Third_Service(App_Operate_Models):
    def __init__(self):
        from .forms import Forms_Third_Service as import_forms
        from .models import Third_Service as import_models
        self.import_forms = import_forms
        self.import_models = import_models
        self.model_cnname = '第三方服务'
        self.model_name = 'third_service'
        self.status_list = ['' , '使用中' , '到期']
        self.type_list = ['' , 'CDN' , '云服务器' , 'RDS', '负载均衡' , '安全', '云存储' , 'AMP', '其他']
        self.forgkey_field_list = [ 'manufacturer' , 'provider'] 
        self.list_title_list = ['id' , '名称' , '类型', '使用状态' , '采购商' , '到期时间' , '操作']
        self.detail_title_list = [ '名称' , '使用状态' , '类型', '服务供应商' , '采购商' , '开通时间' , '到期时间' , '价格【元/月】' , '描述']
        self.detail_field_list = ['name', 'type', 'status', 'manufacturer_id' , 'provider_id', 'start_time', 'expired_time', 'price' , 'description']
        self.list_basic_querysql = '''
            SELECT
                third_service.id,
                third_service.name,
                third_service.type,
                third_service.status,
                provider.name,
                third_service.expired_time
            FROM
                lykops.basicdata_third_service AS third_service
            LEFT JOIN lykops.basicdata_provider AS provider ON provider_id = provider.id
        '''
        
        self.detail_basic_querysql = '''
            SELECT
                third_service.id,
                third_service.name,
                third_service.type,
                third_service.status,
                (
                    SELECT
                        name
                    FROM
                        lykops.basicdata_provider
                    WHERE
                        id = manufacturer_id
                ) AS manufacturer,
                provider.name,
                third_service.start_time,
                third_service.expired_time,
                third_service.price,
                third_service.description
            FROM
                lykops.basicdata_third_service AS third_service
            LEFT JOIN lykops.basicdata_provider AS provider ON provider_id = provider.id
        '''
        self.app_name = App_Name
        self.app_basedir = App_Basedir
        self.op_user = ''


class Wechat_Pubno(App_Operate_Models):
    def __init__(self):
        from .forms import Forms_Wechat_Pubno as import_forms
        from .models import Wechat_Pubno as import_models
        self.import_forms = import_forms
        self.import_models = import_models
        self.model_cnname = '微信公众号'
        self.model_name = 'wechat_pubno'
        self.detail_title_list = ['名称' , '微信号' , '使用状态' , '类型' , '运营者联系方式' , '管理者联系方式' , '应用id' , '应用密匙' , '原始ID' , '下次年审时间' , '最后下次年审时间' , '二维码' , 'txt文件', '描述']
        # 详细页面、导出的中文标题，该文件中下同
        self.list_title_list = ['ID' , '名称' , '微信号' , '使用状态' , '类型' , '应用id' , '下次年审时间' , '操作']
        # 列表页面的中文标题，该文件中下同
        self.deny_edit_list = ['appid' , 'orig_id']
        # 编辑时拒绝修改的字段，该文件中下同
        self.detail_field_list = ['name' , 'wxno' , 'status', 'type' , 'oper', 'manger' , 'appid'  , 'appsecret' , 'orig_id'  , 'start_time' , 'expired_time' , 'qr_code'  , 'auth_file', 'description']
        # 展示详细页面、导出的字段名，该文件中下同
        self.status_list = ['' , '使用中', '未认证' , '未年审']
        # 用于列表展示页面上方，status字段（中文名为使用状态）搜索选择，如果为空，直接不显示搜索，该文件中下同
        self.type_list = ['' , '服务号', '订阅号'  , '企业号']
        self.app_name = App_Name
        self.app_basedir = App_Basedir
        self.op_user = ''
        self.filefield_dict = ['qr_code', 'auth_file' ]
        
class Hardware_Brand(App_Operate_Models):
    def __init__(self):
        from .forms import Forms_Hardware_Brand as import_forms
        from .models import Hardware_Brand as import_models
        self.import_forms = import_forms
        self.import_models = import_models
        self.model_cnname = '硬件型号'
        self.model_name = 'hardware_brand'
        self.type_list = ['' , '服务器'  , '交换机', '路由器' , '防火墙' , '存储', 'CPU' , '硬盘' , '内存', '电源' , '其他']
        self.forgkey_field_list = [ 'manufacturer'] 
        self.list_title_list = ['id' , '品牌 型号' , '类型' , '制造商' , '使用年限' , '描述', '操作']
        self.detail_title_list = [ '品牌 型号' , '类型' , '制造商' , '使用年限' , '描述']
        self.detail_field_list = ['name', 'type', 'manufacturer_id' , 'slp', 'description']
        self.detail_basic_querysql = '''
            SELECT
                hardware_brand.id,
                hardware_brand.name,
                hardware_brand.type,
                provider.name,
                hardware_brand.slp,
                hardware_brand.description
            FROM
                lykops.basicdata_hardware_brand AS hardware_brand
            LEFT JOIN lykops.basicdata_provider AS provider ON manufacturer_id = provider.id
        '''

        self.list_basic_querysql = self.detail_basic_querysql
        self.app_name = App_Name
        self.app_basedir = App_Basedir
        self.op_user = ''


class Hardware(App_Operate_Models):
    def __init__(self):
        from .forms import Forms_Hardware as import_forms
        from .models import Hardware as import_models
        self.import_forms = import_forms
        self.import_models = import_models
        self.model_cnname = '硬件'
        self.model_name = 'hardware'
        self.status_list = ['' , '使用中', '闲置', '报废']
        
        '''
         from .models import Hardware_Brand
        query_set = Hardware_Brand.objects.using('mysql_read').filter().values_list('name').distinct()
        type_list = []
        for query in query_set :
            type_list.append(query[0])
        self.type_list = type_list
        
        
        如果按照以上的命令运行的话，需要修改SQL
        
        SELECT
            hardware.id,
            hardware. NAME,
            (
                SELECT
                    NAME
                FROM
                    lykops.basicdata_hardware_brand
                WHERE
                    id = hardware.type_id
            ) AS type,
            hardware. STATUS,
            hardware.start_time,
            hardware.sn,
            hardware.fixed_no
        FROM
            lykops.basicdata_hardware AS hardware
        LEFT JOIN lykops.basicdata_provider AS provider ON provider_id = provider.id
        WHERE
            1 = 1
        AND type = "Dell R730"
        AND hardware. STATUS NOT LIKE '%到期%'
        
        '''
        
        self.forgkey_field_list = [ 'provider', 'type'] 
        self.list_title_list = ['id' , '名称', '型号' , '状态' , '购买时间'  , 'SN' , '固定资产编号' , '操作']
        self.detail_title_list = ['名称', '型号' , '状态' , '供应商' , '购买时间' , '报废时间', '采购价' , 'SN' , 'PN', '固定资产编号', '描述']
        self.detail_field_list = ['name', 'type_id', 'status' , 'provider_id' , 'start_time', 'expired_time', 'price', 'sn', 'pn', 'fixed_no', 'description']
        self.list_basic_querysql = '''
            SELECT
                hardware.id,
                hardware.name,
                (
                    SELECT
                        name
                    FROM
                        lykops.basicdata_hardware_brand
                    WHERE
                        id = hardware.type_id
                ) AS type,
                hardware.status,
                hardware.start_time,
                hardware.sn,
                hardware.fixed_no
            FROM
                lykops.basicdata_hardware AS hardware
            LEFT JOIN lykops.basicdata_provider AS provider ON provider_id = provider.id
        '''
        
        self.detail_basic_querysql = '''
            SELECT
                hardware.id,
                hardware.name,
                (
                    SELECT
                        name
                    FROM
                        lykops.basicdata_hardware_brand
                    WHERE
                        id = hardware.type_id
                ) AS type,
                hardware.status,
                provider.name,
                hardware.start_time,
                hardware.expired_time,
                hardware.price,
                hardware.sn,
                hardware.pn,
                hardware.fixed_no,
                hardware.description
            FROM
                lykops.basicdata_hardware AS hardware
            LEFT JOIN lykops.basicdata_provider AS provider ON provider_id = provider.id
        '''
        self.app_name = App_Name
        self.app_basedir = App_Basedir
        self.op_user = ''
        

class Software_Type(App_Operate_Models):
    def __init__(self):
        from .forms import Forms_Software_Type as import_forms
        from .models import Software_Type as import_models
        self.import_forms = import_forms
        self.import_models = import_models
        self.model_cnname = '软件类型'
        self.model_name = 'software_type'
        self.type_list = [ '操作系统' , '前端' , '应用软件', '中间件' , '数据库' , 'NoSQL', '存储' , '办公软件', '其他软件']
        self.forgkey_field_list = [ 'manufacturer'] 
        self.list_title_list = ['id' , '品牌 型号' , '类型' , '制造商'  , '描述', '操作']
        self.detail_title_list = ['品牌 型号' , '类型' , '制造商'  , '描述']
        self.detail_field_list = ['name', 'type', 'manufacturer_id' , 'description']
        self.detail_basic_querysql = '''
            SELECT
                software_type.id,
                software_type.name,
                software_type.type,
                provider.name,
                software_type.description
            FROM
                lykops.basicdata_software_type AS software_type
            LEFT JOIN lykops.basicdata_provider AS provider ON manufacturer_id = provider.id
        '''
        
        self.list_basic_querysql = self.detail_basic_querysql
        self.app_name = App_Name
        self.app_basedir = App_Basedir
        self.op_user = ''
        
        
class Software(App_Operate_Models):
    def __init__(self):
        from .forms import Forms_Software as import_forms
        from .models import Software as import_models
        self.import_forms = import_forms
        self.import_models = import_models
        self.model_cnname = '软件'
        self.model_name = 'software'
        self.status_list = ['' , '使用中', '许可到期']
        # from .models import Software_Type
        # self.type_list = Software_Type.objects.using('mysql_read').filter().values_list('name').distinct()
        self.forgkey_field_list = [ 'provider', 'type'] 
        self.list_title_list = ['id' , '名称', '型号' , '状态' , 'SN', '到期时间', '操作']
        self.detail_title_list = ['名称', '型号' , '状态' , '供应商' , '序列号' , '购买时间' , '采购价' , '每年成本', '许可到期时间', '描述', ]
        self.detail_field_list = ['name', 'type_id', 'status' , 'provider_id' , 'sn', 'start_time', 'price', 'cost', 'snend_time', 'description']
        self.list_basic_querysql = '''
            SELECT
                software.id,
                software.name,
                (
                    SELECT
                        name
                    FROM
                        lykops.basicdata_software_type
                    WHERE
                        id = software.type_id
                ) AS software_type,
                software.status,
                software.sn,
                software.snend_time
            FROM
                lykops.basicdata_software AS software
            LEFT JOIN lykops.basicdata_provider AS provider ON provider_id = provider.id
        '''
        
        self.detail_basic_querysql = '''
            SELECT
                software.id,
                software.name,
                (
                    SELECT
                        name
                    FROM
                        lykops.basicdata_software_type
                    WHERE
                        id = software.type_id
                ) AS software_type,
                software.status,
                provider.name,
                software.sn,
                software.start_time,
                software.price,
                software.cost,
                software.snend_time,
                software.description
            FROM
                lykops.basicdata_software AS software
            LEFT JOIN lykops.basicdata_provider AS provider ON provider_id = provider.id
        '''
        self.app_name = App_Name
        self.app_basedir = App_Basedir
        self.op_user = ''
        

class Position(App_Operate_Models):
    def __init__(self):
        from .forms import Forms_Position as import_forms
        from .models import Position as import_models
        self.import_forms = import_forms
        self.import_models = import_models
        self.model_cnname = '岗位'
        self.model_name = 'position'
        self.forgkey_field_list = [ 'department'] 
        self.list_title_list = ['id' , '职位' , '部门'  , '职责', '操作']
        self.detail_title_list = [ '职位' , '部门'  , '职责']
        self.detail_field_list = ['name', 'department_id', 'description']
        self.detail_basic_querysql = '''
            SELECT
                position.id,
                position.name,
                department.name,
                position.description
            FROM
                lykops.basicdata_position AS position
            LEFT JOIN lykops.basicdata_department AS department ON department_id = department.id
        '''
        
        self.list_basic_querysql = self.detail_basic_querysql
        self.app_name = App_Name
        self.app_basedir = App_Basedir
        self.op_user = ''
        

class Department(App_Operate_Models):
    def __init__(self):
        from .forms import Forms_Department as import_forms
        from .models import Department as import_models
        self.import_forms = import_forms
        self.import_models = import_models
        self.model_cnname = '部门'
        self.model_name = 'department'
        self.forgkey_field_list = [ 'supervising_authority'] 
        self.list_title_list = ['id' , '部门' , '上级部门'  , '职责', '操作']
        self.detail_title_list = [ '部门' , '上级部门'  , '职责']
        self.detail_field_list = ['name', 'supervising_authority_id', 'description']
        self.detail_basic_querysql = '''
            SELECT
                department.id,
                department.name,
                (
                    SELECT
                        name
                    FROM
                        lykops.basicdata_department
                    WHERE
                        id = department.supervising_authority_id
                ) AS supervising_authority,
                department.description
            FROM
                lykops.basicdata_department AS department
        '''
        
        self.list_basic_querysql = self.detail_basic_querysql
        self.app_name = App_Name
        self.app_basedir = App_Basedir
        self.op_user = ''
        
        
class Person(App_Operate_Models):
    def __init__(self):
        from .forms import Forms_Person as import_forms
        from .models import Person as import_models
        self.import_forms = import_forms
        self.import_models = import_models
        self.model_cnname = '员工'
        self.model_name = 'person'
        self.forgkey_field_list = [ 'department' , 'leaders' , 'position'] 
        self.detail_title_list = ['姓名' , '部门' , '领导'  , '岗位', '手机' , '固话' , '公司邮箱', '个人邮箱', '微信', 'QQ' , '现住地址' , '入职时间' , '描述']
        self.list_title_list = ['id' , '姓名' , '部门'  , '岗位', '手机' , '公司邮箱', '微信', 'QQ', '操作']
        self.detail_field_list = ['name', 'department_id', 'leaders_id' , 'position_id' , 'mob' , 'tel' , 'mail' , 'self_mail' , 'wxchat' , 'qq' , 'location' , 'start_time' , 'description']
        self.list_basic_querysql = '''
            SELECT
                person.id,
                person.name,
                department.name,
                (
                    SELECT
                        name
                    FROM
                        lykops.basicdata_position
                    WHERE
                        id = person.position_id
                ) AS position,
                person.mob,
                person.mail,
                person.wxchat,
                person.qq
            FROM
                lykops.basicdata_person AS person
            LEFT JOIN lykops.basicdata_department AS department ON department_id = department.id
        '''
        
        self.detail_basic_querysql = '''
            SELECT
                person.id,
                person.name,
                department.name,
                (
                    SELECT
                        name
                    FROM
                        lykops.basicdata_person
                    WHERE
                        id = person.leaders_id
                ) AS leader,
                (
                    SELECT
                        name
                    FROM
                        lykops.basicdata_position
                    WHERE
                        id = person.position_id
                ) AS position,
                person.mob,
                person.tel,
                person.mail,
                person.self_mail,
                person.wxchat,
                person.qq,
                person.location,
                person.start_time,
                person.description
            FROM
                lykops.basicdata_person AS person
            LEFT JOIN lykops.basicdata_department AS department ON department_id = department.id
        '''
        self.app_name = App_Name
        self.app_basedir = App_Basedir
        self.op_user = ''
        
        
class Business_System(App_Operate_Models):
    def __init__(self):
        from .forms import Forms_Business_System as import_forms
        from .models import Business_System as import_models
        self.import_forms = import_forms
        self.import_models = import_models
        self.model_cnname = '业务系统'
        self.model_name = 'business_system'
        self.type_list = ['' , '未上线' , '运营中' , '下架']
        self.forgkey_field_list = ['belong2project' , 'project_manager' , 'developer_manager' , 'test_manager' , 'operate_manager'] 
        self.list_title_list = ['id' , '系统名' , '归属项目'  , '上线时间', '阶段', '项目经理', '研发负责人', '测试负责人', '运维负责人', '操作']
        self.detail_title_list = ['系统名' , '归属项目'  , '阶段', '上线时间', '项目经理', '研发负责人', '测试负责人', '运维负责人', '描述']
        self.detail_field_list = ['name', 'belong2project_id', 'type', 'start_time' , 'project_manager_id', 'developer_manager_id' , 'test_manager_id', 'operate_manager_id' , 'description']
        self.detail_basic_querysql = '''
            SELECT
                business_system.id,
                business_system.name,
                (
                    SELECT
                        name
                    FROM
                        lykops.basicdata_business_system
                    WHERE
                        id = business_system.belong2project_id
                ) AS belong2project,
                business_system.type,
                business_system.start_time,
                person.name ,
                (
                    SELECT
                        name
                    FROM
                        lykops.basicdata_person
                    WHERE
                        id = business_system.developer_manager_id
                ) AS developer_manager,
                (
                    SELECT
                        name
                    FROM
                        lykops.basicdata_person
                    WHERE
                        id = business_system.test_manager_id
                ) AS test_manager,
                (
                    SELECT
                        name
                    FROM
                        lykops.basicdata_person
                    WHERE
                        id = business_system.operate_manager_id
                ) AS operate_manager,
                business_system.description
            FROM
                lykops.basicdata_business_system AS business_system
                LEFT JOIN lykops.basicdata_person AS person ON project_manager_id = person.id
        '''
        
        self.list_basic_querysql = self.detail_basic_querysql
        self.app_name = App_Name
        self.app_basedir = App_Basedir
        self.op_user = ''
        
