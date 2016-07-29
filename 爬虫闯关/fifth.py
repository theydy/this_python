#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-07-27 19:24:48
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import time
from pytesseract import image_to_string
from PIL import Image
from urllib.request import urlretrieve, urlopen
import requests
from io import BytesIO


url = "http://www.heibanke.com/lesson/crawler_ex04/"
url_login = "http://www.heibanke.com/accounts/login"



class Fifth():
	def __init__(self):
		self.cont = 0
		self.wrong = 0

	def check(self, passwrod):
		self.captcha = self.browser.find_element_by_xpath("/html/body/div/div/div[2]/form/div[3]/img").get_attribute("src")

	def start(self):
		self.browser = webdriver.PhantomJS()
		data = {
			"username": "test",
			"password": "test123"
		}
		self.browser.get(url_login)
		self.browser.find_element_by_id("id_username").send_keys(data["username"])
		self.browser.find_element_by_id("id_password").send_keys(data["password"])
		self.browser.find_element_by_id("id_submit").click()
		time.sleep(1)
		for i in range(31):
			self.browser.get(url)
			self.browser.find_element_by_id("id_username").send_keys("ss")
			self.browser.find_element_by_id("id_password").send_keys(str(i))
			while True:
				self.check(i)
				try:
					img = Image.open(BytesIO(urlopen(self.captcha).read()))
					print("captcha ({i}): ".format(i=i), image_to_string(img))
					self.cont+=1
				except:
					self.browser.get(url)
					self.browser.find_element_by_id("id_username").send_keys("ss")
					self.browser.find_element_by_id("id_password").send_keys(str(i))
					print("image_to_string error")
				try:
					self.browser.find_element_by_id("id_captcha_1").send_keys(image_to_string(img))
					self.browser.find_element_by_id("id_submit").click()
					time.sleep(1)
					WebDriverWait(self.browser, 10).until(lambda browser: browser.find_element_by_tag_name("h3").is_displayed())
					if "ss" in self.browser.find_element_by_tag_name("h3").text:
						print(i, "success!")
						self.browser.quit()
						return 0
					elif self.browser.find_element_by_tag_name("h3").text != "验证码输入错误":
						print(i, self.browser.find_element_by_tag_name("h3").text)
						self.wrong+=1
						break
					print(i, self.browser.find_element_by_tag_name("h3").text)
				except:
					print("a error")


q = Fifth()
q.start()