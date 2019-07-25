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
    path('list_goods/', list_goods),
    re_path(r'dg/(?P<good_id>\d+)',details_goods),
    re_path(r'update_goods/(?P<good_id>\d+)',update_goods),

]

# 调试页面 需要单分出来 以后上传的时候可以删除
urlpatterns +=[
    path('base/', base),
]