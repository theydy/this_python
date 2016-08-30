#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-08-30 18:36:05
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os, requests
from bs4 import BeautifulSoup


def download_video_for_html5(aid, title):
    headers = {
        "Host": "www.bilibili.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
    }
    bili = {
        "img": "",
        "comment": "",
        "cid": "",
        "src": ""
    }
    url = "http://www.bilibili.com/m/html5?aid=%s&page=1" % aid
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        json_content = r.json()
        try:
            if json_content['code'] == -500:
                print("api调用失败, aid正确吗?")
            return
        except:
            pass
        bili['img'] = json_content["img"]
        bili['comment'] = json_content["cid"]
        bili['cid'] = json_content["cid"][-11:-4]
        bili['src'] = json_content["src"]
    else:
        print("无法获得json数据 status_code=>", r.status_code)
        return
    
    path = os.path.join(os.getcwd(), title + ".mp4")
    if not os.path.exists(path):
        print("开始下载...")
        r = requests.get(bili['src'])
        with open(path, "wb") as f:
            f.write(r.content)
        print("done...")
    else:
        print("视频已存在")


def get_title(aid):
    url = "http://www.bilibili.com/video/av%s/" % aid
    headers = {
        "Referer": "http://www.bilibili.com/",
        "Host": "www.bilibili.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
    }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    return soup.title.string.split("_")[0]



if __name__ == "__main__":

    # aid = "6083521"
    aid = input("请输入视频av号: ")
    title = get_title(aid)
    # print(title)
    download_video_for_html5(aid, title)

