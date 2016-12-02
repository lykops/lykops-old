from django.db import models

from library.webpage import uploadfile
from lykops.settings import STATIC_ROOT, MEDIA_ROOT


# Create your models here.
class Provider(models.Model):
    type_choices = (
        ('服务供应商' , '服务供应商') ,
        ('电信运营商' , '电信运营商') ,
        ('机房供应商' , '机房供应商') ,
        ('硬软件供应商' , '硬软件供应商') ,
        ('硬件制造商' , '硬件制造商') ,
        ('软件开发商' , '软件开发商') ,
       )
    name = models.CharField(verbose_name='简称*' , max_length=15 , blank=False , unique=True)
    full_name = models.CharField(verbose_name='全称*' , max_length=50 , blank=False , unique=True)
    type = models.CharField(verbose_name='类型*' , max_length=30 , choices=type_choices , db_index=True)
    tel = models.CharField(verbose_name='联系方式*' , max_length=30 , blank=False)
    location = models.CharField(verbose_name='地址*' , max_length=150 , blank=False)
    website = models.URLField(verbose_name='官网 ' , max_length=100  , null=True)
    salesman = models.CharField(verbose_name='销售联系方式' , max_length=254 , null=True)
    customer = models.CharField(verbose_name='客服联系方式*' , max_length=254)
    tech = models.CharField(verbose_name='技术联系方式*' , max_length=254)
    description = models.TextField(verbose_name='描述' , null=True)
    
    def __str__(self):
        return self.short_name


class Idc(models.Model):
    status_choices = (
        ('使用中' , '使用中') ,
        ('到期' , '到期') ,
       ) 
    type_choices = (
        ('公有云' , '公有云') ,
        ('自建' , '自建') ,
        ('托管' , '托管') ,
       )
    name = models.CharField(verbose_name='名称*' , max_length=15 , blank=False , unique=True)
    type = models.CharField(verbose_name='类型*' , max_length=15 , choices=type_choices , db_index=True)
    status = models.CharField(verbose_name='使用状态*' , max_length=15 , choices=status_choices , blank=False , db_index=True)
    provider = models.ForeignKey('provider' , verbose_name='供应商' , related_name='idc_provider', blank=True , null=True)
    tel = models.CharField(verbose_name='值班电话*' , max_length=30 , blank=False)
    location = models.CharField(verbose_name='机房地址*' , max_length=100 , blank=False , help_text='省份-城市-区-路-门牌号')
    description = models.TextField(verbose_name='描述' , null=True)

    def __str__(self):
        return self.name


class Rack(models.Model): 
    status_choices = (
        ('使用中' , '使用中') ,
        ('空闲' , '空闲') ,
        ('到期' , '到期') ,
       ) 
    name = models.CharField(verbose_name='名称*' , max_length=15 , blank=False , unique=True)
    status = models.CharField(verbose_name='使用状态*' , max_length=15 , choices=status_choices , blank=False , db_index=True)
    idc = models.ForeignKey('idc' , verbose_name='机房*' , related_name='rack_idc')
    fixed_no = models.CharField(verbose_name='编号'  , help_text='托管以机房标识为准，自建为资产编号' , max_length=50 , null=True)
    start_time = models.DateField(verbose_name='使用时间' , null=True)
    expired_time = models.DateField(verbose_name='到期时间' , null=True)
    price = models.IntegerField(verbose_name='价格*'  , help_text='托管：元/月/个，自建：元/个')
    max_power = models.IntegerField(verbose_name='最大电流（A）' , default='10')
    max_device = models.IntegerField(verbose_name='最大设备数' , default='12')
    description = models.TextField(verbose_name='描述')

    def __str__(self):
        return self.name


class Bandwidth(models.Model): 
    status_choices = (
        ('使用中' , '使用中') ,
        ('暂停' , '暂停') ,
        ('到期' , '到期') ,
       ) 
    type_choices = (
        ('单线' , '单线') ,
        ('多线多IP' , '多线多IP') ,
        ('双线BGP' , '双线BGP') ,
        ('三线BGP' , '三线BGP') ,
        ('多线BGP' , '多线BGP') ,
        ('专线' , '专线') ,
        ('E1' , 'E1') ,
       )
    name = models.CharField(verbose_name='名称*' , max_length=30 , blank=False , unique=True)
    type = models.CharField(verbose_name='类型*' , max_length=15 , choices=type_choices , blank=False , db_index=True)
    status = models.CharField(verbose_name='使用状态*' , max_length=30 , choices=status_choices , blank=False , db_index=True)
    provider = models.ForeignKey('provider' , verbose_name='供应商' , related_name='bandwidth_provider')
    idc = models.ForeignKey('idc' , verbose_name='归属机房*' , related_name='bandwidth_idc')
    start_time = models.DateField(verbose_name='计费时间*' , blank=False)
    expired_time = models.DateField(verbose_name='到期时间*' , blank=False)
    price = models.IntegerField(verbose_name='价格（元/月）*', blank=False)
    rate = models.IntegerField(verbose_name='带宽（M）*', blank=False)
    location = models.CharField(verbose_name='装机地址*' , blank=False , help_text='装机地址 省份-城市-区-路-门牌号，非专线填写装机地址，专线需填写两端地址'  , max_length=254)
    description = models.TextField(verbose_name='描述' , null=True)


