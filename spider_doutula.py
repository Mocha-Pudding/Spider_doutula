# 使用传统方式下载表情包
# 斗图啦网址：http://www.doutula.com/photo/list/


########################### 使用传统方式爬取和下载表情包 ###########################
import requests
from lxml import etree
from urllib import request
import os
import re

def parse_page(url):
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'
    }
    response = requests.get(url,headers=headers)
    text = response.text
    html = etree.HTML(text)
    imgs = html.xpath("//div[@class='page-content text-center']//img[@class!='gif']")
    for img in imgs:
        # print(etree.tostring(img))
        img_url = img.get('data-original')      #获取图片的url
        # print(img_url)
        alt = img.get('alt')       #获取图片名字
        alt = re.sub(r'[\?？\.，。!！]','',alt)      #正则表达式去除文件名中的特殊字符  re模块
        suffix = os.path.splitext(img_url)[1]      #获取图片的后缀名 os模块下的分割
        # print(suffix)
        filename = alt + suffix      #构建图片的名字（名字+后缀名）
        # print(filename)
        request.urlretrieve(img_url,'images/'+filename)

def main():
    for x in range(1,101):      #以爬取前100页为例
        url = 'http://www.doutula.com/photo/list/?page=%d' %x      #构建url
        parse_page(url)
        # break      #break掉只获取第一页的表情包

if __name__ == '__main__':
    main()