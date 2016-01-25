import smtplib
from email.mime.text import MIMEText
mailto_list=["249776215@qq.com"]
mail_host="smtp.sina.com"
mail_user="qianjing7744@sina.com"
mail_pass="conan88"
mail_postfix="sina.com"

def send_mail(to_list,sub,content):
    me="hello"+"<"+mail_user+">"
    msg = MIMEText(content,_subtype='plain',_charset='gb2312')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        server = smtplib.SMTP()
        server.connect(mail_host)
        server.login(mail_user,mail_pass)
        server.sendmail(me, to_list, msg.as_string())
        server.close()
        return True
    except Exception, e:
        print str(e)
        return False

if __name__ == '__main__':
    if send_mail(mailto_list,"hello","hello world"):
        print "successed"
    else:
        print "failed"

'''
# -*- coding: cp936 -*-
'''
发送带附件邮件
小五义：http://www.cnblogs.com/xiaowuyi
'''

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

#创建一个带附件的实例
msg = MIMEMultipart()

#构造附件1
att1 = MIMEText(open('d:\\abc.pptx', 'rb').read(), 'base64', 'gb2312')
att1["Content-Type"] = 'application/octet-stream'
att1["Content-Disposition"] = 'attachment; filename="abc.pptx"'#这里的filename可以任意写，写什么名字，邮件中显示什么名字
msg.attach(att1)


#加邮件头
msg['to'] = '249776215@qq.com'
msg['from'] = 'qianjing7744@sina.com'
msg['subject'] = 'hello world'
#发送邮件
try:
    server = smtplib.SMTP()
    server.connect('smtp.sina.com')
    server.login('qianjing7744@sina.com','conan88')#XXX为用户名，XXXXX为密码
    server.sendmail(msg['from'], msg['to'],msg.as_string())
    server.quit()
    print '发送成功'
except Exception, e:
    print str(e)

'''