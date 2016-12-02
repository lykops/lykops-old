import time , re

from library.handle_datetime import date_convert
from lykops.settings import STATIC_ROOT


class Export_File():
    def __init__(self, app_name , op_user , op_model , filename_front  , title_list , query_set) :
        self.app_name = app_name
        self.op_user = op_user
        self.op_model = op_model
        if title_list and query_set:
            self.filename_front = filename_front + time.strftime("%Y%m%d%H%M%S", time.localtime())
            self.title_list = title_list
            self.query_set = query_set
        else :
            return '文件位空'
           
    def xls(self):
        from xlwt import Workbook
    
        filename = self.filename_front + '.xls'
        wb = Workbook(encoding='utf-8')  
        wb_sheet = wb.add_sheet("sheet1")
        for title in self.title_list:
            wb_sheet.write(0, self.title_list.index(title), title)
            
        for line in self.query_set :
            row_no = (self.query_set.index(line) + 1)
            print(line)
            col_no = 0
            for column in line[1:] :
                if col_no == len(line) - 2:
                    # 2016-10-17 15:21:33.348313+00:00
                    re.split('\.' , str(column))[0]
                wb_sheet.write(row_no, col_no, column)
                col_no += 1
                # wb.write(行, 列, 数据)
        return filename
    
    def xlsx(self , request):
        from xlsxwriter import Workbook
    
        filename = self.filename_front + '.xlsx'
        wb = Workbook(filename)
        # wb.encoding = 'gbk'
        wb_sheet = wb.add_worksheet()
        wb_sheet.write_row('A1' , self.title_list)
        for line in self.query_set :
            row_no = (self.query_set.index(line) + 2)
            wb_sheet.write_row('A' + str(row_no) , line[1:-1])

        wb_sheet.save
        wb_sheet.close()
        return filename

class Import_File():
# Uploadfile_Importdb():
    def __init__(self, file, filename):
        self.filename = filename
        self.file = file

    def import2db(self):
        if self.file.content_type == 'application/vnd.ms-excel' or 'application/msexcel' :
            # nginx为application/vnd.ms-excel
            # 纯django为'application/msexcel' :
            import xlrd
            # excel读工具
            openxls = xlrd.open_workbook(self.filename)  # 打开文件
            datatable = openxls.sheet_by_index(0)  # 获取工作表
            row_no = datatable.nrows  # 行数
            datalist = []
            for i in range(1, row_no):
                row = datatable.row_values(i)  # 获取每行值
                new_row = []
                
                for col in row :
                    col = str(col)
                    if re.search('^[0-9]{4}[年|-|/][0-9]{2}[月|-|/][0-9]{2}[日]{0,1}[ ]{0,1}[0-9]{2}:[0-9]{2}:[0-9]{2}$', col) :
                        col = date_convert(col , '%Y-%m-%d %H:%M:%S')
                    elif re.search('^[0-9]{4}[年|-|/][0-9]{2}[月|-|/][0-9]{2}[日]{0,1}$', col) :
                        col = date_convert(col , '%Y-%m-%d')
                    elif re.search('^[0-9]{1,}.0$', col) :
                        col = int(float(col))
                    else :
                        col = col
                        
                    new_row.append(col)
                    
                datalist.append(new_row)
                
            return datalist
            
        if self.file.content_type == 'application/pdf' :
            pass