class Ip_Segment(models.Model):
    status_choices = (
        ('使用中' , '使用中') ,
        ('到期' , '到期') ,
        ('闲置' , '闲置') ,
       ) 
    type_choices = (
        ('公网' , '公网') ,
        ('内网' , '内网') ,
       )
    name = models.CharField(verbose_name='名称*' , max_length=30 , blank=False , unique=True)
    type = models.CharField(verbose_name='类型*' , max_length=30 , choices=type_choices , db_index=True)
    status = models.CharField(verbose_name='使用状态*' , max_length=30 , choices=status_choices , blank=False , db_index=True)
    idc = models.ForeignKey('idc' , verbose_name='归属机房*' , related_name='ipsegment_idc')
    bandwidth = models.ForeignKey('bandwidth' , verbose_name='归属带宽*' , related_name='ipsegment_bandwidth')
    net_address = models.GenericIPAddressField(verbose_name='网段*' , blank=False , protocol='ipv4')
    net_mask = models.GenericIPAddressField(verbose_name='子网掩码*' , blank=False , protocol='ipv4')
    gateway = models.GenericIPAddressField(verbose_name='网关*' , blank=False , protocol='ipv4')
    price = models.IntegerField(verbose_name='价格（元/月）*'  , help_text='托管：元/月' , null=True)
    start_time = models.DateField(verbose_name='使用时间 *'  , default='2016-01-01')
    expired_time = models.DateField(verbose_name='到期时间*'  , default='2038-01-01')
    description = models.TextField(verbose_name='描述')


class Domain(models.Model):
    status_choices = (
        ('使用中' , '使用中') ,
        ('备案未用' , '备案未用') ,
        ('未备案' , '未备案') ,
        ('到期' , '到期') ,
       ) 
    name = models.CharField(verbose_name='域名*' , max_length=30 , blank=False , unique=True)
    status = models.CharField(verbose_name='使用状态*' , max_length=15 , choices=status_choices , blank=False , db_index=True)
    provider = models.ForeignKey('provider' , verbose_name='注册商*' , related_name='domain_provider')
    start_time = models.DateField(verbose_name='注册时间*' , blank=False)
    expired_time = models.DateField(verbose_name='到期时间*' , blank=False)
    price = models.IntegerField(verbose_name='域名价格（元/年）*' , blank=False)
    dns_provider = models.ForeignKey('provider' , verbose_name='DNS服务商' , related_name='dns_provider' , null=True, blank=True)
    dns_start_time = models.DateField(verbose_name='DNS解析时间' , default='2038-01-01')
    dns_expired_time = models.DateField(verbose_name='DNS到期时间' , default='2038-01-01')
    dns_price = models.IntegerField(verbose_name='DNS解析价格（元/年）' , default='0')
    icp_provider = models.ForeignKey('provider' , verbose_name='ICP备案商' , related_name='icp_provider' , null=True, blank=True)
    icp_start_time = models.DateField(verbose_name='ICP备案通过时间' , default='2038-01-01')
    icp_id = models.CharField(verbose_name='ICP备案号' , max_length=30 , null=True, blank=True)
    description = models.TextField(verbose_name='描述' , null=True, blank=True)


class Wechat_Pubno(models.Model):
    status_choices = (
        ('使用中' , '使用中') ,
        ('未认证' , '未认证') ,
        ('未年审' , '未年审') ,
       ) 
    type_choices = (
        ('服务号' , '服务号') ,
        ('企业号' , '企业号') ,
        ('订阅号' , '订阅号') ,
       ) 
    name = models.CharField(verbose_name='名称*' , max_length=30 , blank=False , unique=True)
    wxno = models.CharField(verbose_name='公众号*' , max_length=30 , blank=False)
    status = models.CharField(verbose_name='使用状态*' , max_length=15 , choices=status_choices , blank=False , db_index=True)
    type = models.CharField(verbose_name='类型*' , max_length=15 , choices=type_choices , blank=False , db_index=True)
    oper = models.CharField(verbose_name='运营者联系方式' , max_length=100  , null=True)
    manger = models.CharField(verbose_name='管理者联系方式*' , max_length=100  , blank=False)
    appid = models.CharField(verbose_name='应用id*' , max_length=30  , blank=False , unique=True)
    appsecret = models.CharField(verbose_name='应用密匙' , max_length=60  , blank=False)
    orig_id = models.CharField(verbose_name='原始ID*' , max_length=30  , blank=False , unique=True)
    start_time = models.DateField(verbose_name='下次年审时间' , default='2038-01-01')
    expired_time = models.DateField(verbose_name='最后下次年审时间' , default='2038-01-01')
    qr_code = models.ImageField(verbose_name='二维码')
    # upload_to，填写相对路径的话，绝对路径为MEDIA_ROOT+upload_to, upload_to='upload/basicdata/wechat_pubno'
    auth_file = models.FileField(verbose_name='txt文件')
    description = models.TextField(verbose_name='描述' , null=True)
  
    
    def __str__(self):
        return self.name

    
