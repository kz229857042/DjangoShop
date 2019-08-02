

# 创建的serializers文件就是用于存放接口的过滤器

from rest_framework import serializers

from Store.models import *

# 定义用户商品类的接口
class UserSerializer(serializers.HyperlinkedModelSerializer):
    '''
    声明数据（序列化数据）
    '''

    class Meta:  # 元类
        model = Goods  # 要进行接口序列化的模型
        fields = ['good_name', 'good_price', 'good_number', 'good_date','good_safeDate','id']  # 序列要返回的字段
# 定义商品类型接口
class GoodsTypeSerializer(serializers.HyperlinkedModelSerializer):
    '''
        声明查询的表和返回的字段
    '''

    class Meta:
        model = GoodsType
        fields = ['name', 'description']

# 定义商店类型接口
class StoreTypeSerializer(serializers.HyperlinkedModelSerializer):

    class Mate:
        model  = StoreType  # 要进行接口序列化的模型
        fields = ['store_type','type_description']
