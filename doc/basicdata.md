basicdata基础数据

**基础数据** 解决必须只能手动输入的基础数据，包括供应商、机房宽带、硬软件、第三方服务、部门等，为其他app提供数据支撑。

各个表（下面用表的后缀名来表示，前缀为basicdata_）的用途：

    provider：登记供应商/制造商的官方、销售、客服、技术支持等部门的联系方式
    机房和带宽：
        idc：登记机房的类型、供应商、联系方式，关联provider
        rack：登记机柜的使用状态、开始结束时间、编号、规格、价格等信息，关联provider和idc
        bandwidth：登记带宽的使用状态、开始结束时间、规格、价格等信息，关联provider和idc
        ip_segment：登记网段使用状态、开始结束时间、规格、价格等信息，关联bandwidth和idc
    第三方服务：
        domain：登记域名注册、DNS解析、备案等使用状态、开始结束时间、价格等信息，关联provider
        wechat_pubno：登记微信公众号的基本信息，包括二维码
        third_service：登记第三方服务的使用状态、开始结束时间、规格、价格等信息，关联provider
    硬软件：
        hardware_brand：登记硬件的型号、制造商等信息，所有硬件型号全部由此表登记，关联provider
        hardware：登记硬件的采购、报废时间、SN、价格、固定资产编号、规格等信息，关联provider和hardware_brand
        software_type：登记软件的类型、开发商等信息，关联provider
        software：登记软件类型、供应商、SN、采购和许可到期时间、成本等信息，关联provider
    组织机构：
        department：登记部门信息
        position：登记岗位信息，关联department
        person：登记雇员的部门、岗位、联系方式等信息，关联poistion
        business_system：登记业务系统的开发、项目、测试、运维等负责人，，关联person
        
        
说明：

    1、关于关联provider表：
		机房和带宽、第三方服务、硬软件服务很多表关联provider
		为了减少筛选，通过类型对供应商进行筛选，例如hardware表只会出现provider表的类型为硬/软件供应商的内容
		部分表有两个字段关联到provider，是考虑到制造商和采购商分离
    2、字段使用状态值为“到期”的，将不会在list页面上展示，需要手动进行授权
    3、每个数据库表有6个操作：新增、编辑、列表、详细信息、导出、导入，不会有删除这个操作
        如果需要删除有两种方式：直接登录到数据库上操作或者使用状态设置为到期
    4、关于代码实现，一个‘懒’字了得：
 		在django中实现数据库操作，至少有以下几个python文件：models.py【定义数据库字段】、forms.py【定义编辑、新增forms】、views.py【操作具体实现方式，绝大部分代码共用】、UI【web页面，代码共用】
		每次新增一个表，要实现功能的话，只需要修改models.py、forms.py、views.py
  			第一步：在models.py上定义好数据库字段
			第二步：在forms.py上编写类，继承ModelForm，在__init__函数中修改字段信息【例如：某些字段可为空、外键表id转化为name等】，在添加一个Meta类。比继承Forms减少50%以上代码
			第三步：在views.py上编写一个class，编写__init__即可，参考其他class
 			第四步：修过该目录的urls.py，添加对应的功能URL
                                
		关于详细功能实现【views.py】，把各个表实现上述6个功能代码进行统一，继承api模块的App_Operate_Models函数。
            **App_Operate_Models**，继承library/db_page下的Operate_Models，重写实现list【列表展示】和import【导入】等功能
            **Operate_Models**实现了，实现add【新增】、edit【编辑】、detail【详细信息】、export【导出】功能。
                                        
        关于模板页面：
            有3个：list.html【列表展示】、detail.html【详细信息展示】、add_edit.html【新增和编辑】
                
        这样做的优势：模块化、代码重复使用、新增表实现功能快、减少代码量【大约减少50~75%】
        劣势：由于功能太过于统一、不适合个性化【可以新增一个页面或者模块，进行分离】
 