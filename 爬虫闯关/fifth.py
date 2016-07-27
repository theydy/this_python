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
url_head ="http://www.heibanke.com"
url_login = "http://www.heibanke.com/accounts/login"


cont = 0
wrong = 0

def check(passwrod):
	captcha = browser.find_element_by_xpath("/html/body/div/div/div[2]/form/div[3]/img").get_attribute("src")
	# urlretrieve(captcha, "captcha.png")

def start():
	browser = webdriver.PhantomJS()
	browser.quit()
	data = {
		"username": "test",
		"password": "test123"
	}
	browser.get(url_login)
	browser.find_element_by_id("id_username").send_keys(data["username"])
	browser.find_element_by_id("id_password").send_keys(data["password"])
	browser.find_element_by_id("id_submit").click()
	time.sleep(1)
	for i in range(31):
		browser.get(url)
		while True:
			check(i)
			browser.find_element_by_id("id_username").send_keys("ss")
			browser.find_element_by_id("id_password").send_keys(str(i))
			try:
				img = Image.open(BytesIO(urlopen(captcha).read()))
				print("captcha ({i}): ".format(i=i), image_to_string(img))
			except:
				browser.get(url)
				print("image_to_string error")
			cont+=1
			try:
				browser.find_element_by_id("id_captcha_1").send_keys(image_to_string(img))
				browser.find_element_by_id("id_submit").click()
				time.sleep(1)
				WebDriverWait(browser, 10).until(lambda browser: browser.find_element_by_tag_name("h3").is_displayed())
				if browser.find_element_by_tag_name("h3").text != "验证码输入错误":
					print(i, browser.find_element_by_tag_name("h3").text)
					wrong+=1
					break
				elif "ss" in browser.find_element_by_tag_name("h3").text:
					print(i, "success!")
					browser.quit()
					return 0
				print(i, browser.find_element_by_tag_name("h3").text)
			except:
				print("a error")



start()
print("一共{cont}张图片下载成功， 正确率{ans}".format(cont=cont, ans=((cont-wrong)/cont)))
# img = Image.open("captcha.png")
# img = img.convert("L")
# print(image_to_string(img))