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
'''
if __name__ == '__main__':
    if send_mail(mailto_list,"hello","hello hello"):
        print "successed"
    else:
        print "failed"
'''

