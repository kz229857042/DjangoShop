# import smtplib  # 登陆邮件服务器，进行邮件发送
# from email.mime.text import MIMEText  # 负责构建邮件格式
#
# subject = "Python群发邮箱实验"
# content = "这是一个实验内容，主要的要求就是如何使用python程序给各位群发右键，试一试"
# sender = "503492021@qq.com"
# recver = """806680775@qq.com,
# 1246761102@qq.com,
# 979180660@qq.com,
# 1160195048@qq.com,"""
#
# password = "aizsjtizdsykcaih"
#
# message = MIMEText(content, "plain", "utf-8")
# message["Subject"] = subject
# message["To"] = recver
# message["From"] = sender
#
# smtp = smtplib.SMTP_SSL("smtp.qq.com", 465)
# smtp.login(sender, password)
# smtp.sendmail(sender, recver.split(",\n"), message.as_string())
# smtp.close()



#<--------------------------------------------------------------测试重新练----------------------------------------------------------------------->
# 1、导入相应模块
import smtplib  # 登录邮件服务器，进行邮件发送
from email.mime.text import MIMEText # 负责构建邮箱格式

# 标题
subject = '这是个邮件的标题'
# 内容
content = '这是整个邮件的内容'
# 发送方
sender = '503492021@qq.com'
# 接收方
receiver = '''21130245@qq.com,
12351345@qq.com,
1245345343@qq.com,
4381233443@qq.com'''
# 这里的密码不是自己的账户密码，而是开启QQ邮箱的IMAP/SMTP时给与的唯一授权码
password = 'aizsjtizdsykcaih'
# 邮箱格式： 内容，字符串格式(提醒的就是plain)，编码格式
message = MIMEText(content,'plain','utf-8')
message['Subject'] = subject
# 发送给--
message['To'] = receiver
# 从哪里发--
message['From'] = sender
# 这是登录邮件服务器，第一个参数是邮件服务器的ip，第二个是端口号
smtp = smtplib.SMTP_SSL('smtp.qq.com',465)
# 使用login方式验证序列
smtp.login(sender,password)
#  receiver.split(',\n')是为了将字符串类型变成列表类型，且将没有用的数据切割
# 注意：这里的receiver传递的数据必须是列表类型，即使只有一个数据
smtp.sendmail(sender,receiver.split(',\n'),message.as_string())
# 关闭smtp服务
smtp.close()
