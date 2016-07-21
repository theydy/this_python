from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, os, re
from collections import deque
from bs4 import BeautifulSoup



class qidian_spider(object):
    def __init__(self, target_url):
        self.browser = webdriver.PhantomJS()
        self.current_url = target_url
        self.js = "document.body.scrollTop=2100"
        self.content = {}
        self.url_list = deque([])
        self.filter = ["订阅VIP章节",  "返回书目"]

    def start_spider(self):
        time_long=time.time()
        self.get_url()
        print("章节url采集完毕，共{count}章等待下载".format(count=len(self.url_list)))
        while self.url_list:
            self.current_url = self.url_list.popleft()
            self.page_source()
            self.down_load()
            print("还剩{cont}章节等待下载.".format(cont=len(self.url_list)))
        self.browser.quit()
        print("共耗时: ", (time.time() - time_long)/ 60 )

    def get_url(self):
        self.browser = webdriver.PhantomJS()
        self.browser.get(self.current_url)
        WebDriverWait(self.browser, 10).until(lambda browser: browser.find_element_by_xpath("//*[@id='content']/div[6]/div[2]/ul/li[1]/a").is_displayed())
        self.soup = BeautifulSoup(self.browser.page_source, "html.parser")
        lis = self.soup.find_all(href=re.compile(".*qidian.com/BookReader.*"))
        for li in lis:
            if li.string.strip() not in self.filter:
                self.url_list.append(li.get("href"))

    def page_source(self):
        self.browser.get(self.current_url)
        self.browser.implicitly_wait(30)
        self.browser.execute_script(self.js)
        cont = 1
        while True:
            cont += 1
            try:
                WebDriverWait(self.browser, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "bookreadercontent"))
                )
                break
            except:
                time.sleep(1)
            finally:
                if cont == 20:
                    print("下载失败")
                    break

    def down_load(self):
        self.soup = BeautifulSoup(self.browser.page_source, "html.parser")
        self.content["title"] = self.soup.h1.text
        self.content["content"] = self.soup.find(id="chaptercontent").text
        with open(os.path.join(os.path.abspath(""), self.content["title"].replace("*", "_") + ".txt"), "w+") as f:
            f.write(self.content["content"])


if __name__ == "__main__":
    # qidian_url="http://read.qidian.com/BookReader/LYQM3SG7Sm9xo3Pbs2jtrw2.aspx"
    qidian_url = input("输入小说章节目录url: ")
    q = qidian_spider(qidian_url)
    q.start_spider()