class Third_Service(models.Model):
    status_choices = (
        ('使用中' , '使用中') ,
        ('空闲' , '空闲') ,
        ('到期' , '到期') ,
       ) 
    type_choices = (
        ('CDN' ,'CDN' ) ,
        ('云服务器' ,'云服务器' ) ,
        ('RDS' , 'RDS') ,
        ('负载均衡' ,'负载均衡' ) ,
        ('安全' ,'安全') ,
        ('云存储' ,'云存储') ,
        ('AMP' ,'AMP' ) ,
        ('其他' ,'其他' ) ,
        )
    name = models.CharField(verbose_name='名称*' , max_length=30 , blank=False , unique=True)
    status = models.CharField(verbose_name='使用状态*' , max_length=15 , choices=status_choices , blank=False , db_index=True)
    type = models.CharField(verbose_name='类型*' , max_length=15 , choices=type_choices , blank=False , db_index=True)
    manufacturer = models.ForeignKey('provider' , verbose_name='服务提供商*' , related_name='third_service_manufacturer')
    provider = models.ForeignKey('provider' , verbose_name='采购商*' , related_name='third_service_provider')
    start_time = models.DateField(verbose_name='使用时间*' , blank=False)
    expired_time = models.DateField(verbose_name='到期时间*' , blank=False)
    price = models.IntegerField(verbose_name='价格（元/月）*' , blank=False)
    description = models.TextField(verbose_name='描述' , null=True)


class Hardware_Brand(models.Model):
    type_choices = (
        ('服务器' , '服务器') ,
        ('交换机' , '交换机') ,
        ('路由器' , '路由器') ,
        ('防火墙' , '防火墙') ,
        ('存储' , '存储') ,
        ('CPU' , 'CPU') ,
        ('硬盘' , '硬盘') ,
        ('内存' , '内存') ,
        ('电源' , '电源') ,
        ('其他' , '其他') ,
       )
    name = models.CharField(verbose_name='品牌 型号*' , max_length=100 , blank=False , unique=True)
    type = models.CharField(verbose_name='类型 *' , max_length=30 , choices=type_choices  , db_index=True)
    manufacturer = models.ForeignKey('provider' , verbose_name='制造商*' , related_name='hardware_manufacturer')
    slp = models.IntegerField(verbose_name='使用年限*' , blank=False)
    description = models.TextField(verbose_name='描述' , null=True)


class Hardware(models.Model): 
    status_choices = (
        ('使用中' , '使用中') ,
        ('闲置' , '闲置') ,
        ('到期' , '报废') ,
       )
    name = models.CharField(verbose_name='名称*' , max_length=50 , blank=False , unique=True)
    type = models.ForeignKey('hardware_brand' , verbose_name='硬件型号*' , related_name='hardware')
    status = models.CharField(verbose_name='使用状态*' , max_length=30 , choices=status_choices , db_index=True)
    provider = models.ForeignKey('provider' , verbose_name='制造商*' , related_name='hardware_provider')
    start_time = models.DateField(verbose_name='采购日期*' , blank=False)
    expired_time = models.DateField(verbose_name='报废时间*' , blank=False)
    price = models.IntegerField(verbose_name='采购价*' , blank=False)
    sn = models.CharField(verbose_name='SN*' , max_length=100)
    pn = models.CharField(verbose_name='PN' , max_length=100,null=True,blank=False)
    fixed_no = models.CharField(verbose_name='固定资产编号*' , null=True , max_length=100)
    description = models.TextField(verbose_name='描述' , null=True)


class Software_Type(models.Model): 
    type_choices = (
        ('OS' , 'OS') ,
        ('前端' , '前端') ,
        ('应用软件' , '应用软件') ,
        ('中间件' , '中间件') ,
        ('数据库' , '数据库') ,
        ('NoSQL' , 'NoSQL') ,
        ('存储' , '存储') ,
        ('办公软件' , '办公软件') ,
        ('其他软件' , '其他软件') ,
       )
    name = models.CharField(verbose_name='名称*' , max_length=50 , blank=False , unique=True)
    type = models.CharField(verbose_name='类型*' , max_length=30 , choices=type_choices , db_index=True)
    manufacturer = models.ForeignKey('provider' , verbose_name='制造商*' , related_name='software_manufacturer')
    description = models.TextField(verbose_name='描述' , null=True)


