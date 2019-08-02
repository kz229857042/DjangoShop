'''
这个代码是在指定的短信工具平台，帮助我们自动发送短信的一个脚本
本代码使用的是互易网站，全部数据基于互易网站
'''
import requests
#coding:utf-8
# 互易网站信息中的url
url='http://106.ihuyi.com/webservice/sms.php?method=Submit'

# 后面根据互易模板中的内容，填写自己的信息即可
account = "C85050877"
password = "9c14def972fa00acf877b04cc827fa8a"
mobile = "13331153360"
# 这个content的内容是发送模板，可以修改的是验证码的值，其他内容想要修改的话，需要花钱购买
content = "您的验证码是：201981。请不要把验证码泄露给其他人。"

#   定义请求的头部
headers ={
    'content-type':'application/x-www-form-urlencoded',
    'Accept':'text/plain'
}
# 定义数据
data = {
    'account':account,
    'password':password,
    'mobile':mobile,
    'content':content
}
# 发起数据请求
response = requests.post(url,headers=headers,data=data)