import time
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import HttpResponseRedirect
from alipay import AliPay
from Buyer.models import *
from Store.models import *
from Store.views import setPassword


# 思路
# 1、购物车需要创建一个新表，用于存储用户加入购物车的商品，里面有订单号，用户id，商品名称，商品单位，商品价格，商品数量，小计，状态（当确认购买后修改状态），时间（默认为支付时间，不需要修改）
# 在用户中心的全部订单中也会查询新表，通过订单号显示，查询商品
# 2、在收获地址中，也需要创建一个新表，这个表用于存储用户的收货信息，与用户表为外键关联，一对多关系，里面有收件人，详细信息，邮编，手机



# base 基础页
def base(request):
    return render(request, 'buyer/base.html')

# 注册页
def register(request):
    #如果请求为post
    if request.method == 'POST':
        # 获取注册页信息
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        cpassword = request.POST.get('cpwd')
        email = request.POST.get('email')
        # 如果四个信息都存在（问题一：应查询输入的数据与数据库中的账户是否有相同的）
        if username and password and cpassword and email:
            # 并且密码和重复密码一样
            if setPassword(password) == setPassword(cpassword):
                # 保存数据
                buyer = Buyer()
                buyer.username = username
                buyer.password = setPassword(password)
                buyer.email = email
                buyer.save()
                return HttpResponseRedirect('/Buyer/login/')
    return render(request, 'buyer/register.html')

# 登录页面
def login(request):
    # 如果请求方式为post 那么获取相关数据
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        if username and password:
            user = Buyer.objects.filter(username=username).first()
            # 对比数据库密码与输入的密码是否一致
            if user and setPassword(password) == user.password:
                response = HttpResponseRedirect('/Buyer/index/')
                # 设置cookie和session  这里注意 cookie是用response，session用request
                response.set_cookie('username', username)
                request.session['username'] = username
                # 为了以后的方便，加入id认证
                response.set_cookie('user_id', user.id)
                return response
    return render(request, 'buyer/login.html')

# 定义身份验证
def set_cookie(fun):
    def inner(request, *args, **kwargs):
        # 获取网页中的cookie 和session
        c_username = request.COOKIES.get('username')
        s_username = request.session.get('username')
        # 判断如果输入的存在，并且c_username == s_username
        if c_username and s_username and c_username == s_username:
            # 查询数据库  查看c_username 在不在数据库
            user_sql = Buyer.objects.filter(username=c_username).first()
            if user_sql:
                # 返回页面
                return fun(request, *args, **kwargs)
        return HttpResponseRedirect('/Buyer/index/')
    return inner
# 创建主装饰器，用于验证cookie
# def cookie_user(fun):
#     def inner(request,*args,**kwargs):
#         c_user = request.COOKIES.get('username')
#         s_user = request.session.get('username')
#         if c_user and s_user and c_user==s_user:
#             return fun(request,*args,**kwargs)
#         else:
#             return HttpResponseRedirect('/Buyer/login/')
#     return inner


def logout(request):
    response = HttpResponseRedirect('/Buyer/index/')
    # 删除所有的cookie和session
    for key in request.COOKIES:
        # 循环删除所有cookie
        response.delete_cookie(key)
    del request.session['username']
    return response


def index(request):
    # 创建一个列表，用来存储一个结果
    result_list = []
    # 查询所有商品类型
    goods_type_list = GoodsType.objects.all()
    # 循环所有类型
    for i in goods_type_list:
        goodsList = i.goods_set.values()[:4]  # 查询前四条数据
        if goodsList:
            goodsType = {
                'id': i.id,
                'name': i.name,
                'description': i.description,
                'picture': i.picture,
                'goods_list': goodsList
            }  # 构建输出结果
            # 查询类型当中有数据的数据
            result_list.append(goodsType)  # 将有数据的数据放入到result_list
    return render(request, 'buyer/index.html', locals())


