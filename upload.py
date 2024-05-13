#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2024/4/29 15:08
# Author    : smart
# @File     : upload.py
# @Software : PyCharm
import requests
# rb,以只读的方式打开二进制文件
files = {"files":open("a.jpg","rb")}
# 发送post请求携带文件
response = requests.post("http://httpbin.org/post",files=files,timeout=5)
# 响应内容
print(response.text)