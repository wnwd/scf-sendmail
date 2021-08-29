import json
import os
import smtplib
import time
from email.mime.text import MIMEText
from email.utils import formataddr
def main(event, context):

    send_key = os.environ.get('send_key')          # 设置的send_key
    core_content = event.get('body')               # 邮件的主要参数
    core_body = json.loads(core_content)
    
    get_send_key = core_body.get("send_key")       # 获取到的send_key
    mail_acct = core_body.get("mail_acct")         # 发件人邮箱账号
    mail_paswd = core_body.get("mail_paswd")       # 发件人邮箱密码
    mail_to = core_body.get("mail_to")             # 收件人邮箱账号
    smtp_server = core_body.get("smtp_server")     # 设置的smtp server
    smtp_port = core_body.get("smtp_port")         # 设置的smtp port
    subject = core_body.get("subject")             # 邮件的主题
    content = core_body.get("content")             # 邮件的正文
    from_nikename = core_body.get("from_nikename") # 显示的发件人昵称
    to_nikename = core_body.get("to_nikename")     # 显示的收件人昵称
    send_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def mail():
        ret = True
        try:
            msg = MIMEText(content, 'plain', 'utf-8')
            msg['From'] = formataddr([from_nikename, mail_acct])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
            msg['To'] = formataddr([to_nikename, mail_to])        # 括号里的对应收件人邮箱昵称、收件人邮箱账号
            msg['Subject'] = subject                              # 邮件的主题，也可以说是标题
            server = smtplib.SMTP_SSL(smtp_server, smtp_port)     # 发件人邮箱中的SMTP服务器，SMTP端口
            server.login(mail_acct, mail_paswd)                   # 括号中对应的是发件人邮箱账号、邮箱密码
            server.sendmail(mail_acct, [mail_to, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            server.quit()  # 关闭连接
            
        except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
            ret = False
        return ret

    if get_send_key == send_key:
        ret = mail()
    else:
        ret = False
        print("send_key ERROR!")

    if ret:
        data = { '响应' : "邮件发送成功", '发送时间':send_time, '邮件主题' : subject, '邮件正文' : content}
        body = json.dumps(data, sort_keys=True, indent=2, separators=(',', ': '), ensure_ascii=False)
        print("Sms send success!")
        resp = {
            "isBase64Encoded": False,
            "send_date": send_time,
            "statusCode": 200,
            "headers": {"Content-Type":"application/json; charset=UTF-8"},
            "body": body
        }
        return(resp)
        
    else:
        data = { '响应' : "邮件发送失败", '发送时间':send_time, '邮件主题' : subject, '邮件正文' : content}
        body = json.dumps(data, sort_keys=True, indent=2, separators=(',', ': '), ensure_ascii=False)
        resp = {
            "isBase64Encoded": False,
            "send_date": send_time,
            "statusCode": 300,
            "headers": {"Content-Type":"application/json; charset=UTF-8"},
            "body": body
        }
        return(resp)
