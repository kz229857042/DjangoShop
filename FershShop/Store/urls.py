from django.urls import path
from django.urls import re_path
from Store.views import *

urlpatterns = [
    path('register/', register),
    path('login/', login),
    path('index/', index),
    re_path('^$', index),# 将不输入的网址默认跳转到首页
    path('base/', base),
]