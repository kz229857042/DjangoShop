from django.urls import path
from django.urls import re_path
from Store.views import *

urlpatterns = [
    path('register/', register),
    path('login/', login),
    path('index/', index),
    re_path('^$', index),# 将不输入的网址默认跳转到首页
    path('rs/', register_store),
    path('add_goods/', add_goods),
    re_path(r'list_goods/(?P<state>\w+)', list_goods),# 设置商品列表
    re_path(r'dg/(?P<good_id>\d+)',details_goods),
    re_path(r'update_goods/(?P<good_id>\d+)',update_goods),
    re_path(r'set_goods/(?P<state>\w+)' ,set_goods),# 设置商品状态
    path('logout/', logout),
    path('list_goods_type/', list_goods_type),
    path('add_goods_type/', add_goods_type),
    path('del_goods_type/', del_goods_type),
]

# 调试页面 需要单分出来 以后上传的时候可以删除
urlpatterns +=[
    path('base/', base),
]