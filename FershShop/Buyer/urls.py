
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
]
urlpatterns +=[
    path('base/',base),
]