def goods_list(request):
    '''
    前台列表页
    :param request:
    :return:
    '''
    # 定义一个列表用于存储结果
    goodsList = []
    # 获取类型id
    type_id = request.GET.get('type_id')
    # 通过类型id 可以获取到类型
    goods_type = GoodsType.objects.filter(id=type_id).first()
    # 如果类型存在
    if goods_type:
        # 则通过商品外键获取商品列表
        goodsList = goods_type.goods_set.filter(good_state=1)
    return render(request, 'buyer/goods_list.html', locals())


@set_cookie
# 详情页
def detail(request):
    # 获取详情页的商品id
    good_id = request.GET.get('good_id')
    if good_id:
        # 获取商品id所对应的值
        goodsList = Goods.objects.filter(id=good_id).first()
        if goodsList:
            return render(request, 'buyer/detail.html', locals())
    # 通过商品ID可以获取到商品信息
    return render(request, 'buyer/detail_null.html')


# def cart(request):
#     # 定义一个空列表，用于存储购物车的商品  这个方案行不通，每次调用，空列表都刷新
#     # 方案2 在数据库里面创建一个临时表，用于存放加入购物车的商品，当支付成功以后，清空表格数据
#     user_id = request.COOKIES.get('user_id')
#     if not user_id:
#         return HttpResponseRedirect('/Buyer/cart_hint/')
#     else:
#         # 获取商品ID
#         good_id = request.GET.get('good_id')
#         if good_id:
#             # 将购买商品的id放入到列表中
#             # 获取get中的访问前页面
#             lase_form = request.META.get('HTTP_REFERER')
#             return HttpResponseRedirect(lase_form)
#             #查询商品列表
#             goods_list = Goods.objects.filter(id=good_id)
#             #前端通过循环，将商品信息一一展示到页面上
#         else:
#             return render(request,'buyer/cart_null.html')
#     return render(request,'buyer/cart.html',locals())
# 定义自动生成订单数据
def setOrderId(user_id, good_id, store_id):
    '''
    设置订单编号
    时间+用户id+商品的id+商铺+id
    :param request:
    :return:
    '''
    strtime = time.strftime('%Y%m%d%H%M%S', time.localtime())
    return strtime + str(user_id) + str(good_id) + str(store_id)

from django.db.models import Sum

# 购物车
def cart(request):
    # 获取登录用户的cookie（user_id）
    user_id = request.COOKIES.get('user_id')
    # 如果值不存在，则证明没登录
    if not user_id:
        return HttpResponseRedirect('/Buyer/cart_hint/')
    else:
        # 通过user_id 将Cart购物车中的数据提取出来
        goods_list = Cart.objects.filter(user_id=user_id)
        if request.method=='POST':
            # 获取POST请求来的数据
            post_data = request.POST
            # 定义一个列表，用于存储前端传递来的商品
            cart_data = []
            # <-----------------------普通查询------------------->
            # # 循环遍历post_data，查询出里面的key和value
            # for k,v in post_data.items():
            #     # 判断，如果key值中的前面是以good_ 开头的，则获取
            #     if k.startswith('good_'):
            #         cart_data.append(Cart.objects.get(id=int(v)))
            # # 获取提交过来的数据的总数据
            # good_count = len(cart_data)
            # # 订单的总价  先查询出每一个商品的总价格，然后在通过循环，查出所有人的，最后求和
            # good_total = sum([int(i.good_total) for i in cart_data])
            #<-----------------------聚类查询--------------------->
            # 1、查询到购物车中的商品的id号
            for k,v in post_data.items():
                # 筛选post_data的数据key值是以good_ 开头的数据
                if k.startswith('good_'):
                    cart_data.append(int(v))
            # 2、使用in方法进行范围的规定，然后使用Sum方法进行计算
            # 查询cart_data的长度
            good_count = len(cart_data)
            # 通过id 将数据中的good_total提取出来并求和  获取到的值为{'good_total__sum': 求的和的数值}
            good_total = Cart.objects.filter(id__in = cart_data).aggregate(Sum('good_total'))
            # 保存订单 先保存订单表，在保存订单详情表，因为订单详情表有外键为订单表
            order = Order()
            order.order_id = setOrderId(user_id,good_count,1)
            order.good_count = good_count
            order.order_user = Buyer.objects.get(id=user_id)
            order.order_price = good_total['good_total__sum']
            order.order_status = 1
            order.save()

            # 保存订单详情表  因为订单详情表的数据不是一条，而是一个序列，所以需要通过循环遍历，挨个添加
            # 前面已经将所有数据放入到cart_data 中了，所以现在只需要循环遍历即可
            for detail in cart_data:
                d = Cart.objects.filter(id=detail).first()
                orderDetail = OrderDetail()
                orderDetail.order_id = order # 这是一条订单数据
                orderDetail.good_id = d.good_id
                orderDetail.good_name = d.good_name
                orderDetail.good_price = d.good_price
                orderDetail.good_number = d.good_number
                orderDetail.good_total = d.good_total
                orderDetail.good_store = d.good_store
                orderDetail.good_image = d.good_image
                orderDetail.save()

            # order 是一条支付页 也就是成功保存完数据会跳转到支付界面
            url = '/Buyer/place_order/?order_id=%s'%order.id
            return HttpResponseRedirect(url)
        return render(request, 'buyer/cart.html', locals())

