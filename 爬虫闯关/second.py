#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-07-06 10:39:48
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os
import urllib.request
import urllib
from bs4 import BeautifulSoup
import re
from collections import deque



import requests


url='http://www.heibanke.com/lesson/crawler_ex01/'



params = {
	'username' : 'ydy',
	'password' : 0
}


for num in range(30):
	params['password'] = num
	r = requests.post(url,data=params)
	soup = BeautifulSoup(r.text,'html.parser')
	string = soup.h3.string
	if params['username'] in string:
		print(num, string)
		break

