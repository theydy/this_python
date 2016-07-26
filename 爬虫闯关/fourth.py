#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-07-26 16:11:15
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os
from bs4 import BeautifulSoup
import time
import requests
from selenium import webdriver



url = "http://www.heibanke.com/lesson/crawler_ex03/"
pw_url = "http://www.heibanke.com/lesson/crawler_ex03/pw_list/"
url_login = "http://www.heibanke.com/accounts/login"

class Spider():
	def __init__(self):
		self.browser = webdriver.PhantomJS()
		self.pw_list = {}
		self.list = []
		self.ans_pw = ""

	def start(self):
		time_log = time.time()
		self.login()
		self.get_password()
		self.sort_pw()
		self.browser.quit()
		print("time: ", time.time() - time_log)

	def sort_pw(self):
		self.list = sorted(int(item) for item in self.pw_list.keys())
		for x in self.list:
			print(x, self.pw_list[str(x)])
			self.ans_pw += self.pw_list[str(x)]
		print(self.ans_pw)
		self.browser.get(url)
		self.browser.find_element_by_name("username").send_keys("ss")
		self.browser.find_element_by_name("password").send_keys(self.ans_pw)
		self.browser.find_element_by_id("id_submit").click()
		time.sleep(1)
		print(self.browser.page_source)

	def login(self):
		data = {
			"username": "test",
			"password": "test123"
		}
		self.browser.get(url_login)
		self.browser.find_element_by_id("id_username").send_keys(data["username"])
		self.browser.find_element_by_id("id_password").send_keys(data["password"])
		self.browser.find_element_by_id("id_submit").click()
		time.sleep(1)

	def get_password(self):
		while True:
			if len(self.pw_list) >= 100:
				break
			print("now page ", len(self.pw_list))
			self.browser.get(pw_url)
			pos_list = [item.text for item in self.browser.find_elements_by_css_selector("td[title=password_pos]")]
			val_list = [item.text for item in self.browser.find_elements_by_css_selector("td[title=password_val]")]
			self.pw_list.update(zip(pos_list,val_list))





if __name__ == "__main__":
	print("begin:...")
	p = Spider()
	p.start()
