#!/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header

mail_host = 'smtp.163.com'
mail_usr = '13659879951@163.com'
mail_pass = 'JQKEKWBBNTCAEFBJ'
sender = '13659879951@163.com'
receivers = ['903637599@qq.com,13659879951@163.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

# 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
message = MIMEText('Python test', 'plain', 'utf-8')
message['From'] = sender # 发送者
message['To'] = Header("test", 'utf-8')  # 接收者

subject = 'Python test'
message['Subject'] = Header(subject, 'utf-8')

try:
    smtpObj = smtplib.SMTP()
    smtpObj.set_debuglevel(1)
    smtpObj.connect(mail_host, 25)
#    smtpObj = smtplib.SMTP_SSL(mail_host)
#    smtpObj.ehlo(mail_host)
    smtpObj.login(mail_usr, mail_pass)
    smtpObj.sendmail(sender, receivers, message.as_string())
    print("邮件发送成功")
except smtplib.SMTPException:
    print("Error: 无法发送邮件")
