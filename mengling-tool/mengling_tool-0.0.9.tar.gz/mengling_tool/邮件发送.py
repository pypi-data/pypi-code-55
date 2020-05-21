# smtplib 用于邮件的发信动作
import smtplib
from email.mime.text import MIMEText
# email 用于构建邮件内容
from email.header import Header

config = {
    '发信方': '1650444933@qq.com',
    '授权码': 'maufoyvvihkmfcdh',
    '发信服务器': 'smtp.qq.com',
    '参数格式': 'plain',
    '编码': 'utf-8',
}


def send(title, context, mane_mail='1321443305@qq.com'):
    # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
    msg = MIMEText(context, config['参数格式'], config['编码'])

    # 邮件头信息
    msg['From'] = Header(config['发信方'])
    msg['To'] = Header(mane_mail)
    msg['Subject'] = Header(title)

    # 开启发信服务，这里使用的是加密传输
    server = smtplib.SMTP_SSL()
    server.connect(config['发信服务器'], 465)
    # 登录发信邮箱
    server.login(config['发信方'], config['授权码'])
    # 发送邮件
    server.sendmail(config['发信方'], mane_mail, msg.as_string())
    # 关闭服务器
    server.quit()
