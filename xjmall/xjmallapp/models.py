# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone


# Create your models here.

# 时间基类
class BaseModel(models.Model):
    create_time = models.DateTimeField(default=timezone.now)
    modify_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# 销售代表
class SellerUser(BaseModel):
    user_type_choice = [
        (0, '销售代表'),
        (1, '管理员'),
    ]
    name = models.CharField(max_length=32, verbose_name='销售代表的名字')
    phone = models.CharField(max_length=32, verbose_name='销售代表的电话',null=True,blank=True)
    account = models.CharField(max_length=64, unique=True, verbose_name='销售代表的账号,6-20位')
    password = models.CharField(max_length=128, verbose_name='销售代表的密码,6-20位')
    area = models.CharField(max_length=64, verbose_name='地区')
    user_type = models.IntegerField(choices=user_type_choice,default=0,verbose_name='用户类型')
    icon_phone = models.CharField(max_length=128, verbose_name='电话小图标',default='http://static.fibar.cn/icon_phone1.png')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = '销售代表'

    def save(self, *args, **kwargs):
        if (len(self.account) < 3 or len(self.account) > 20) or (len(self.password) < 6 or len(self.password) > 20):
            raise ValueError("account or password length invalid")
        super(SellerUser, self).save(*args, **kwargs)

#on_delete=models.CASCADE


# 门店
class Store(BaseModel):
    virtual_coin_limit_choice = [
        (0, 5000.0),
        (1, 50000.0),
    ]
    account = models.CharField(max_length=64,verbose_name='销售代表的账号,6-20位') #手机号为账号
    password = models.CharField(max_length=128, verbose_name='销售代表的密码,6-20位')
    name = models.CharField(max_length=128, verbose_name='注册人名字')
    store_name = models.CharField(max_length=128, verbose_name='终端店名字',unique=True)
    # phone = models.CharField(max_length=32, verbose_name='终端店电话')
    virtual_coin_limit = models.IntegerField(choices=virtual_coin_limit_choice, null=True, blank=True,
                                             verbose_name='额度')
    virtual_coin_canuse = models.FloatField(default=0.0, verbose_name='可使用的额度')
    selleruser = models.ForeignKey(SellerUser, related_name='selleruser_store', null=True, blank=True,
                                   verbose_name='所属销售代表')
    is_check = models.BooleanField(default=False, verbose_name='是否审核了')
    address = models.CharField(max_length=128, verbose_name='终端店地址',null=True,blank=True)

    def __unicode__(self):
        return self.store_name

    class Meta:
        verbose_name_plural = '终端店'

    def selleruser_info(self):
        if self.selleruser:
            return self.selleruser.name
        else:
            return '未审核通过，暂无'

    def save(self, *args, **kwargs):
        if (len(self.account) < 6 or len(self.account) > 20) or (len(self.password) < 6 or len(self.password) > 20):
            raise ValueError("account or password length invalid")
        super(Store, self).save(*args, **kwargs)


class DeliveryAddress(BaseModel):
    store = models.ForeignKey(Store,related_name='store_deliveryaddress',verbose_name='所属店铺')
    phone = models.CharField(max_length=32, verbose_name='收货电话')
    name = models.CharField(max_length=16, verbose_name='收货人姓名')
    is_default = models.BooleanField(default=False,verbose_name='默认收货地址')
    detail_address = models.CharField(max_length=128, verbose_name='详细地址',default='',blank=True,null=True)
    area_address = models.CharField(max_length=64, verbose_name='区域地址',default='',blank=True,null=True)
    area_code = models.CharField(max_length=64, verbose_name='区域编号',default='',blank=True,null=True)
    postalcode=models.CharField(max_length=64, verbose_name='邮政编码',default='',blank=True,null=True)
    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = '收货地址'

class Classification(BaseModel):
    name = models.CharField(max_length=64)
    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = '商品类别'

# 商品
class Good(BaseModel):
    name = models.CharField(max_length=32, verbose_name='商品名字')
    picture = models.ImageField(upload_to='photo',null=True,blank=True,default='photo/default.png')
#    picture = models.TextField(verbose_name='商品图片',null=True,blank=True,default='')
    current_nums = models.IntegerField(default=0, verbose_name='商品库存')
    unit = models.CharField(max_length=32, verbose_name='商品单位')
    price = models.FloatField(default=0.0, verbose_name='商品价格')
    priority = models.IntegerField(default=0, verbose_name='商品权重，越大越优先展示')
    classification = models.ForeignKey(Classification,related_name='classification_good',verbose_name='商品类别')
#    picture_str = models.TextField(default='',null=True,blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = '商品'

    def sales_volume(self):   #销量
        eles = OrderItem.objects.filter(good=self).filter(belong__order_status__in=[1,3])  # 取order_status等于1、3的
        sum = 0
        for ele in eles:
            sum+=ele.numbers
        return sum

