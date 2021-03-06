from django.db import models
# 导入自定义类型模块
from django.db.models import Manager
# Create your models here.
#  卖家模型
class Seller(models.Model):
    username = models.CharField(max_length=32,verbose_name='用户名')
    password = models.CharField(max_length=32,verbose_name='密码')
    nickname = models.CharField(max_length=32,verbose_name='昵称',null=True,blank=True)
    phone = models.CharField(max_length=32,verbose_name='昵称',null=True,blank=True)
    email = models.EmailField(verbose_name='邮箱',null=True,blank=True)
    picture = models.ImageField(upload_to='store/images',verbose_name='用户头像',null=True,blank=True)
    address = models.CharField(max_length=32,verbose_name='地址',null=True,blank=True)

    card_id = models.CharField(max_length=32,verbose_name='身份证',null=True,blank=True)


# 卖家类型
class StoreType(models.Model):
    store_type = models.CharField(max_length=32,verbose_name='类型名称')
    type_description = models.TextField(verbose_name='类型描述')



# 商店模型
class Store(models.Model):
    store_name = models.CharField(max_length=32,verbose_name='店铺名称')
    store_address = models.CharField(max_length=32,verbose_name='店铺地址')
    store_description = models.TextField(verbose_name='店铺描述')
    store_logo = models.ImageField(upload_to='store/images',verbose_name='店铺logo')
    store_phone = models.CharField(max_length=32,verbose_name='店铺电话')
    store_money = models.FloatField(verbose_name='店铺注册资金')


    user_id = models.IntegerField(verbose_name='店铺主人')
    type = models.ManyToManyField(to=StoreType,verbose_name='店铺类型')
# 商品类型模型
class GoodsType(models.Model):
    name = models.CharField(max_length=32,verbose_name='商品类型名称')
    description = models.TextField(verbose_name='商品类型描述')
    picture = models.ImageField(upload_to='buyer/images')


# 商品模型
class Goods(models.Model):
    good_name = models.CharField(max_length=32,verbose_name='商品名称')
    good_price = models.FloatField(verbose_name='商品价格')
    good_image = models.ImageField(upload_to='store/images',verbose_name='商品图片')
    good_number = models.IntegerField(verbose_name='商品数量库存')
    good_description = models.TextField(verbose_name='商品描述')
    good_date = models.DateField(verbose_name='商品出厂日期')
    good_safeDate = models.IntegerField(verbose_name='商品保质期')
    good_state  = models.IntegerField(verbose_name='商品状态',default=1)# 待售为1 下架为0

    good_type = models.ForeignKey(to=GoodsType,on_delete=models.CASCADE,verbose_name='商品类型')
    store_id = models.ForeignKey(to=Store,on_delete=models.CASCADE,verbose_name='店铺名称')

# 商品图片模型
class GoodsImg(models.Model):
    img_address = models.ImageField(upload_to='store',verbose_name='图片地址')
    img_description = models.TextField(verbose_name='图片描述')

    goods_id = models.ForeignKey(to=Goods,on_delete=models.CASCADE,verbose_name='商品ID')
