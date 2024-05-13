#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2024/4/27 8:44
# Author    : smart
# @File     : send_email_base.py
# @Software : PyCharm
# 用于建立smtp连接
import smtplib
# 邮件需要专门的mime格式
from email.mime.text import MIMEText
# plain指普通文本格式邮件内容
msg = MIMEText("sjy是lyq的好大儿",'plain','utf-8')
# 发件人
msg['From'] = '3030181766@qq.com'
# 收件人
msg['To']='3030181766@qq.com'
# 邮件的标题
msg['Subject']='lyq美丽日记'

smtp = smtplib.SMTP_SSL('smtp.qq.com')
smtp.login('3030181766@qq.com','fahwrefuwteqddfe')
smtp.sendmail('3030181766@qq.com','3030181766@qq.com',msg.as_string())
smtp.quit()