@set_cookie
def cart_hint(request):
    return render(request, 'buyer/cart_hint.html')

@set_cookie
def add_cart(request):
    result = {'state': 'error', 'data': ''}
    if request.method == 'POST':
        # 通过post传递的值，获取数量与商品id
        count = int(request.POST.get('count'))
        good_id = request.POST.get('good_id')
        good = Goods.objects.get(id=int(good_id))
        # 通过cookie值获取用户id
        user_id = request.COOKIES.get('user_id')
        # 将获取的数据保存到数据库
        cart = Cart()
        cart.good_name = good.good_name
        cart.good_pirce = good.good_price
        cart.good_total = count * good.good_price
        cart.good_number = count
        cart.good_image = good.good_image
        cart.good_id = good_id
        cart.good_store = good.store_id.id
        cart.user_id = user_id
        cart.save()
        result['state'] = 'success'
        result['data'] = '加入购物车成功'
    else:
        result['data'] = '请求错误'
    return JsonResponse(result)

def del_cart(request):
    pass

# 定义支付结果功能
def pay_result(request):
    '''
    支付宝支付成功自动生成用get请求返回的参数
    # 编码
    charset = utf-8
    # 订单号
    out_trade_no = 10002
    # 订单类型
    method = alipay.trade.page.pay.return
    # 订单金额
    total_amount = 1000.00
    # 校验值
    sign = enBOqQsaL641Ssf%2FcIpVMycJTiDaKdE8bx8tH6shBDagaNxNfKvv5iD737ElbRICu1Ox9OuwjR5J92k0x8Xr3mSFYVJG1DiQk3DBOlzIbRG1jpVbAEavrgePBJ2UfQuIlyvAY1fu%2FmdKnCaPtqJLsCFQOWGbPcPRuez4FW0lavIN3UEoNGhL%2BHsBGH5mGFBY7DYllS2kOO5FQvE3XjkD26z1pzWoeZIbz6ZgLtyjz3HRszo%2BQFQmHMX%2BM4EWmyfQD1ZFtZVdDEXhT%2Fy63OZN0%2FoZtYHIpSUF2W0FUi7qDrzfM3y%2B%2BpunFIlNvl49eVjwsiqKF51GJBhMWVXPymjM%2Fg%3D%3D&trade_no=2019072622001422161000050134&auth_app_id=2016093000628355&version=1.0&app_id=2016093000628355
    # 订单号
    trade_no=2019072622001422161000050134
    # 用户的应用id
    auth_app_id=2016093000628355
    # 版本
    version=1.0
    # 商家的应用id
    app_id=2016093000628355
    # 加密方式
    sign_type=RSA2
    # 商家id
    seller_id=2088102177891440
    # 时间
    timestamp=2019-07-26
    '''
    return render(request, "buyer/pay_result.html", locals())

