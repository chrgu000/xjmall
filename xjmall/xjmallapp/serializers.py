# coding:utf-8
from rest_framework import serializers
from models import *



class SellerUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = SellerUser
        fields = ('id', 'name', 'phone','area','user_type','icon_phone')

class StoreSerializers(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    # virtual_coin_limit = serializers.SerializerMethodField()  #展示choice内容
    # selleruser = SellerUserSerializers(read_only=True)

    # name = serializers.CharField(required=True,max_length=60)
    # store_name = serializers.CharField(required=True,max_length=60)
    # account = serializers.CharField(required=True, max_length=20,min_length=6)  #账号即手机号
    # password = serializers.CharField(required=True, max_length=20,min_length=6)

    class Meta:
        model = Store
        fields = ('id', 'name', 'store_name', 'virtual_coin_limit', 'virtual_coin_canuse', 'is_check',
                  'account','selleruser_info','create_time','address')
    # def get_virtual_coin_limit(self,obj):
    #     return obj.get_virtual_coin_limit_display()

    # def create(self, validated_data):
    #     print validated_data
    #     print '------create store'
    #     return Store.objects.create(**validated_data)

class DeliveryAddressSerializers(serializers.ModelSerializer):
    store = StoreSerializers(read_only=True)
    class Meta:
        model = DeliveryAddress
        fields = '__all__'

class ClassificationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Classification
        fields = '__all__'


class GoodSerializers(serializers.ModelSerializer):
    classification = ClassificationSerializers(read_only=True)
    class Meta:
        model = Good
        # fields = '__all__'
        fields = ('id','name','picture','current_nums','unit','price','priority','classification','sales_volume')
        # fields = ('id','name')


class OrderSerializers(serializers.ModelSerializer):
    store_belong = StoreSerializers(read_only=True)
    check_user = SellerUserSerializers()
    create_time = serializers.DateTimeField(read_only=True,format='%Y-%m-%d %H:%M:%S')
    class Meta:
        model = Order
        fields = ('id','order_num','express_num','express_cost',
                  'store_belong','total_price','firstorderitem','check_user','create_time','address','order_status','good_quantity')


class OrderItemSerializers(serializers.ModelSerializer):
    good = GoodSerializers(read_only=True)
    # belong = OrderSerializers(read_only=True)
    class Meta:
        model = OrderItem
        fields = '__all__'



class ShoppingCardSerializers(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    good = GoodSerializers(read_only=True)
    store = StoreSerializers(read_only=True)
    class Meta:
        model = ShoppingCard
        fields = ('id','good','store','numbers','total_price','create_time')



