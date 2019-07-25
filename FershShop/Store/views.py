import hashlib


from django.shortcuts import render
from django.core.paginator import Paginator
from django.shortcuts import HttpResponseRedirect



from Store import models




# 定义密码加密
def setPassword(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    return  md5.hexdigest()

# 基本页
def base(request):
    return render(request,'store/base.html')
# 注册界面
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
# 登录界面

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
                    # 并且再次设置cookie和session(增加一个user_id用来查询)
                    response.set_cookie('username',username)
                    response.set_cookie('user_id',user_sql.id)
                    request.session['username'] = username
                    # 增加校验 校验是否有店铺
                    store = models.Store.objects.filter(user_id=user_sql.id).first()
                    # 如果有店铺，则对cookie里上传店铺id
                    if store:
                        response.set_cookie('has_store',store.id)
                    # 没有，则上传空
                    else:
                        response.set_cookie('has_store','')
                    return response
    return response

# 主界面装饰器，用于验证cookie
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
# 主界面
def index(request):
    '''
    添加检查账号是否存在店铺的逻辑
    :param request:
    :return:
    '''
    # 查询当前用户是谁(现在问题，获取不到账户(在index界面可以查询到COOKIES信息))
    user_id = request.COOKIES.get('user_id')
    # print(user_id)
    if user_id:
        user_id = int(user_id)
    else:
        user_id=0
    # 通过用户查询店铺是否存在（店铺和用户通过用户的id进行关联）
    store = models.Store.objects.filter(user_id = user_id).first()
    if store:
        has_store=1
    else:
        has_store=''
    return render(request,'store/index.html',{'has_store':has_store})

# 添加店铺
@cookie_user
def register_store(request):
    # 查询店铺类型的所有信息
    type_list = models.StoreType.objects.all()
    # 判断数据类型
    if request.method=='POST':
        # 接收post数据
        post_data = request.POST
        # 将数据添加到数据库 因为由多对多数据，所以要注意
        store_name = post_data.get('store_name')
        store_description = post_data.get('store_description')
        store_phone = post_data.get('store_phone')
        store_money = post_data.get('store_money')
        store_address = post_data.get('store_address')

        # 通过cookie 获取得到的user_id
        # print(request.COOKIES.get('user_id'))
        user_id = int(request.COOKIES.get('user_id'))
        # 通过request.post得到类型，但是是一个列表
        # 问题1 获取的数据是['蛋奶', '水果', '生鲜']，获取不到索引
        # 以解决，在前端代码加入t.id  给予id值，这样返回的就是索引了
        type_lists = post_data.getlist('store_type')
        # 通过request.FILES 得到    图片格式的得到方式就是FILES
        store_logo = request.FILES.get('store_logo')

        # 保存非多对多的数据
        # 定义变量
        store = models.Store()
        store.store_name = store_name
        store.store_description = store_description
        store.store_phone = store_phone
        store.store_money = store_money
        store.store_address = store_address
        store.user_id = user_id
        store.store_logo = store_logo # 在django1.8之后的图片可以直接保存，django的人员已经将其打包好，在1.8之前需要手写
        store.save()

        # 保存多对多数据(需要再次保存数据)
        for i in type_lists:# 循环type列表，得到类型的id
            # 查询数据类型
            store_type = models.StoreType.objects.get(id=i)
            # 添加到类型字段，多对多的映射表  是实例化的对象的
            store.type.add(store_type)
        store.save()
        # 当添加完店铺，我们需要在将cookie的值赋给首页
        response = HttpResponseRedirect('/Store/index/')
        response.set_cookie('has_store',store.id)
        return response

    return render(request,'store/register_store.html',locals())


# 商品的增加
@cookie_user
def add_goods(request):
    if request.method=='POST':
        good_name = request.POST.get('good_name')
        good_price = request.POST.get('good_price')
        good_number = request.POST.get('good_number')
        good_description = request.POST.get('good_description')
        good_date = request.POST.get('good_date')
        good_safeDate = request.POST.get('good_safeDate')
        good_store = request.COOKIES.get('has_store')
        good_image = request.FILES.get('good_image')

        # 保存数据库 处理普通关系
        goods = models.Goods()
        goods.good_name=good_name
        goods.good_price=good_price
        goods.good_number=good_number
        goods.good_description=good_description
        goods.good_date=good_date
        goods.good_safeDate=good_safeDate
        goods.good_image=good_image
        goods.save()

        # 保存多对多数据
        goods.store_id.add(
            models.Store.objects.get(id= int(good_store))
        )
        goods.save()
        return HttpResponseRedirect('/Store/list_goods/')
    return render(request,'store/add_goods.html')

# 商品列表的展示
@cookie_user
def list_goods(request):
    # 获取keywords的值
    keywords = request.GET.get('keywords','')
    # 获取分页
    page_num = request.GET.get('page_num',1)
    # 查询店铺
    store_id = request.COOKIES.get('has_store')
    store = models.Store.objects.get(id=int(store_id))
    #   判断是否存在，如果存在进行模糊查询
    if keywords:
        # 模糊查询 good_name 是要查询数据库的关键词 ，__contains  是模糊查询
        list_goods = store.goods_set.filter(good_name__contains=keywords)
    else:
        list_goods =store.goods_set.all()
    # 对list_goods的数据进行分页，每3条数据为一页
    paginator = Paginator(list_goods,3)
    p = int(page_num)
    page = paginator.page(p)
    start = p-3
    end = p+2
    if start<=0 and end <=5:
        start = 0
        end = 5
    page_range = paginator.page_range[start:end]

    # 由于不是所有内容都返回，所以不用locals，而选择字符串
    return render(request,'store/list_goods.html',{'page':page,'page_range':page_range,'keywords':keywords})

# 商品列表的删除
def del_goods(request):
    # 获取点击删除的那个按键的id
    pass


# 商品详情
@cookie_user
def details_goods(request,good_id):
    # 获取商品信息
    goods_data = models.Goods.objects.filter(id = good_id).first()
    return render(request,'store/details_goods.html',locals())

# 修改商品
@cookie_user
def update_goods(request,good_id):
    goods_data = models.Goods.objects.filter(id=good_id).first()
    if request.method == 'POST':
        good_name = request.POST.get('good_name')
        good_price = request.POST.get('good_price')
        good_number = request.POST.get('good_number')
        good_description = request.POST.get('good_description')
        good_date = request.POST.get('good_date')
        good_safeDate = request.POST.get('good_safeDate')
        good_image = request.FILES.get('good_image')

        # 保存数据库 处理普通关系
        goods = models.Goods.objects.get(id=int(good_id))
        goods.good_name = good_name
        goods.good_price = good_price
        goods.good_number = good_number
        goods.good_description = good_description
        goods.good_date = good_date
        goods.good_safeDate = good_safeDate
        if good_image:
            goods.good_image = good_image
        goods.save()
        return HttpResponseRedirect('/Store/dg/%s'%good_id)
    return render(request,'store/update_goods.html',locals())