class Software(models.Model): 
    status_choices = (
        ('使用中' , '使用中') ,
        ('到期' , '许可到期') ,
       )
    name = models.CharField(verbose_name='名称*' , max_length=50 , blank=False , unique=True)
    type = models.ForeignKey('software_type' , verbose_name='软件类型*' , related_name='software_type')
    status = models.CharField(verbose_name='使用状态*' , max_length=30 , choices=status_choices , db_index=True)
    provider = models.ForeignKey('provider' , verbose_name='供应商*' , related_name='software_provider')
    sn = models.CharField(verbose_name='序列号' , max_length=100 , blank=True , null=True)
    start_time = models.DateField(verbose_name='采购日期'  , default='2038-01-01')
    price = models.IntegerField(verbose_name='采购价' , blank=True , null=True, default='0')
    cost = models.IntegerField(verbose_name='后续费用（元/年）' , blank=True , null=True, default='0')
    snend_time = models.DateField(verbose_name='许可到期日期'  , default='2038-01-01')
    description = models.TextField(verbose_name='描述' , null=True)


class Position(models.Model): 
    name = models.CharField(verbose_name='职位*' , max_length=30 , blank=False , unique=True)
    department = models.ForeignKey('department' , verbose_name='部门*' , related_name='position_department')
    description = models.TextField(verbose_name='职责*')


class Department(models.Model): 
    name = models.CharField(verbose_name='部门*' , max_length=20 , blank=False , unique=True)
    supervising_authority = models.ForeignKey('self' , verbose_name='上级部门*' , related_name='department_department', blank=True, null=True)
    description = models.TextField(verbose_name='描述')


class Person(models.Model): 
    name = models.CharField(verbose_name='姓名*' , max_length=15 , blank=False , unique=True)
    department = models.ForeignKey('department' , verbose_name='部门*' , related_name='person_department')
    leaders = models.ForeignKey('self' , verbose_name='领导' , related_name='person_leaders', blank=True, null=True)
    position = models.ForeignKey('position' , verbose_name='岗位*' , related_name='person_position')
    mob = models.CharField(verbose_name='手机*' , max_length=50)
    tel = models.CharField(verbose_name='固话' , max_length=50)
    mail = models.CharField(verbose_name='公司邮箱*' , max_length=50)
    self_mail = models.CharField(verbose_name='个人邮箱' , max_length=50)
    wxchat = models.CharField(verbose_name='微信*' , max_length=30)
    qq = models.CharField(verbose_name='QQ*' , max_length=30)
    location = models.CharField(verbose_name='现住地址' , max_length=30)
    start_time = models.DateField(verbose_name='入职时间*')
    description = models.TextField(verbose_name='描述' , null=True)

    
class Business_System(models.Model): 
    type_choices = (
        ('未上线' , '未上线') ,
        ('运营中' , '运营中') ,
        ('到期' , '下架') 
       )
    name = models.CharField(verbose_name='业务系统名*' , max_length=30 , blank=False , unique=True)
    belong2project = models.ForeignKey('self' , verbose_name='归属项目' , related_name='business_system_belong2project', blank=True, null=True)
    type = models.CharField(verbose_name='阶段*' , max_length=30 , choices=type_choices , db_index=True)
    start_time = models.DateField(verbose_name='上线时间*')
    project_manager = models.ForeignKey('person' , verbose_name='项目经理' , related_name='business_system_project_manager', blank=True, null=True)
    developer_manager = models.ForeignKey('person' , verbose_name='开发负责人' , related_name='business_system_developer_manager', blank=True, null=True)
    test_manager = models.ForeignKey('person' , verbose_name='测试负责人' , related_name='business_system_test_manager', blank=True, null=True)
    operate_manager = models.ForeignKey('person' , verbose_name='运维负责人*' , related_name='business_system_operate_manager')
    description = models.TextField(verbose_name='描述' , null=True)
    

'''
class Change_History(models.Model):
    name = models.CharField(verbose_name='名称*' , blank=False , editable=False , max_length=30 , db_index=True)
    type = models.CharField(verbose_name='类型*' , blank=False , editable=False , max_length=30 , db_index=True)
    old_value = models.TextField(verbose_name='旧值*' , blank=False , editable=False)
    new_value = models.TextField(verbose_name='新值*' , blank=False , editable=False)
    reason = models.TextField(verbose_name='原因*' , blank=False , editable=False)
    change_time = models.DateTimeField(blank=False , auto_now_add=True , editable=False)
'''