def pay_order(request):
    money = request.GET.get("money")  # 获取订单金额
    order_id = request.GET.get("order_id")  # 获取订单id

    alipay_public_key_string = """-----BEGIN PUBLIC KEY-----
    MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA6M7zHSmJhDrrfKt7eYapbbGhdth72wcws74vLQamlzIpCuLLTaJFUkva0fVlwAwl0l9DZotLSORKxxIORhzslOxtwGnQ+staKJUEe2AhLVu/v5jRTIuVPVFm7qgWXD/H3vNF9kL9jFCl1REvgc207xe0r1rk41cQFAodWmJEp+0pcKq6UzAi8ZNhnjbSQjOE1WbMDIb+lgXQdDlk/Bp5w2W7wNJ6oAISejruKAOvCSnbk1WRUYUDPXxbJakhqBoozrni8R5LKEQ/MJAs9ztCi3h3RKdAhaOqgaTwrR52fCqolaCl0JTUZu0YNIqUdeo3MbnqC95HIK82N0h6oL9mWwIDAQAB
    -----END PUBLIC KEY-----"""

    app_private_key_string = """-----BEGIN RSA PRIVATE KEY-----
    MIIEpgIBAAKCAQEA6M7zHSmJhDrrfKt7eYapbbGhdth72wcws74vLQamlzIpCuLLTaJFUkva0fVlwAwl0l9DZotLSORKxxIORhzslOxtwGnQ+staKJUEe2AhLVu/v5jRTIuVPVFm7qgWXD/H3vNF9kL9jFCl1REvgc207xe0r1rk41cQFAodWmJEp+0pcKq6UzAi8ZNhnjbSQjOE1WbMDIb+lgXQdDlk/Bp5w2W7wNJ6oAISejruKAOvCSnbk1WRUYUDPXxbJakhqBoozrni8R5LKEQ/MJAs9ztCi3h3RKdAhaOqgaTwrR52fCqolaCl0JTUZu0YNIqUdeo3MbnqC95HIK82N0h6oL9mWwIDAQABAoIBAQCoKOO+SsSD+LMkKBFWJIi5LTc9yv0bpkPtcRBOa6FlUNwIeuzytKVx3ky+n4zRfXTMUfczWKYWjp/czxP0XOweXfCgrU4/+Sa0bX8BRtxwEPeeA1oa+i/gTK4W8N7F32QVjI8aZCUUdyRxlKpGDjoFAZCHoRX3iGmar/unz5db2zfYx1XvelzP8B10XCBg9E8Efid587ud6g+FfaC+YbSfH9I6bE3cGcGF4Vr3/iDK7StvjaPJflGl/zZKkjakrhglJWa5k4yqfgwjqxnOT6FR1r4kMm59p62D2MsmAdn6WXRk3iEGLfXOhTRA8TuzKD/KX9NhqRWkVSoLMGGU6MqBAoGBAPwkt00FvmvL+M0F84Dl5qcdTg6jYbB8T/Jp1+rJHDA/4jboZwxd9NuChiks+IWhQASUYp8aedjaJShm+xgwzOZGbNrD3gk3asQMqfdReRiW8/dnOGi2r3Q5vyR7yFxLITLsBjh44CYPxJNmoX01mx84Wwpg3/t01K4pFGL+aVahAoGBAOxehq5CDbMnexPDycP1lBwyp8TGlocO+5xkDzi94IQ9Pam3Gp/CiPXx3F9ZBvuKg3SGTamBPVsOvs0yNjv119Px0pjuPIkenkhUN7s56rQhXBSvj1dDAceSkYlxoY28bHa4gS781i1/6CkNhW4kvVsgUgwlOzxb9qlStWyFSGd7AoGBAKyA3htG87lCSkzSZn7oSv5IMVAYfUxGMFgUC9Gol61292hDZcTzPwMy8GCZUMnzwR2g+zwI3BX9YPCcS+uH75cX1X9yA6VgkZ3hYCNBTU0CcZTwvIn/elhU7a2jNjfWercg/TyDji7cGMwTqiZEl4UrhDW8g2DA1IT2u+jiT+UhAoGBAOuIUdpo9a/VIp6SVYaQOvNSQr0hSjPw6SZwyn43Lvd28vAgBka2GbZCON9GHmAfKVi+z7qdjx8idVyRsVtUYanP6ZP8qZPVT9IxIYvObaLrLw9p1YMVwTs2QRHdiidrYAV5WzkQNvgF4biuwYv8zjd04G072GgQF52oTiKCOaDrAoGBANg3xbUhpWAKqSLRTnTKzxikBZdfpHPgC7S9fAHumYBp4m252nJCQORh/TA/E0GVSxE+tqih98EGvbWqck+yhYTaxqcO2pRmrnFT0xizHKfjJsmMkuzxKY6FOL3SrZv2Kj0KhSuW0KmkpCSF5Yw2dbHvuHCh56c2ttPhVQUDV5eO
    -----END RSA PRIVATE KEY-----"""

    # 实例化支付应用
    alipay = AliPay(
        appid="2016093000628355",
        app_notify_url=None,
        app_private_key_string=app_private_key_string,
        alipay_public_key_string=alipay_public_key_string,
        sign_type="RSA2"
    )

    # 发起支付请求
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=order_id,  # 订单号
        total_amount=str(money),  # 支付金额
        subject="生鲜交易",  # 交易主题
        return_url="http://127.0.0.1:8000/Buyer/pay_result/",
        notify_url="http://127.0.0.1:8000/Buyer/pay_result/"
    )
    # 在支付成功以后，将订单的数据修改为2
    order = Order.objects.get(order_id=order_id)
    order.order_status = 2
    order.save()

    return HttpResponseRedirect("https://openapi.alipaydev.com/gateway.do?" + order_string)



