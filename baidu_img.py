import os
import re
import time
import urllib.request
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# base_url_part1和base_url_part2固定不变无需更改
base_url_part1 = 'https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=index&fr=&hs=0&xthttps=111111&sf=1&fmq=&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word='
base_url_part2 = '&oq=bagua&rsp=0'
# 检索关键字
search_query = '王灿'
# Chrome驱动程序在电脑中的位置
location_driver = 'C:/Users/HR/AppData/Local/Google/Chrome/Application/chromedriver.exe'

class Crawler:
    def __init__(self):
        self.url = base_url_part1 + search_query + base_url_part2

    # 启动Chrome浏览器驱动
    def start_brower(self):
        chrome_options = Options()
        chrome_options.add_argument("--disable-infobars")
        # 启动Chrome浏览器
        driver = webdriver.Chrome(executable_path=location_driver, chrome_options=chrome_options)
        # 最大化窗口 因为每一次爬取只能看到视窗内的图片
        driver.maximize_window()
        # 浏览器打开爬取页面
        driver.get(self.url)
        return driver

    def download_img(self, driver):
        t = time.localtime(time.time())
        # 定义文件夹的名字
        folder_name = str(t.__getattribute__("tm_year")) + "-" + str(t.__getattribute__("tm_mon")) + "-" + str(t.__getattribute__("tm_mday"))
        picpath = 'BaiduImg/{}'.format(folder_name)  # 下载到的本地目录
        # 路径不存在时创建一个
        if not os.path.exists(picpath):
            os.makedirs(picpath)
        # 记录下载过的图片地址，避免重复下载
        img_url_dict = {}
        count = 0
        # 当鼠标的位置小于最后的鼠标位置时,循环执行
        pos = 0
        # 此处可自己设置爬取范围
        for i in range(10):  
            # 每次下滚500
            pos += 500  
            js = "document.documentElement.scrollTop=%d" % pos
            driver.execute_script(js)
            time.sleep(2)
            # 获取页面源码
            html_page = driver.page_source
            # 利用Beautifulsoup4创建soup对象并进行页面解析
            soup = bs(html_page, "html.parser")
            # 通过soup对象中的findAll函数图像信息提取
            img_list = soup.findAll('img', {'src': re.compile(r'https:.*\.(jpg|png)')})
            # 遍历list中每一张图下载保存
            for img_url in img_list:
                if img_url['src'] not in img_url_dict:
                    target = '{}/{}.jpg'.format(picpath, count)
                    img_url_dict[img_url['src']] = ''
                    urllib.request.urlretrieve(img_url['src'], target)
                    count = count + 1

    def run(self):
        print("Start downloading...\n")
        driver = self.start_brower()
        self.download_img(driver)
        driver.close()
        print("Download has finished...\n")


if __name__ == '__main__':
    craw = Crawler()
    craw.run()
