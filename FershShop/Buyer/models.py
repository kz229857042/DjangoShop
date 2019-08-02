from django.db import models



class Buyer(models.Model):
    username = models.CharField(max_length=32,verbose_name='用户名')
    password = models.CharField(max_length=32,verbose_name='密码')
    email = models.EmailField(verbose_name='邮箱')
    phone = models.IntegerField(verbose_name='联系电话',blank=True,null=True)
    connect_address = models.TextField(verbose_name='联系地址',blank=True,null=True)



class Address(models.Model):
    address = models.TextField(verbose_name='收货地址')
    receive = models.CharField(max_length=32,verbose_name='收货人')
    receive_phone = models.IntegerField(verbose_name='收货人电话')
    post_number = models.IntegerField(verbose_name='邮编')
    buyer_id = models.ForeignKey(to=Buyer,on_delete=models.CASCADE,verbose_name='用户ID')



class Order(models.Model):
    '''
    订单表
    '''
    order_id = models.CharField(max_length=32,verbose_name='订单编号')
    good_count = models.IntegerField(verbose_name='订单数量')
    order_user = models.ForeignKey(to=Buyer,on_delete=models.CASCADE,verbose_name='订单用户')
    order_address = models.ForeignKey(to=Address,on_delete=models.CASCADE,verbose_name='订单地址',blank=True,null=True)
    order_price = models.FloatField(verbose_name='订单总价')
    order_status = models.IntegerField(default=1,verbose_name='订单状态')


class OrderDetail(models.Model):
    '''
    订单详情表
    '''
    order_id = models.ForeignKey(to=Order,on_delete=models.CASCADE,verbose_name='订单编号')
    good_id = models.IntegerField(verbose_name='商品id')
    good_name = models.CharField(max_length=32,verbose_name='商品名称')
    good_price = models.FloatField(verbose_name='商品价格')
    good_number = models.IntegerField(verbose_name='商品数量')
    good_total = models.FloatField(verbose_name='商品总价')
    good_store = models.IntegerField(verbose_name='商店id')
    good_image = models.ImageField(verbose_name='商品图片')
# Create your models here.


class Cart(models.Model):
    good_name = models.CharField(max_length=32,verbose_name='商品名称')
    good_price = models.FloatField(verbose_name='商品价格')
    good_total = models.FloatField(verbose_name='商品总价')
    good_number = models.IntegerField(verbose_name='商品数量')
    good_image = models.FileField(upload_to='buyer/images',verbose_name='商品图片')
    good_id = models.IntegerField(verbose_name='商品ID')
    good_store = models.IntegerField('商品店铺')
    user_id = models.IntegerField(verbose_name='用户ID')