# 定义 点击立即购买跳转页面
def place_order(request):
    if request.method == 'POST':
        # 先保存订单表 获取数据
        # 获取post数据
        count = int(request.POST.get('count'))
        good_id = request.POST.get('good_id')
        # 获取cookie数据
        user_id = request.COOKIES.get('user_id')
        # 获取数据库数据
        good = Goods.objects.get(id=int(good_id))
        store_id = good.store_id.id  # 获取对应商店的id
        price = good.good_price

        # 保存order表数据
        order = Order()
        order.order_id = setOrderId(str(user_id), str(good_id), str(store_id))
        order.good_count = count
        order.order_user = Buyer.objects.get(id=user_id)
        order.order_price = count * price
        # 保存数据提交状态 1为未支付
        order.order_status = 1
        order.save()

        # 保存OrderDetail数据
        order_detail = OrderDetail()
        order_detail.order_id = order
        order_detail.good_id = good_id
        order_detail.good_name = good.good_name
        order_detail.good_price = good.good_price
        order_detail.good_number = count
        order_detail.good_total = count * good.good_price
        order_detail.good_store = store_id
        order_detail.good_image = good.good_image
        order_detail.save()

        detail = [order_detail]
        return render(request, 'buyer/place_order.html', locals())
    else:
        # 如果是get请求方式，则先获取订单编号
        order_id = request.GET.get('order_id')
        # trug有订单编号
        if order_id:
            # 通过订单编号，查询订单的信息
            order = Order.objects.get(id=order_id)
            # 通过外键查询，查询到详细的订单信息
            detail = order.orderdetail_set.all()
            return render(request,'buyer/place_order.html',locals())
        else:
            return HttpResponse('非法请求')
# Create your views here.
