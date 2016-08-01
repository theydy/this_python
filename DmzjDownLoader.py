# -*- coding:utf-8 -*-


import requests
import os
from bs4 import BeautifulSoup
from selenium import webdriver


class DmzjDownloader(object):
    def __init__(self, url):
        self.browser = webdriver.PhantomJS()
        self.page_list = []
        self.url = url
        self.js = "for(var i=0; i<%s; i++){ next_img(this); }"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0",
            "Host": "images.dmzj.com",
            "Referer": ""
        }
        self.headers["Referer"] = self.url.split("#")[0]

    def start(self):
        self.get_page_source()
        self.get_image_source()
        self.begin_download()
        self.browser.quit()

    def get_page_source(self):
        print("开始...")
        self.browser.get(self.url)
        source = self.browser.page_source
        self.soup = BeautifulSoup(source, "html.parser")
        print("page_source 得到...")

    def get_image_source(self):
        self.page_list = self.soup.find_all("option")
        self.title = self.soup.title.text.split("-")[0]
        self.len = len(self.page_list)
        self.browser.execute_script(self.js % (self.len - 2))
        self.cookies = self.browser.get_cookies()
        for cookie in self.cookies:
            self.headers[cookie["name"]] = cookie["value"]
        print("图片cookie 得到...")

    def begin_download(self):
        path = os.path.join(os.getcwd(), self.title)
        if not os.path.exists(path):
            os.makedirs(path)
        for page in self.page_list:
            print("正在下载{num}".format(num=page.text))
            page_path = os.path.join(path, page.text + page["value"][-4:])
            data = requests.get(page["value"], headers=self.headers, stream=True)
            with open(page_path, "wb") as f:
                f.write(data.content)

if __name__ == "__main__":
    url_detail = input("输入想要下载的漫画的第一页url: ")
    # url_detail = "http://manhua.dmzj.com/magi/23586.shtml#@page=1"
    d = DmzjDownloader(url_detail)
    d.start()

