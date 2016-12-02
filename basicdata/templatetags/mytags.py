import re , time , datetime,os,sys

from django import template
from django.template.context_processors import request
from lykops.settings import BASE_DIR

register = template.Library()

@register.filter
# ('img_display', img_display)
def str_display(value):
    value = str(value)
    full_filename = BASE_DIR + '/' + value
    
    img_format_list = ['gif' , 'jpeg' , 'jpg' , 'png' , 'ico' , 'bmp' , 'tif' , 'tiff' , 'wbmp' , 'jng' , 'svg' , 'svgz' , 'webp']
    # img_list = ['image/gif', 'image/jpeg', 'image/png', 'image/tiff', 'image/vnd.wap.wbmp', 'image/x-icon', 'image/x-jng', 'image/x-ms-bmp', 'image/svg+xml', 'image/webp']
    suffix_name = re.split('\.' , value)[-1]
    file_format_list = {'html', 'htm', 'css', 'xml', 'gif', 'jpeg', 'jpg', 'js', 'atom', 'rss', 'mml', 'txt', 'jad', 'wml', 'htc', 'png', 'tif', 'tiff', 'wbmp', 'ico', 'jng', 'bmp', 'svg', 'svgz', 'webp', 'woff', 'jar', 'war', 'json', 'hqx', 'doc', 'pdf', 'ps', 'eps', 'rtf', 'm3u8', 'xls', 'eot', 'ppt', 'wmlc', 'kml', 'kmz', '7z', 'cco', 'jardiff', 'jnlp', 'run', 'pl', 'pm', 'prc', 'pdb', 'rar', 'rpm', 'sea', 'swf', 'sit', 'tcl', 'tk', 'der', 'pem', 'xpi', 'xhtml', 'xspf', 'zip', 'bin', 'exe', 'deb', 'dmg', 'iso', 'img', 'msi', 'msp', 'docx', 'xlsx', 'pptx', 'mid', 'midi', 'mp3', 'ogg', 'm4a', 'ra', '3gpp', '3gp', 'ts', 'mp4', 'mpeg', 'mpg', 'mov', 'webm', 'flv', 'm4v', 'mng', 'asx', 'asf', 'wmv', 'avi'}
    
    if suffix_name in img_format_list :
        if os.path.exists(full_filename) and os.path.isfile(full_filename) :
            return '<img alt="image" width="100" height="100"  src="/' + value + '" />'
        else :
            return '文件不存在'
    elif suffix_name in file_format_list :        
        if os.path.exists(full_filename) and os.path.isfile(full_filename) :
            return '<a href="/' + value + '"><button type="button" class="btn btn-sm btn-primary" >下载</button></a>'
        else :
            return '文件' + value + '不存在'
    else :
        if re.search('^http://', value) or re.search('^https://', value) :
            return '<a href="' + value + '">' + value + '</a>' 
        elif value == '2038-01-01' :
            return ''
        else :
            return value
