#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
邮件发送脚本 - 用于定时任务通知
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
import sys

# QQ邮箱配置
SMTP_SERVER = "smtp.qq.com"
SMTP_PORT = 465
SENDER_EMAIL = "25932437@qq.com"
SENDER_PASSWORD = os.environ.get("EMAIL_SMTP_PASSWORD", "vmwtteoqvlwfbgfj")  # 授权码
SENDER_NAME = "OpenClaw 机器人"

def send_email(to_email, subject, content, content_type="plain"):
    """
    发送邮件
    
    Args:
        to_email: 收件人邮箱
        subject: 邮件主题
        content: 邮件内容
        content_type: "plain" 或 "html"
    
    Returns:
        (success, message)
    """
    try:
        # 创建邮件对象
        msg = MIMEMultipart()
        msg['From'] = formataddr([SENDER_NAME, SENDER_EMAIL])
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # 添加正文
        msg.attach(MIMEText(content, content_type, 'utf-8'))
        
        # 发送
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, [to_email], msg.as_string())
        
        return True, "发送成功"
    except Exception as e:
        return False, str(e)

def main():
    """命令行入口"""
    if len(sys.argv) < 4:
        print("用法: python3 send_email.py <收件人> <主题> <内容>")
        print("      python3 send_email.py <收件人> <主题> <内容> --html")
        sys.exit(1)
    
    to_email = sys.argv[1]
    subject = sys.argv[2]
    content = sys.argv[3]
    content_type = "html" if "--html" in sys.argv else "plain"
    
    success, message = send_email(to_email, subject, content, content_type)
    
    if success:
        print(f"✅ 邮件发送成功: {to_email}")
    else:
        print(f"❌ 邮件发送失败: {message}")
        sys.exit(1)

if __name__ == "__main__":
    main()
