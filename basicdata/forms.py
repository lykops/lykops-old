import re, os, sys

from django import forms
from django.contrib.admin import widgets
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.db.models.sql.query import Query
from django.forms.widgets import *

from library.database import operate_nativesql

from .models import *


def name_vaildate(value):
    # 自定义验证方法（正则匹配）
    name_re = re.compile(r'^[a-zA-Z]{1}\w+$')
    if not name_re.match(value):
        raise ValidationError('姓名格式错误')


def sex_vaildate(value):
    li = [1, 2]
    if value not in li:
        raise ValidationError('请选择性别')


def telno_validate(value):
    mobile_re = re.compile(r'^1[3-5,7-8][0-9]{9}$')
    # 手机
    tel_re = re.compile(r'^0[1-9][0-9]{1,2}-[2-8][0-9]{6,7}$')
    # 没有分机号
    tel1_re = re.compile(r'^0[1-9][0-9]{1,2}-[2-8][0-9]{6,7}-[0-9]')
    # 有分机号
    sep48_re = re.compile(r'^[4,8]00[0-9]{7}$')
    # 400或者800
    sep9_re = re.compile(r'^9[0-9]{4,5}$')
    # 9特殊服务号码
    sep5_re = re.compile(r'^100[0-9]{2}$')
    
    
    if mobile_re.match(str(value)) or tel_re.match(str(value)) or tel1_re.match(str(value)) or sep48_re.match(str(value)) or  sep9_re.match(str(value))  or  sep5_re.match(str(value)) :
        pass
    else :
        raise ValidationError('电话号码格式错误，正确格式为固话：0[1-9][0-9]{1,2}-[2-8][0-9]{6,7}【-分机号码】，手机：1[3-5,7-8][0-9]{9}，400[0-9]{9}，9[0-9]{4,5}')  # 如果没有匹配到主动触发一个错误


def qq_validate(value):
    qq_re = re.compile(r'^[1-9][0-9]{4,}$')
    if not qq_re.match(str(value)) and not str(value):
        raise ValidationError('QQ号码格式错误')  # 如果没有匹配到主动触发一个错误


def list_addempty(query_set):
    temp = ('', '---------')
    query_set = list(query_set)
    query_set.insert(0, temp)
    return query_set


class Forms_Provider(forms.ModelForm): 
    type_choices = (
        ('服务供应商' , '服务供应商') ,
        ('电信运营商' , '电信运营商') ,
        ('机房供应商' , '机房供应商') ,
        ('硬软件供应商' , '硬软件供应商') ,
        ('硬件制造商' , '硬件制造商') ,
        ('软件开发商' , '软件开发商') ,
       )
    
    # from django.forms.widgets import CheckboxSelectMultiple, SelectMultiple
    # type = forms.MultipleChoiceField(label=u'类型', choices=type_choices, widget=CheckboxSelectMultiple()) 
    # 复选框
    # type = forms.MultipleChoiceField(label=u'类型*', widget=SelectMultiple(), choices=type_choices)
    # 下拉框

    def __init__(self, *args, **kwargs):
        super(Forms_Provider, self).__init__(*args, **kwargs)
        self.fields['website'].required = False
        self.fields['location'].required = False
        self.fields['salesman'].required = False
        self.fields['description'].required = False
        self.fields['tel'].validators = [telno_validate]
        
    '''
    Field.initial,initial初始化，用于指定字段的值当在一个未绑定表单中渲染字段时。
    name = forms.CharField(initial='your name')
    '''
    class Meta:  
        model = Provider
        fields = '__all__'

provider_idcserver_queryset = Provider.objects.using('mysql_read').filter(Q(type__contains='机房供应商') | Q(type__contains='服务供应商')).values_list('id' , 'name').distinct()
class Forms_Idc(forms.ModelForm):
    def __init__(self , *args , **kwargs):
        super(Forms_Idc , self).__init__(*args, **kwargs)
        self.fields['description'].required = False
        self.fields['provider'].required = False
        self.fields['tel'].validators = [telno_validate]
        self.fields['provider'].choices = list_addempty(provider_idcserver_queryset)
    # provider = forms.ModelMultipleChoiceField(queryset=provider.objects.values('name').distinct())


    class Meta :
        model = Idc
        fields = '__all__'
   

idc_tuanzi_queryset = Idc.objects.using('mysql_read').filter((Q(type__contains='托管') | Q(type__contains='自建')) & Q(status__contains='使用中')).values_list('id' , 'name').distinct()