#一对一测试
class GoodCode(BaseModel):
    code = models.OneToOneField(Good,on_delete=models.CASCADE,related_name='code_good')   #CASCADE，删除good，goodcode也就没了
    name = models.CharField(max_length=64)
    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = '商品编码'



#多对多测试
class Category(BaseModel):
    name = models.CharField(max_length=128)
    good = models.ManyToManyField(Good,related_name='category_good')
    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = '多对多商品种类'




# 订单
class Order(BaseModel):
    order_status_choice = [
       (0, '未审核'),
       (1, '审核通过'),
       (2, '审核驳回'),
       (3, '配送完成'),
    ]
    order_num = models.CharField(max_length=64, verbose_name='订单号',unique=True)
#    is_check = models.BooleanField(default=False, verbose_name='是否审核')
    express_num = models.CharField(max_length=64, verbose_name='快递号', null=True, blank=True)
    express_cost = models.FloatField(default=0.0, verbose_name='运费')
    store_belong = models.ForeignKey(Store, related_name='storebelong_order', verbose_name='订单所属门店')
    total_price = models.FloatField(default=0.0, verbose_name='订单总价')
    check_user = models.ForeignKey(SellerUser,related_name='checkuser_order',verbose_name='审核人员')
#    is_delivery = models.BooleanField(default=False,verbose_name='是否收货，默认超过七天自动收货')
    address = models.CharField(max_length=128, verbose_name='收货信息', null=True, blank=True,default='')
#    is_revoke = models.BooleanField(default=False,verbose_name='是否被驳回')
    order_status = models.IntegerField(default=0,choices=order_status_choice,verbose_name='订单状态')
    def save(self, *args, **kwargs):
        self.total_price = round(self.total_price,2)
        super(Order, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.order_num

    class Meta:
        verbose_name_plural = '订单'
    def good_quantity(self):
        orderitems = self.belong_orderitem.all()
        num = 0
        for orderitem in orderitems:
            num+=orderitem.numbers
        return num

    def firstorderitem(self):
        orderitem = self.belong_orderitem.first()
        # from xjmallapp.serializers import OrderItemSerializers
        # return OrderItemSerializers()
        picture_url = "http://shop-xj.chafanbao.com"+orderitem.good.picture.url
        return {'good_name':orderitem.good.name,'numbers':orderitem.numbers,'picture':picture_url,
                'orderitem_total_price':orderitem.total_price}



# 订单详情
class OrderItem(BaseModel):
    good = models.ForeignKey(Good, related_name='good_orderitem', verbose_name='订单单个商品')
    numbers = models.IntegerField(default=0, verbose_name='订单单个商品数量')
    belong = models.ForeignKey(Order, related_name='belong_orderitem', verbose_name='所属订单')
    total_price = models.FloatField(default=0.0)

    def __unicode__(self):
        return self.belong.order_num

    class Meta:
        verbose_name_plural = '订单详情'
    def save(self, *args, **kwargs):
        self.total_price = round(self.total_price,2)
        super(OrderItem, self).save(*args, **kwargs)


# 购物车
class ShoppingCard(BaseModel):
    good = models.ForeignKey(Good, related_name='good_shoppingcard', verbose_name='购物车商品')
    numbers = models.IntegerField(default=0, verbose_name='购物车单个商品数量')
    store = models.ForeignKey(Store, related_name='store_shoppingcard', verbose_name='所属终端店')
    # total_price = models.FloatField(default=0.0)

    def __unicode__(self):
        return self.store.name

    class Meta:
        verbose_name_plural = '购物车'
    # def save(self, *args, **kwargs):
    #     self.total_price = round(self.total_price,2)
    #     super(ShoppingCard, self).save(*args, **kwargs)


    @property
    def total_price(self):
        return round(self.good.price*self.numbers,2)


# 短信发送表
# class Message(BaseModel):
#     message_type_choice = [
#         (0, '用户注册'),
#         (1, '终端店审核通过'),
#         (2, '修改密码')
#     ]
#     message_type = models.IntegerField(choices=message_type_choice)
#     content = models.TextField(verbose_name='短信文本')
#     sendee = models.ForeignKey(Store, related_name='sendee_message', verbose_name='短信接收方',null=True,blank=True)
#     sender = models.ForeignKey(SellerUser, related_name='sender_message', verbose_name='短信发送方',null=True,blank=True)
#
#     def __unicode__(self):
#         return self.content
#
#     class Meta:
#         verbose_name_plural = '短信发送表'


# 销售人员token
class SellerUserToken(BaseModel):
    token = models.CharField(max_length=128)
    selleruser = models.ForeignKey(SellerUser, related_name='selleruser_token', verbose_name='销售人员token')

    def __unicode__(self):
        return self.selleruser.name

    class Meta:
        verbose_name_plural = 'token销售代表'


# 终端店token
class StoreToken(BaseModel):
    token = models.CharField(max_length=128)
    store = models.ForeignKey(Store, related_name='store_token', verbose_name='终端店人员token')

    def __unicode__(self):
        return self.store.name

    class Meta:
        verbose_name_plural = 'token终端店'



