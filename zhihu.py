import  time, json, re
import requests
from PIL import Image
from requests.utils import cookiejar_from_dict
from http.cookiejar import LWPCookieJar
from bs4 import BeautifulSoup



class Login(object):
	def __init__(self):
		self._session = requests.session()

		self._headers = {
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
			"Host": "www.zhihu.com",
			"Origin": "http://www.zhihu.com",
			"Referer": "http://www.zhihu.com/"
		}
		self._captcha = ""

	def login(self, data, url=None):
		if re.match("^1{0-9}{10}$", data["account"]):
			account_type = "phone_num"
			url_login = url or "https://www.zhihu.com/login/phone_num"
		elif re.match(".+@.+\.com", data["account"]):
			account_type = "email"
			url_login = url or "https://www.zhihu.com/login/email"
		else:
			print("账号类型错误")

		self._data = {
			"_xsrf": self._session.cookies.get("_xsrf", ""),
			"password": data.get("password", ""),
			"captcha": self._captcha,
			"remember_me": "true",
			account_type: data.get("account", "")
		}
		self._headers["X-Xsrftoken"] = self._session.cookies.get("_xsrf", "")
		self._r = self._session.post(url_login, data=self._data, headers=self._headers)
		if self._r.status_code != 200:
			print("提交数据失败")
		else:
			self._response_json = json.loads(self._r.content.decode("utf-8"))
			if self._response_json["r"] == 0:
				print(self._response_json["msg"])
				# save cookies
				lwpcookie = LWPCookieJar('cookie.txt')
				cookiejar_from_dict({ c.name: c.value for c in self._session.cookies}, lwpcookie)
				lwpcookie.save(ignore_discard=True)
			else:
				if self._response_json["errcode"] in [1991829, 100005]:
					print(self._response_json["msg"])
					self.get_captcha()
					self.login()
				else:
					print("未知的错误")

	def get_captcha(self, url=None):
		url_captcha = url or "https://www.zhihu.com/captcha.gif"
		params = {
			"r": str(int(time.time()*1000)),
			"type": "login"
		}
		self._r = self._session.get(url_captcha, params=params, headers=self._headers)
		if self._r.status_code != 200:
			print("验证码请求失败")
		captcha_name = "captcha.png"
		with open(captcha_name, "wb") as f:
			f.write(self._r.content)
		print("验证码下载成功, 正在打开验证码...")

		# 打开验证码图片
		Image.open(captcha_name).show()
		self._captcha = input("请输入验证码: ")
		return self._captcha

	def login_xsrf(self, url=None):
		url_xsrf = url or "http://www.zhihu.com"
		self._r = self._session.get(url_xsrf, headers=self._headers)
		if self._r.status_code != 200:
			print(self._r.status_code)
			print("访问知乎失败")


if __name__ == "__main__":
	data={
		"password": "xxx",
		"account": "xxx"
	}
	login = Login()
	login.login_xsrf()
	login.get_captcha()
	login.login(data=data)

