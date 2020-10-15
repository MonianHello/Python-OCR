# encoding:utf-8
import requests
import base64
import re
import os
import os.path
from PIL import Image
import time

outputtext = "C:\\MonianHello\\list.txt"

os.system('mkdir C:MonianHello\\')

def IsValidImage(img_path):
    """
    判断文件是否为有效（完整）的图片
    :param img_path:图片路径
    :return:True：有效 False：无效
    """
    bValid = True
    try:
        Image.open(img_path).verify()
    except:
        bValid = False
    return bValid


def transimg(img_path):
    """
    转换图片格式
    :param img_path:图片路径
    :return: True：成功 False：失败
    """
    if IsValidImage(img_path):
        try:
            str = img_path.rsplit(".", 1)
            output_img_path = str[0] + ".jpg"
            print(output_img_path)
            im = Image.open(img_path)
            im.save(output_img_path)
            return True
        except:
            return False
    else:
        return False

def get_file_path(root_path,file_list,dir_list):
    #获取该目录下所有的文件名称和目录名称
    dir_or_files = os.listdir(root_path)
    for dir_file in dir_or_files:
        #获取目录或者文件的路径
        dir_file_path = os.path.join(root_path,dir_file)
        #判断该路径为文件还是路径
        if os.path.isdir(dir_file_path):
            dir_list.append(dir_file_path)
            #递归获取所有文件和目录的路径
            get_file_path(dir_file_path,file_list,dir_list)
        else:
            file_list.append(dir_file_path)        

def ocr(localfile):
    localfile = str(localfile)
    '''
    获取Access Token
    '''
    # encoding:utf-8
    ak = '[请输入在百度API获取的ak(通用文字识别)]'
    sk = '[请输入在百度API获取的sk(通用文字识别)]'
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id='+ak+'&client_secret='+sk
    response = requests.get(host)
    response = response.json()
    access_token = response.get('access_token')
    '''
    通用文字识别
    '''
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
    # 二进制方式打开图片文件
    f = open(str(localfile), 'rb')
    # 将图像文件转为base64编码方式
    img = base64.b64encode(f.read())
    params = {"image":img}
    # 请求url
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    output = response.json()
    #print('debug:'+str(output))
    if response:
        print('文本唯一识别码:'+str(output.get('log_id')))
        print('文件目录:'+path)
        print('共返回数据:'+str(output.get('words_result_num'))+'行')
        print('----------')
        textlist.append('文件目录:'+path)
        textlist.append('----------')
        for i in output.get('words_result'):
            print(i.get('words'))
            textlist.append(i.get('words'))
        print('==========')
        textlist.append('==========')
#ocr(re.sub(r'\\\\','/',i))
'''
dirlist = input('请拖拽文件到此，多个文件使用空格隔开')
for i in dirlist.split():
    try:
        ocr(i)
    except:
        print('无法访问文件或目录有误')
        print('请检查文件目录之间的空格')
'''
textlist = []
root_path = r"C:\MonianHello"
#用来存放所有的文件路径
file_list = []
#用来存放所有的目录路径
dir_list = []
get_file_path(root_path,file_list,dir_list)
file_list.pop(0)
fl=open(outputtext,'w')
print('==========')
print('M-N-H  OCR')
print('启动时间:'+time.asctime( time.localtime(time.time()) ))
print('共找到文件数:'+str(len(file_list)))
print('==========')
textlist.append('==========')
textlist.append('M-N-H  OCR')
textlist.append('启动时间:'+time.asctime( time.localtime(time.time()) ))
textlist.append('共找到文件数:'+str(len(file_list)))
textlist.append('==========')
for path in file_list:
    try:
        #transimg(path)
        ocr(path)
    except:
        print('出现内部错误')

print('识别完成，现在将结果写入文件...')

try:
    for i in textlist:
        fl.write(i)
        fl.write("\n")
    fl.write('结束时间:'+time.asctime( time.localtime(time.time()) ))
    fl.close()
    print('写入成功，已将文件写入'+str(outputtext))
    print('结束时间:'+time.asctime( time.localtime(time.time()) ))
except:
    print('写入失败，请确认'+fl+'目录以及文件存在')