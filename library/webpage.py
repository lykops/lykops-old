import time, re , os

from django.http.response import HttpResponse

from library.handle_datetime import date_convert
from lykops.settings import BASE_DIR


def  paginator_options(request , query_set): 
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    perpage = request.GET.get('perpage')
    try:
        paginator = Paginator(query_set, perpage) 
    except :
        perpage = 10
        paginator = Paginator(query_set, perpage) 

    curr_page = request.GET.get('page')
    try:
        curr_page_query_list = paginator.page(curr_page)
    except EmptyPage:
        curr_page_query_list = paginator.page(paginator.num_pages)
    except :
        curr_page_query_list = paginator.page(1)

    max_page = paginator.num_pages
    curr_page = curr_page_query_list.number
    min_page = curr_page - 5 if curr_page - 5 >= 1 else 1
    max_page = curr_page + 6 if curr_page + 6 <= max_page  else max_page + 1
    page_range = range(min_page , max_page)
    
    request_dict = {'query_list': curr_page_query_list , "page_range":page_range , 'max_page':max_page , 'perpage' :perpage}
    return request_dict
    
    
class Export_File_Html():
    def __init__(self, filename_front  , title_list , query_set) :
        if title_list and query_set:
            self.filename_front = filename_front + time.strftime("%Y%m%d%H%M%S", time.localtime())
            self.title_list = title_list
            self.query_set = query_set
        else :
            return HttpResponse('文件为空')
           
    def xls(self, requetst):
        from xlwt import Workbook,easyxf
    
        filename = self.filename_front + '.xls'
        wb = Workbook(encoding='utf-8')  
        wb_sheet = wb.add_sheet("sheet1")
        
        style = easyxf('pattern: pattern solid;')
        # 电子表格每个格子样式
        
        for title in self.title_list:
            wb_sheet.write(0, self.title_list.index(title), title)
            
        for line in self.query_set :
            row_no = (self.query_set.index(line) + 1)
            col_no = 0
            for column in line[1:] :
                if re.search('^[0-9]{4}[-/][0-9]{2}[-/][0-9]{2}$', str(column)) :
                    column = date_convert(str(column) , '%Y年%m月%d日')
                elif re.search('^[0-9]{4}[-/][0-9]{2}[-/][0-9]{2}[ ]{0,1}[0-9]{2}:[0-9]{2}:[0-9]{2}$', str(column)) :
                    column = date_convert(str(column) , '%Y年%m月%d日 %H:%M:%S')

                wb_sheet.write(row_no, col_no, column)
                col_no += 1
                # wb.write(行, 列, 数据)
        response = HttpResponse(content_type='application/msexcel')
        response['Content-Disposition'] = 'attachment; filename=' + filename
        # 不会保存在本地，直接在页面导出
        wb.save(response)
        return response


def uploadfile(file, filename, upload_dir):
    if not os.path.exists(upload_dir):
        try :
            os.mkdir(upload_dir)
        except :
            os.makedirs(upload_dir)
    '''    
    if self.file.size > 5 * 1024 * 1024 :
        return HttpResponse('超过上传限制，最大5M')
    '''
    
    filename = upload_dir + filename
    
    with open(filename, 'wb+') as dest:
        for chunk in file.chunks():
            dest.write(chunk)
        return filename

