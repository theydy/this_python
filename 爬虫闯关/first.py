#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-07-06 10:38:17
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import urllib.request
import urllib
from bs4 import BeautifulSoup
import requests
import re
from collections import deque

url='http://www.heibanke.com/lesson/crawler_ex00/'


queue = deque()
queue.append("")
vis = set()

while queue:
	link = url + queue.popleft()
	if link not in vis:
		print(link)
		vis.add(link)
		r = requests.get(link)
		soup = BeautifulSoup(r.text,"html.parser")
		h3 = soup.find_all('h3')
		new_key = re.search('\D*(\d*)\D*',str(h3[0].string)).group(1)
		queue.append(new_key)
	else:
		continue
	print('ok')
















