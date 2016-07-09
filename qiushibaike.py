# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup

url = "http://www.qiushibaike.com/hot/"
page_num = 3
time = 0
userAgent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"


headers = {
    "User-Agent": userAgent
}

def get_url_content(url,page_num=3):
    current_page = 1
    now_url = url
    while current_page <= page_num:
        print("page :", current_page)
        print(now_url)
        r = requests.get(now_url, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")
        articles = soup.find_all("div", {"class": ["article", "block"]})
        num = 1
        for article in articles:
            content = article.find("div", {"class": "content"}).text
            print(num, content)
            num += 1
            if article.find("div", {"class": "thumb"}):
                thumb = article.find("div", {"class": "thumb"})
                img = thumb.find("img")
                print(img["src"])
        if current_page == 1:
            time = soup.select(".pagination > li > a")[0]["href"].split("=")[1]
        current_page += 1
        now_url = url + "page/" + str(current_page) + "/?s=" + time





if __name__ == "__main__":
    print("=======糗事百科爬虫=======")
    page_num = input("请输入爬取页数(默认为3页): ")
    print("开始爬取:")
    get_url_content(url, int(page_num))
    print("爬取结束")
