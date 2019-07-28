from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from Buyer import models
from Store import  models
from Store.views import  setPassword



# 定义身份验证
def set_cookie(fun):
    def inner(request,*args,**kwargs):
        pass


def base(request):
    return render(request,'buyer/base.html')


def register(request):
    if request.method=='POST':
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        cpassword = request.POST.get('cpwd')
        email = request.POST.get('email')
        if username and password and cpassword and email:
            if setPassword(password)==setPassword(cpassword):
                buyer = models.Buyer()
                buyer.username = username
                buyer.password = setPassword(password)
                buyer.email = email
                buyer.save()
                return HttpResponseRedirect('/Buyer/login/')
    return render(request,'buyer/register.html')
def login(request):
    if request.method=='POST':
        username =  request.POST.get('username')
        password = request.POST.get('pwd')
        if username and password:
            user = models.Seller.objects.filter(username=username).first()
            web_password = user.password
            if user and setPassword(password)==web_password:
                response = HttpResponseRedirect('/Buyer/index/')
                response.set_cookie('username',username)
                request.session['username']= username
                # 为了以后的方便，加入id认证
                response.set_cookie('user_id',user.id)
                return response
    return render(request,'buyer/login.html')

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
        response.delete_cookie(key)
    del request.session['username']
    return response


def index(request):
    # 创建一个列表，用来存储一个结果
    result_list = []
    # 查询所有商品类型
    goods_type_list = models.GoodsType.objects.all()
    # 循环所有类型
    for i in goods_type_list:
        goodsList = i.goods_set.values()[:4]# 查询前四条数据
        if goodsList:
            goodsType = {
                'id' :i.id,
                'name':i.name,
                'description':i.description,
                'picture':i.picture,
                'goods_list':goodsList
            } # 构建输出结果
            # 查询类型当中有数据的数据
            result_list.append(goodsType)# 将有数据的数据放入到result_list
    return render(request,'buyer/index.html',locals())


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
    goods_type = models.GoodsType.objects.filter(id=type_id).first()
    # 如果类型存在
    if goods_type:
        # 则通过商品外键获取商品列表
        goodsList = goods_type.goods_set.filter(good_state = 1)
    return render(request,'buyer/goods_list.html',locals())


def detail(request):
    # 定义一个列表用于储存结果
    goodsList = []
    good_id = request.GET.get('good_id')
    if good_id:
        goodsList = models.Goods.objects.filter(id=good_id)
    # 通过商品ID可以获取到商品信息
    return  render(request,'buyer/detail.html',locals())

def cart(request):
    user_id = request.COOKIES.get('user_id')
    if not user_id:
        return HttpResponseRedirect()
    return render(request,'buyer/cart.html',locals())

# Create your views here.
