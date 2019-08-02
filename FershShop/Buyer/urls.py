
from django.urls import path,include,re_path
from Buyer.views import *


urlpatterns = [
    path('register/',register),
    path('login/',login),
    path('logout/',logout),
    path('index/',index),
    re_path('^$',index),
    path('goods_list/',goods_list),
    path('detail/', detail),
    path('cart/', cart),
    path('cart_hint/', cart_hint),
    path('add_cart/', add_cart),
    path('place_order/', place_order),
]
urlpatterns +=[
    path('base/',base),
    # 支付结果界面
    path("pay_result/", pay_result),
    # 支付界面
    path("pay_order/", pay_order),
]