from bs4 import BeautifulSoup
import pymongo
import requests
import re
import time
from threading import Thread


client = pymongo.MongoClient("localhost", 27017)
db = client.douban_db
collection = db.book_collection


class Book(object):
    def __init__(self, title=None, title_e=None, author=None,
                score=None, comments=None):
        self.title = title
        self.title_e = title_e
        self.author = author
        self.score = score
        self.comments = comments


def d_book_spider(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    item_list = soup.find_all("tr", class_="item")
    for item in item_list:
        title = item.find("a", title=re.compile(".+"))
        title_e = item.find("span", style="font-size:12px;")
        author = item.find("p", class_="pl")
        score = item.find("span", class_="rating_nums")
        comments = item.find("span", class_="pl")
        title = title["title"] if title is not None else None
        title_e = title_e.text if title_e is not None else None
        author = author.text if author is not None else None
        score = score.text if score is not None else None
        reg = re.compile("\(\s+(\d+.+)\s+\)")
        comments = reg.match(comments.text).group(1) if comments is not None else None
        collection.insert_one({
            "title": title,
            "title_e": title_e,
            "author": author,
            "score": score,
            "comments": comments
        })


if __name__ == "__main__":
    time_begin = time.time()
    url_top250 = "https://book.douban.com/top250?start=%s"
    url_list = [url_top250 % (page * 25) for page in range(10)]
    thread_list = []
    for url in url_list:
        t = Thread(target=d_book_spider, name=url, args=(url,))
        thread_list.append(t)
    for t in thread_list:
        t.start()
    for t in thread_list:
        t.join()
    print("总用时： ", time.time() - time_begin)
    for book in collection.find():
        print(book)
    print(collection.find().count())