class Forms_Rack(forms.ModelForm):
    def __init__(self , *args , **kwargs):
        super(Forms_Rack , self).__init__(*args, **kwargs)
        self.fields['fixed_no'].required = False
        self.fields['expired_time'].required = False
        self.fields['price'].required = False
        self.fields['max_power'].required = False
        self.fields['max_device'].required = False
        self.fields['description'].required = False
        
        self.fields['idc'].choices = list_addempty(idc_tuanzi_queryset)
        
    class Meta :
        # start_time = forms.DateField(widget=widgets.AdminDateWidget(), label='使用时间')
        model = Rack
        fields = '__all__'
        widgets = {
                            'price':TextInput,
                            'max_power':TextInput,
                            'max_device':TextInput
                        }


class Forms_Bandwidth(forms.ModelForm):
    def __init__(self , *args , **kwargs):
        super(Forms_Bandwidth , self).__init__(*args, **kwargs)
        self.fields['expired_time'].required = False
        self.fields['description'].required = False
        query_set = Provider.objects.using('mysql_read').filter(Q(type__contains='电信运营商') | Q(type__contains='机房供应商')).values_list('id' , 'name').distinct()
        self.fields['provider'].choices = list_addempty(query_set)
        self.fields['idc'].choices = list_addempty(idc_tuanzi_queryset)


    class Meta :
        # start_time = forms.DateField(widget=widgets.AdminDateWidget(), label='使用时间')
        model = Bandwidth
        fields = '__all__'
        widgets = {
                            'price':TextInput,
                            'rate':TextInput
                        }


class Forms_Ip_Segment(forms.ModelForm):
    def __init__(self , *args , **kwargs):
        super(Forms_Ip_Segment , self).__init__(*args, **kwargs)
        self.fields['description'].required = False

        self.fields['idc'].choices = list_addempty(idc_tuanzi_queryset)

        query_set = Bandwidth.objects.using('mysql_read').filter(Q(status__contains='使用')).values_list('id' , 'name').distinct()
        self.fields['bandwidth'].choices = list_addempty(query_set)


    class Meta :
        model = Ip_Segment
        fields = '__all__'
        widgets = {
                            'price':TextInput
                        }


class Forms_Domain(forms.ModelForm):
    def __init__(self , *args , **kwargs):
        super(Forms_Domain , self).__init__(*args, **kwargs)
        self.fields['description'].required = False
        self.fields['dns_provider'].required = False
        self.fields['icp_provider'].required = False
        self.fields['icp_id'].required = False

        self.fields['provider'].choices = list_addempty(provider_idcserver_queryset)
        self.fields['icp_provider'].choices = list_addempty(provider_idcserver_queryset)
        self.fields['dns_provider'].choices = list_addempty(provider_idcserver_queryset)
        # 因为域名不一定做域名解析，所以这部分为空

    class Meta :
        model = Domain
        fields = '__all__'
        widgets = {
                            'price':TextInput,
                            'dns_price':TextInput
                        }


class Forms_Third_Service(forms.ModelForm):
    def __init__(self , *args , **kwargs):
        super(Forms_Third_Service , self).__init__(*args, **kwargs)
        self.fields['description'].required = False
        query_set = Provider.objects.using('mysql_read').filter(Q(type__contains='服务供应商') | Q(type__contains='机房服务商')).values_list('id' , 'name').distinct()
        self.fields['provider'].choices = list_addempty(query_set)
        self.fields['manufacturer'].choices = list_addempty(query_set)


    class Meta :
        model = Third_Service
        fields = '__all__'
        widgets = {
                            'price':TextInput
                        }


class Forms_Wechat_Pubno(forms.ModelForm):
    def __init__(self , *args , **kwargs):
        super(Forms_Wechat_Pubno , self).__init__(*args, **kwargs)
        self.fields['start_time'].required = False
        self.fields['expired_time'].required = False
        self.fields['qr_code'].required = False
        self.fields['auth_file'].required = False
        self.fields['description'].required = False
        self.fields['oper'].required = False
        

    class Meta :
        model = Wechat_Pubno
        fields = '__all__'


class Forms_Hardware_Brand(forms.ModelForm):
    def __init__(self , *args , **kwargs):
        super(Forms_Hardware_Brand , self).__init__(*args, **kwargs)
        self.fields['description'].required = False
        query_set = Provider.objects.using('mysql_read').filter(Q(type__contains='硬件')).values_list('id' , 'name').distinct()
        self.fields['manufacturer'].choices = list_addempty(query_set)


    class Meta :
        model = Hardware_Brand
        fields = '__all__'
        widgets = {
                            'slp':TextInput
                        }


