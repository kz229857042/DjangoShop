import hashlib


from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect


from Store import models




# 定义密码加密
def setPassword(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    return  md5.hexdigest()


def base(request):
    return render(request,'store/blank.html')

def register(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        nickname = request.POST.get('nickname')
        if username and password:
            # user = models.Seller.objects.filter(username=username).first()
            models.Seller.objects.create(
                username=username,
                password=setPassword(password),
                nickname=nickname,
            )
            return HttpResponseRedirect('/Store/login')
    return render(request,'store/register.html')
# Create your views here.

def login(request):
    '''
    登陆功能，如果登录成功，则跳转到首页
    如果失败，则跳转到登录页
    '''
    response = render(request,'store/login.html')
    # 随意设置cookie 这个cookie就是为了保证是从登陆页面登陆的
    response.set_cookie('login_from','login_page')
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user_sql = models.Seller.objects.filter(username=username).first()
            if user_sql:
                # 对密码进行加密
                web_password = setPassword(password)
                # 获取cookie值
                cookies = request.COOKIES.get('login_from')
                # 判断 如果数据库密码与加密后的密码一致 并且cookie值也等于刚刚设置的cookie
                if user_sql.password == web_password and  cookies == 'login_page':
                    # 跳转到主界面
                    response = HttpResponseRedirect('/Store/index/')
                    # 并且再次设置cookie和session
                    response.set_cookie('username',username)
                    request.session['username'] = username
                    return response
    return response


def cookie_user(fun):
    def inner(request,*args,**kwargs):
        # 获取网页中的cookie 和session
        c_username = request.COOKIES.get('username')
        s_username = request.session.get('username')
        # 判断如果输入的存在，并且c_username == s_username
        if c_username and s_username and c_username == s_username:
            # 查询数据库  查看c_username 在不在数据库
            user_sql = models.Seller.objects.filter(username=c_username).first()
            if user_sql:
                # 返回页面
                return fun(request,*args,**kwargs)
        return HttpResponseRedirect('/Store/login/')
    return inner

@cookie_user
def index(request):
    return render(request,'store/index.html')