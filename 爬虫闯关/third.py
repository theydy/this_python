#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-07-06 19:01:01
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os
import re
import urllib
import urllib.request
import time
import requests
from selenium import webdriver
from collections import deque
from bs4 import BeautifulSoup


url='http://www.heibanke.com/lesson/crawler_ex02/'
url_login='http://www.heibanke.com/accounts/login/?next=/lesson/crawler_ex02/'

browser = webdriver.Chrome()
browser.get(urll)
time.sleep(1)
browser.find_element_by_id('id_username').send_keys('test')
browser.find_element_by_id('id_password').send_keys('test123')
browser.find_element_by_id('id_submit').click()
time.sleep(1)
cont = 0
while cont<30:
	browser.get(url)
	time.sleep(1)
	browser.find_element_by_name('username').send_keys('ydy')
	browser.find_element_by_id('id_password').send_keys(str(cont))
	browser.find_element_by_id('id_submit').click()
	time.sleep(1)
	if 'ydy' in browser.page_source:
		print('password = ',cont)
		break
	cont+=1




