# 注意：该项目暂停开发


# lykops

**lykops**是一款由Python3编写的运维自动化工具，为了减轻运维工作量而开发。

运行环境：

	建议：Linux、Python3+django1.10、MySQL、Nginx
	测试环境：CentOS7.2+Python3.5+django1.10+MySQL5.7+Nginx1.9
	必须使用Nginx，否则静态文件无法展示，页面错乱


已完成功能：

    **基础数据app**:解决必须只能手动输入的基础数据，包括供应商、机房宽带、硬软件、第三方服务、部门等，为其他app提供数据支撑。


目录说明：

    basicdata：基础数据APP
    doc：文档
    file：上传文件的文件夹
    install：安装脚本、依赖包文件
    library：基础功能库
    logs：日志
    lykops：该项目管理包
    static：静态文件夹，不含上传文件
    templates：共用模板，不含各个app模板【各个app模板文件夹放在自己app下的templates下】
    
APP下的通用目录：

	templates：各个app模板文件夹
	templatetags：tags