class Forms_Hardware(forms.ModelForm):
    def __init__(self , *args , **kwargs):
        super(Forms_Hardware , self).__init__(*args, **kwargs)
        self.fields['description'].required = False
        self.fields['pn'].required = False
        query_set = Provider.objects.using('mysql_read').filter(Q(type__contains='硬件')).values_list('id' , 'name').distinct()
        self.fields['provider'].choices = list_addempty(query_set)
        query_set = Hardware_Brand.objects.using('mysql_read').filter().values_list('id' , 'name').distinct()
        self.fields['type'].choices = list_addempty(query_set)


    class Meta :
        model = Hardware
        fields = '__all__'
        widgets = {
                            'price':TextInput
                        }


class Forms_Software_Type(forms.ModelForm):
    def __init__(self , *args , **kwargs):
        super(Forms_Software_Type , self).__init__(*args, **kwargs)
        self.fields['description'].required = False
        query_set = Provider.objects.using('mysql_read').filter(Q(type__contains='软件')).values_list('id' , 'name').distinct()
        self.fields['manufacturer'].choices = list_addempty(query_set)
        
    
    class Meta :
        model = Software_Type
        fields = '__all__'


class Forms_Software(forms.ModelForm):
    def __init__(self , *args , **kwargs):
        super(Forms_Software , self).__init__(*args, **kwargs)
        self.fields['description'].required = False
        self.fields['sn'].required = False
        self.fields['start_time'].required = False
        self.fields['price'].required = False
        self.fields['cost'].required = False
        self.fields['snend_time'].required = False
        query_set = Provider.objects.using('mysql_read').filter(Q(type__contains='软件')).values_list('id' , 'name').distinct()
        self.fields['provider'].choices = list_addempty(query_set)
        
        query_set = Software_Type.objects.using('mysql_read').filter().values_list('id' , 'name').distinct()
        self.fields['type'].choices = list_addempty(query_set)
        
        
    class Meta :
        model = Software
        fields = '__all__'
        widgets = {
                            'price':TextInput,
                            'cost':TextInput
                        }


class Forms_Position(forms.ModelForm):
    def __init__(self , *args , **kwargs):
        super(Forms_Position , self).__init__(*args, **kwargs)
        query_set = Department.objects.using('mysql_read').filter().values_list('id' , 'name').distinct()
        self.fields['department'].choices = list_addempty(query_set)


    class Meta :
        model = Position
        fields = '__all__'
        

class Forms_Department(forms.ModelForm):
    def __init__(self , *args , **kwargs):
        super(Forms_Department , self).__init__(*args, **kwargs)
        query_set = Department.objects.using('mysql_read').filter().values_list('id' , 'name').distinct()
        self.fields['supervising_authority'].choices = list_addempty(query_set)

    class Meta :
        model = Department
        fields = '__all__'


class Forms_Person(forms.ModelForm):
    def __init__(self , *args , **kwargs):
        super(Forms_Person , self).__init__(*args, **kwargs)
        query_set = Department.objects.using('mysql_read').filter().values_list('id' , 'name').distinct()
        self.fields['department'].choices = list_addempty(query_set)

        query_set = Person.objects.using('mysql_read').filter().values_list('id' , 'name').distinct()
        self.fields['leaders'].choices = list_addempty(query_set)
        
        query_set = Position.objects.using('mysql_read').filter().values_list('id' , 'name').distinct()
        self.fields['position'].choices = list_addempty(query_set)
        
        self.fields['tel'].required = False
        self.fields['position'].required = False
        self.fields['location'].required = False
        self.fields['start_time'].required = False
        self.fields['description'].required = False
        self.fields['self_mail'].required = False
        self.fields['mob'].validators = [telno_validate]
        self.fields['tel'].validators = [telno_validate]
        self.fields['qq'].validators = [qq_validate]

    class Meta :
        model = Person
        fields = '__all__'


class Forms_Business_System(forms.ModelForm):
    def __init__(self , *args , **kwargs):
        super(Forms_Business_System , self).__init__(*args, **kwargs)
        query_set = Business_System.objects.using('mysql_read').filter().values_list('id' , 'name').distinct()
        self.fields['belong2project'].choices = list_addempty(query_set)
        
        query_set = Person.objects.using('mysql_read').filter().values_list('id' , 'name').distinct()
        self.fields['project_manager'].choices = list_addempty(query_set)
        
        query_set = Person.objects.using('mysql_read').filter().values_list('id' , 'name').distinct()
        self.fields['developer_manager'].choices = list_addempty(query_set)
        
        query_set = Person.objects.using('mysql_read').filter().values_list('id' , 'name').distinct()
        self.fields['test_manager'].choices = list_addempty(query_set)
        
        query_set = Person.objects.using('mysql_read').filter().values_list('id' , 'name').distinct()
        self.fields['operate_manager'].choices = list_addempty(query_set)

        self.fields['belong2project'].required = False
        self.fields['start_time'].required = False
        self.fields['description'].required = False

    class Meta :
        model = Business_System
        fields = '__all__'
