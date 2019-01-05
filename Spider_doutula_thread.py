# 使用生产者与消费者模式多线程下载表情包
# 斗图啦网址：http://www.doutula.com/photo/list/


########################### 使用多线程方式爬取和下载表情包 ###########################
import requests
from lxml import etree
from urllib import request
import os
import re
from queue import Queue
import threading

class Producer(threading.Thread):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'
    }

    #构造函数
    def __init__(self, page_queue, img_queue, *args, **kwargs):
        super(Producer, self).__init__(*args, **kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue

    def run(self):
        while True:
            if self.page_queue.empty():
                break
            url = self.page_queue.get()
            self.parse_page(url)

    def parse_page(self, url):
        response = requests.get(url,headers=self.headers)
        text = response.text
        html = etree.HTML(text)
        imgs = html.xpath("//div[@class='page-content text-center']//img[@class!='gif']")
        for img in imgs:
            img_url = img.get('data-original')      #获取图片的url
            alt = img.get('alt')       #获取图片名字
            alt = re.sub(r'[\?？\.，。!！、\*\']','',alt)      #正则表达式去除文件名中的特殊字符  re模块
            suffix = os.path.splitext(img_url)[1]      #获取图片的后缀名 os模块下的分割
            filename = alt + suffix      #构建图片的名字（名字+后缀名）
            self.img_queue.put((img_url,filename))     #队列中以元组方式保存

class Consumer(threading.Thread):
    #同上，构造函数
    def __init__(self, page_queue, img_queue, *args, **kwargs):
        super(Consumer, self).__init__(*args, **kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue

    def run(self):
        while True:
            if self.img_queue.empty() and self.page_queue.empty():
                break
            img_url,filename = self.img_queue.get()    #返回来的元组，定义好两个已有的变量进行解包操作
            request.urlretrieve(img_url, 'images/'+filename)    #保存到本地
            print(filename+'  下载完成!')

def main():
    page_queue = Queue(100)     #定义好两个队列  页面的队列
    img_queue = Queue(1000)     #图片的队列
    for x in range(1,101):      #以爬取前100页为例
        url = 'http://www.doutula.com/photo/list/?page=%d' %x      #构建url
        page_queue.put(url)

    #给5个生产者线程
    for x in range(5):
        t = Producer(page_queue, img_queue)
        t.start()

    #再给5个消费者线程
    for x in range(5):
        t = Consumer(page_queue, img_queue)
        t.start()


if __name__ == '__main__':
    main()