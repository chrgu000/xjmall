# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
import json
from rest_framework import viewsets
from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse, HttpResponse
from models import *
from serializers import *
from rest_framework.response import Response
# from rest_framework.pagination import PageNumberPagination
from core.mixin import *
from django_filters.rest_framework.backends import DjangoFilterBackend
import random
import hashlib
from core.func import create_token
from core.send_message import client_post_formurlencodeddata_requests
from datetime import datetime,timedelta
from core.send_ic import save_redis_ic
import sys
import redis
import time
from core.cut_page import cutpage
from core.send_revoke_message import send_revoke_store_message
# import pudb; pu.db

reload(sys)
sys.setdefaultencoding('utf8')


#发送验证码
class SendICView(APIView):
    def get(self,request):
        data = request.GET
        account = data.get('account')
        style = int(data.get('style'))  # 1为注册的验证码，2为找回密码的验证码
        if style == 1:
            if Store.objects.filter(account=account).first():
                return Response({'body': {}, 'status': ERROR_ACCOUNTREPEAT, 'msg': 'phone used'})  # 账号重复

        r = redis.StrictRedis(host='localhost', port=6379, db=7)
        if r.get(account):
            return Response({'body': {}, 'status': ERROR_INFO, 'msg': 'It is been done in five minutes'})
        redis_ic = save_redis_ic(phone=account)
        if redis_ic:
            return Response({'body': {'ic':redis_ic}, 'status': INFO_SUCCESS, 'msg': 'send message success'})
        return Response({'body': {}, 'status': ERROR_INFO, 'msg': 'send message fail'})


# 注册
class RegisterView(APIView):
    def post(self, request):
        data1 = request.body
        data = json.loads(data1.decode('utf-8'))
        print 'data--', data
        account = data.get('account')
        password = data.get('password')
        password2 = data.get('password2')
        name = data.get('name')
        store_name = data.get('store_name')
        address = data.get('address')
        ic = data.get('ic')
        r = redis.StrictRedis(host='localhost', port=6379, db=7)
        redis_ic = r.get(account)
        if not redis_ic or not ic == redis_ic or not ic:
            return Response({'body': {}, 'status': ERROR_PARAMETER, 'msg': 'identifying code wrong'})

        if password != password2:
            return Response({'body': {}, 'status': ERROR_PARAMETER, 'msg': 'inconsistent passwords '})  # 密码不一致

        if not all([account,password,name,store_name,address]):
            return Response({'body': {}, 'status': ERROR_PARAMETER, 'msg': 'loss param'})  # 缺少字段
        if Store.objects.filter(account=account).first() or Store.objects.filter(store_name=store_name).first():
            return Response({'body': {}, 'status': ERROR_ACCOUNTREPEAT, 'msg': 'phone used'})  # 账号重复
        store = Store(account=account,name=name,store_name=store_name,password=password,address=address)
        store.save()
        # DeliveryAddress(store=store,address=address,phone=account,name=name).save()
        return Response({'body': {}, 'status': INFO_SUCCESS, 'msg': 'register success'})  # 注册成功


# 终端店登录
class LoginStoreView(APIView):
    def get(self, request):
        data = request.GET
        account = data.get('account')
        password = data.get('password')
        print data
        if account and password:
            store = Store.objects.filter(account=account).first()
            if not store:
                return Response({'body': {}, 'status': ERROR_LOGIN, 'msg': 'no the account'})
            if not any([store.password == password,hashlib.md5(store.password) == password,]):
                return Response({'body': {}, 'status': ERROR_LOGIN, 'msg': 'password wrong'})
            if store:
                serializer = StoreSerializers(store)
                random_token = create_token()
                data = serializer.data
                data['spl_token'] = random_token
                StoreToken(store = store,token=random_token).save()
                default_deliveryaddress = store.store_deliveryaddress.filter(is_default = True).first()
                if default_deliveryaddress:
                    body = {'user_info':data,'deliveryaddress_info':DeliveryAddressSerializers(default_deliveryaddress).data}
                else:
                    body = {'user_info': data}
                return Response({'body':body,'status':INFO_SUCCESS,'msg':'login success'})
        return Response({'body': {}, 'status': ERROR_LOGIN, 'msg': 'login error'})

# 销售代表登录
class LoginSellerUserView(APIView):
    def get(self, request):
        data = request.GET
        account = data.get('account')
        password = data.get('password')
        print account,password
        print data
        if account and password:
            selleruser = SellerUser.objects.filter(account=account).first()
            if not selleruser:
                return Response({'body': {}, 'status': ERROR_LOGIN, 'msg': 'no the account'})
            if not any([selleruser.password == password, hashlib.md5(selleruser.password) == password]):
                return Response({'body': {}, 'status': ERROR_LOGIN, 'msg': 'password wrong'})
            if selleruser:
                serializer = SellerUserSerializers(selleruser)
                data = serializer.data
                random_token = create_token()
                data['spl_token'] = random_token
                SellerUserToken(selleruser=selleruser, token=random_token).save()
                return Response({'body': data, 'status': INFO_SUCCESS, 'msg': 'login success'})
        return Response({'body': {}, 'status': ERROR_LOGIN, 'msg': 'login error'})

#找回密码
class RetrievePasswordView(StatusWrapMixin,APIView):
    def get(self,request):
        if not self.check_token(self.request):
            return self.render_to_response({},self.request)
        data = request.GET
        account = data.get('account')
        ic = data.get('ic')
        r = redis.StrictRedis(host='localhost', port=6379, db=7)
        redis_ic = r.get(account)
        print redis_ic
        print ic
        if not redis_ic or not ic == redis_ic or not ic:
            return Response({'body': {}, 'status': ERROR_PARAMETER, 'msg': 'identifying code wrong'})
        store = Store.objects.filter(account=account).first()
        password = store.password
        return Response({'body': {'password':password}, 'status': INFO_SUCCESS, 'msg': 'success'})




#修改密码
class ChangePasswordView(StatusWrapMixin,APIView):
    def post(self,request):
        if not self.check_token(self.request):
            return self.render_to_response({},self.request)
        data1 = request.body
        data = json.loads(data1.decode('utf-8'))
        print 'data--', data
        store_id = data.get('store_id')
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        store = Store.objects.get(id=int(store_id))
        if store.password == old_password:
            store.password = new_password
            store.save()
            return self.render_to_response({},self.request)
        return Response({'body': {}, 'status': ERROR_LOGIN, 'msg': 'error'})


class DeliveryaddressListView(StatusWrapMixin,viewsets.ModelViewSet):
    queryset = DeliveryAddress.objects.filter()
    serializer_class = DeliveryAddressSerializers
    def get_queryset(self):
        return DeliveryAddress.objects.filter()

    def list(self, request, *args, **kwargs):
        store_id = self.request.GET.get('store_id')
        data_list_queryset = self.get_queryset().filter(store=Store.objects.get(id=int(store_id)))
        data_list = self.get_serializer(data_list_queryset, many=True)
        return self.render_to_response(data_list.data, self.request)


#新增收货地址
class CreateDeliveryAddressView(StatusWrapMixin,APIView):
    def post(self,request):
        if not self.check_token(self.request):
            return self.render_to_response({},self.request)
        data1 = request.body
        data = json.loads(data1.decode('utf-8'))
        print 'data--', data
        store_id = data.get('store_id')
        phone = data.get('phone')
        name = data.get('name')
        detail_address = data.get('detail_address')
        area_address = data.get('area_address')
        postalcode = data.get('postalcode')
        is_default = data.get('is_default')
        area_code = data.get('area_code')
        if not all([store_id, phone, name,detail_address,area_address,postalcode]):
            return Response({'body': {}, 'status': ERROR_PARAMETER, 'msg': 'loss param'})
        store = Store.objects.get(id=int(store_id))
        if is_default:
            old_default_deliveryaddress = store.store_deliveryaddress.filter(is_default=True).first()
            if old_default_deliveryaddress:
                old_default_deliveryaddress.is_default = False
                old_default_deliveryaddress.save()

        DeliveryAddress(store=store,phone=phone,name=name,detail_address=detail_address,area_address=area_address,
                        postalcode=postalcode,is_default=is_default,area_code=area_code).save()
        return self.render_to_response({},request)

#设置为默认收获地址
class SetDefaultAddressView(StatusWrapMixin,APIView):
    def post(self,request):
        if not self.check_token(self.request):
            return self.render_to_response({},self.request)
        data1 = request.body
        data = json.loads(data1.decode('utf-8'))
        print 'data--', data
        store_id = data.get('store_id')
        deliveryaddress_id = data.get('deliveryaddress_id')
        store = Store.objects.get(id=int(store_id))
        old_default_deliveryaddress = store.store_deliveryaddress.filter(is_default = True).first()
        if old_default_deliveryaddress:
            old_default_deliveryaddress.is_default = False
            old_default_deliveryaddress.save()
        deliveryaddress = DeliveryAddress.objects.get(id=int(deliveryaddress_id))
        deliveryaddress.is_default = True
        deliveryaddress.save()
        return self.render_to_response({}, request)


#修改收货地址
class ChangeDeliveryAddressView(StatusWrapMixin,APIView):
    def post(self,request):
        if not self.check_token(self.request):
            return self.render_to_response({},self.request)
        data1 = request.body
        data = json.loads(data1.decode('utf-8'))
        print 'data--', data
        phone = data.get('phone')
        name = data.get('name')
        detail_address = data.get('detail_address')
        area_address = data.get('area_address')
        postalcode = data.get('postalcode')
        deliveryaddress_id = data.get('deliveryaddress_id')
        area_code = data.get('area_code')
        is_default = data.get('is_default')

        if not all([deliveryaddress_id,phone, name,detail_address,area_address,postalcode,area_code]):
            return Response({'body': {}, 'status': ERROR_PARAMETER, 'msg': 'loss param'})
        deliveryaddress=DeliveryAddress.objects.get(id=int(deliveryaddress_id))
        deliveryaddress.phone = phone
        deliveryaddress.name = name
        deliveryaddress.detail_address = detail_address
        deliveryaddress.area_address = area_address
        deliveryaddress.postalcode = postalcode
        deliveryaddress.area_code = area_code
        deliveryaddress.is_default = is_default
        deliveryaddress.save()
        return self.render_to_response({},request)

#删除收货地址
class DeleteDeliveryAddress(StatusWrapMixin, APIView):
    def get(self,request):
        if not self.check_token(self.request):
            return self.render_to_response({}, self.request)
        data = request.GET
        deliveryaddress_id = data.get('deliveryaddress_id')
        DeliveryAddress.objects.get(id=int(deliveryaddress_id)).delete()
        return self.render_to_response({}, request)


# 销售人员列表
class SellerUserView(StatusWrapMixin, viewsets.ModelViewSet):
    queryset = SellerUser.objects.filter(user_type=0)
    serializer_class = SellerUserSerializers
    def get_queryset(self):
        return SellerUser.objects.filter(user_type=0)
    def list(self, request, *args, **kwargs):
        data_list_queryset = self.get_queryset()
        print data_list_queryset
        data_list = self.get_serializer(data_list_queryset, many=True)
        return self.render_to_response(data_list.data,self.request)



# 终端店列表，传入参数store_id是查看单个门店信息，如门店查看自己的门店信息，传入参数selleruser_id是销售代表查看自己旗下的门店信息
class StoreView(StatusWrapMixin, viewsets.ModelViewSet):
    queryset = Store.objects.order_by('-create_time')
    serializer_class = StoreSerializers
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('virtual_coin_limit','is_check',)  # 过滤，eg: http://127.0.0.1:8000/school/grade?is_check=0


    def get_queryset(self):
        return Store.objects.order_by('-create_time')

    def list(self, request, *args, **kwargs):
        self.queryset = self.filter_queryset(self.get_queryset())
        store_id = self.request.GET.get('store_id')
        selleruser_id = self.request.GET.get('selleruser_id')

        if store_id:
            data_list_queryset = self.queryset.filter(id=int(store_id)).first()  # 单个门店
            data_list = self.get_serializer(data_list_queryset)
            return self.render_to_response(data_list.data, self.request)
        else:
            if selleruser_id:
                data_list_queryset = self.queryset.filter(
                    selleruser=SellerUser.objects.get(id=int(selleruser_id)))  # 销售代表下的门店
            else:
                data_list_queryset = self.queryset  # 全部

            total_data = len(data_list_queryset)

            if self.request.GET.get('page_size') and self.request.GET.get('page_num'):
                data_list_queryset, page_sum = cutpage(data_list_queryset, self.request.GET.get('page_num'), self.request.GET.get('page_size'))
            else:
                page_sum = 1

            data_list = self.get_serializer(data_list_queryset, many=True)
            return self.render_to_response(data_list.data,self.request,page_sum,total_data)

    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)
    #
    #     serializer = self.get_serializer(queryset, many=True)
    #     return self.render_to_response(serializer.data, self.request)

    # def create(self, request, *args, **kwargs):
    #     data = self.request.data
    #     print data
    #     if Store.objects.filter(account = data.get('account')).first():
    #         return Response({'body': {}, 'status': ERROR_PARAMETER, 'msg': 'phone used'})  # 账号重复
    #     serializer = StoreSerializers(data=data)
    #     if self.check_token:
    #         return self.render_to_response({})
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({'body': {}, 'status': INFO_SUCCESS, 'msg': 'register success'})  # 注册成功
    #     return Response({'body': serializer.errors, 'status': ERROR_PARAMETER, 'msg': 'param error'})  # 参数缺失或错误


# 审核门店
class CheckStoreView(StatusWrapMixin, APIView):
    def post(self, request):
        if not self.check_token(self.request):
            return self.render_to_response({},self.request)
        data1 = request.body
        data = json.loads(data1.decode('utf-8'))
        print 'data--', data
        store_id = data.get('store_id')
        selleruser_id = data.get('selleruser_id')
        virtual_type = int(data.get('virtual_type'))
        if not all([store_id, selleruser_id, virtual_type==0 or virtual_type==1]):
            return Response({'body': {}, 'status': ERROR_PARAMETER, 'msg': 'param error'})
        store = Store.objects.get(id=int(store_id))
        store.selleruser = SellerUser.objects.get(id=int(selleruser_id))
        store.virtual_coin_limit = virtual_type
        store.is_check=True
        if virtual_type ==0:
            store.virtual_coin_canuse=5000.0
        else:
            store.virtual_coin_canuse = 50000.0
        store.save()
        client_post_formurlencodeddata_requests(store.account) #发送审核终端店短信提示
        return self.render_to_response({}, request)

#驳回门店审核
class RevokeStoreView(StatusWrapMixin, APIView):
    def post(self,request):
        if not self.check_token(self.request):
            return self.render_to_response({},self.request)
        data1 = request.body
        data = json.loads(data1.decode('utf-8'))
        print 'data--', data
        store_id = data.get('store_id')
        store = Store.objects.get(id=int(store_id))
        send_revoke_store_message(store.account)
        store.delete()
        return self.render_to_response({}, request)

# 商品分类
class ClassificationView(StatusWrapMixin, viewsets.ModelViewSet):
    queryset = Classification.objects.filter()
    serializer_class = ClassificationSerializers
    def get_queryset(self):
        return Classification.objects.all()
    def list(self, request, *args, **kwargs):
        data_list = self.get_serializer(self.get_queryset(), many=True)
        return self.render_to_response(data_list.data,self.request)

# 商品列表
class GoodView(StatusWrapMixin, viewsets.ModelViewSet):
    queryset = Good.objects.order_by('-priority')
    serializer_class = GoodSerializers

    def get_queryset(self):
        return Good.objects.order_by('-priority')


    def list(self, request, *args, **kwargs):
        """
        @apiVersion 1.0.0
        @api {get} /api/v1/good 商品接口
        @apiName get good
        @apiGroup good
        @apiDescription  获得商品列表
        @apiParamExample Request (example):
            /api/v1/good
        @apiSuccessExample {json} Success-Response (example):
            HTTP/1.1 200 OK
            {
            "body": [
                {
                "id": 15,
                "order_num": "453453242",
                "is_check": true,
                "express_num": "12345",
                "express_cost": 12,
                "store_belong": {
                    "id": 1,
                    "name": "小王",
                    "store_name": "某某门店",
                    "virtual_coin_limit": 1,
                    "virtual_coin_canuse": 49948,
                    "is_check": true,
                    "account": "152011931491",
                    "selleruser_info": "销售1",
                    "create_time": "2019-01-30 10:42:00",
                    "address": null
                },]
            }
        """
        class_list = Classification.objects.all()
        class_data_list = ClassificationSerializers(class_list,many=True).data
        for i in range(len(class_data_list)):
            good_query = self.get_queryset().filter(classification=class_data_list[i].get('id'))
            class_data_list[i]['good'] = self.get_serializer(good_query, many=True).data
        return self.render_to_response(class_data_list,self.request)


# 订单列表
class OrderView(StatusWrapMixin, viewsets.ModelViewSet):
    queryset = Order.objects.order_by('-create_time')
    serializer_class = OrderSerializers
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('order_status',)

    def get_queryset(self):
        return Order.objects.order_by('-create_time')

    def list(self, request, *args, **kwargs):

        """
        @apiVersion 1.0.0
        @api {get} /api/v1/order 订单接口

        @apiGroup order
        @apiDescription  获得订单列表
        @apiParam {Int} store_id 终端店id,可不填
        @apiParam {Int} selleruser_id 销售代表id，可不填
        @apiParamExample Request (example):
            /api/v1/order?store_id=1
        @apiSuccessExample {json} Success-Response (example):
            HTTP/1.1 200 OK
            {
            "body": [
                {
                "id": 15,
                "order_num": "453453242",
                "is_check": true,
                "express_num": "12345",
                "express_cost": 12,
                "store_belong": {
                    "id": 1,
                    "name": "小王",
                    "store_name": "某某门店",
                    "virtual_coin_limit": 1,
                    "virtual_coin_canuse": 49948,
                    "is_check": true,
                    "account": "152011931491",
                    "selleruser_info": "销售1",
                    "create_time": "2019-01-30 10:42:00",
                    "address": null
                },]
            }
        """


        self.queryset = self.filter_queryset(self.get_queryset())
        store_id = self.request.GET.get('store_id')
        selleruser_id = self.request.GET.get('selleruser_id')
        if store_id:
            data_list_queryset = self.queryset.filter(store_belong=Store.objects.get(id=int(store_id)))
        elif selleruser_id:
            data_list_queryset = self.queryset.filter(check_user=SellerUser.objects.get(id=int(selleruser_id)))
        else:
            data_list_queryset = self.queryset
        total_data = len(data_list_queryset)
        if self.request.GET.get('page_size') and self.request.GET.get('page_num'):
            data_list_queryset, page_sum = cutpage(data_list_queryset, self.request.GET.get('page_num'),
                                                   self.request.GET.get('page_size'))
        else:
            page_sum = 1
        data_list = self.get_serializer(data_list_queryset, many=True)
        return self.render_to_response(data_list.data,self.request,page_sum,total_data)


# 搜索订单 eg  http://127.0.0.1:8000/api/v1/search_order/?selleruser_id=1&search=某某&date=2019-1-28
from rest_framework import filters
class SearchOrderView(StatusWrapMixin, viewsets.ModelViewSet):
    queryset = Order.objects.order_by('-create_time')
    serializer_class = OrderSerializers
    filter_backends = (filters.SearchFilter,)
    search_fields = ('store_belong__store_name',)
    def get_queryset(self):
        return Order.objects.filter(order_status=self.request.GET.get('order_status')).order_by('-create_time')

    def list(self, request, *args, **kwargs):
        is_check = self.request.GET.get('store_id')
        self.queryset = self.filter_queryset(self.get_queryset())
        selleruser_id = self.request.GET.get('selleruser_id')
        data_list_queryset = self.queryset.filter(check_user=SellerUser.objects.get(id=int(selleruser_id)))
        date = self.request.GET.get('date')

        if date:
            start_time = datetime.strptime(date, '%Y-%m-%d')
            end_time = start_time+timedelta(days=1)
            data_list_queryset = data_list_queryset.filter(create_time__gte=start_time,create_time__lte=end_time)
        total_data = len(data_list_queryset)
        if self.request.GET.get('page_size') and self.request.GET.get('page_num'):
            data_list_queryset, page_sum = cutpage(data_list_queryset, self.request.GET.get('page_num'),
                                                   self.request.GET.get('page_size'))
        else:
            page_sum = 1
        data_list = self.get_serializer(data_list_queryset, many=True)
        return self.render_to_response(data_list.data,self.request,page_sum,total_data)

# 提交订单
class SendOrderView(StatusWrapMixin,APIView):
    def post(self,request):
        if not self.check_token(self.request):
            return self.render_to_response({},self.request)
        data1 = request.body
        data = json.loads(data1.decode('utf-8'))
        print 'data--', data
        store_id = data.get('store_id')
        sc_list = data.get('sc_list')  #购物车列表
        order_num = data.get('order_num') #订单号
        total_price = data.get('total_price')  # 总价
        deliveryaddress_id = data.get('deliveryaddress_id')

        store = Store.objects.get(id=int(store_id))

        if not all([store_id, order_num,total_price,deliveryaddress_id,sc_list]):
            return Response({'body': {}, 'status': ERROR_PARAMETER, 'msg': 'param loss'})

        deliveryaddress = DeliveryAddress.objects.get(id=int(deliveryaddress_id))
        address = '收货人-{0}，收货人电话-{1}，收货地址-{2}'.format(deliveryaddress.name,deliveryaddress.phone,
                                                   deliveryaddress.area_address+deliveryaddress.detail_address)

        if len(sc_list) == 0:
            return Response({'body': {}, 'status': ERROR_INFO, 'msg': 'no shoppingcards'})

        if store.is_check==False:
            return Response({'body': {}, 'status': ERROR_NOCHECK, 'msg': 'no check'})

        if total_price>store.virtual_coin_canuse:
            return Response({'body': {}, 'status': ERROR_INFO, 'msg': 'limit not enough'})

        for sc_id in sc_list:
            sc = ShoppingCard.objects.get(id=int(sc_id))
            good = sc.good
            if good.current_nums < sc.numbers:
                return Response({'body': {}, 'status': ERROR_INFO, 'msg': 'inventory not enough'})  # 库存不足
        order = Order(order_num=order_num,store_belong=store,total_price=total_price,check_user=store.selleruser,address=address)

        order.save()

        # 减去额度
        store.virtual_coin_canuse -= total_price
        store.save()

        for sc_id in sc_list:
            sc = ShoppingCard.objects.get(id=int(sc_id))
            OrderItem(good=sc.good,numbers=sc.numbers,belong = order,total_price=sc.total_price).save()
            sc.delete()
        return self.render_to_response({},request)

#销售代表审核订单
class CheckOrderView(StatusWrapMixin,APIView):
    def post(self,request):
        if not self.check_token(self.request):
            return self.render_to_response({},self.request)
        data1 = request.body
        data = json.loads(data1.decode('utf-8'))
        print 'data--', data
        order_id = data.get('order_id')
        express_num = data.get('express_num')
        express_cost = data.get('express_cost')
        order = Order.objects.get(id=int(order_id))
        store = order.store_belong
        if store.virtual_coin_canuse < order.total_price:
            return Response({'body': {}, 'status': ERROR_INFO, 'msg': 'insufficient quota'})
        if express_num:
            order.express_num = express_num
        if express_cost:
            order.express_cost = express_cost
        order.order_status = 1
        order.save()

        return self.render_to_response({},request)

#销售代表驳回订单
class RevokeOrderView(StatusWrapMixin,APIView):
    def post(self,request):
        if not self.check_token(self.request):
            return self.render_to_response({},self.request)
        data1 = request.body
        data = json.loads(data1.decode('utf-8'))
        print 'data--', data
        order_id = data.get('order_id')
        order = Order.objects.get(id=int(order_id))
        store = order.store_belong
        store.virtual_coin_canuse += order.total_price
        store.save()
        order.order_status = 2
        order.save()
        return self.render_to_response({}, request)




# 订单详情
class OrderItemView(StatusWrapMixin, viewsets.ModelViewSet):
    queryset = OrderItem.objects.filter()
    serializer_class = OrderItemSerializers

    def get_queryset(self):
        return OrderItem.objects.filter()

    def list(self, request, *args, **kwargs):
        order_id = self.request.GET.get('order_id')
        order = Order.objects.get(id=int(order_id))
        data_list_queryset = self.get_queryset().filter(belong=Order.objects.get(id=int(order_id)))
        data_list = self.get_serializer(data_list_queryset,many=True)
        order_info = OrderSerializers(order)
        data={'orderitem_list':data_list.data,'order_info':order_info.data}
        return self.render_to_response(data,self.request)

import pdb

# pdb.set_trace()#放到return之前，然后执行p xxx 查看xxx变量，执行c继续下一步
# 购物车列表
class ShoppingCardView(StatusWrapMixin, viewsets.ModelViewSet):
    queryset = ShoppingCard.objects.order_by('-create_time')
    serializer_class = ShoppingCardSerializers
    def get_queryset(self):
        return ShoppingCard.objects.order_by('-create_time')

    def list(self, request, *args, **kwargs):

        store_id = self.request.GET.get('store_id')

        data_list_queryset = self.get_queryset().filter(store=Store.objects.get(id=int(store_id)))
        data_list = self.get_serializer(data_list_queryset, many=True)
        final_data = data_list.data
        for ele in final_data:
            ele.get('good')['quantity'] = ele.get('numbers')
        return self.render_to_response(final_data,self.request)


# 创建购物车
class CreateShoppingCardView(StatusWrapMixin, APIView):
    def post(self, request):
        if not self.check_token(self.request):
            return self.render_to_response({},self.request)
        data1 = request.body
        data = json.loads(data1.decode('utf-8'))
        print 'data--', data
        store_id = data.get('store_id')
        good_id = data.get('good_id')
        good = Good.objects.get(id=int(good_id))
        store = Store.objects.get(id=int(store_id))
        shoppingcard = ShoppingCard.objects.filter(good=good,store=store).first()
        if shoppingcard:
            shoppingcard.numbers+=1
            shoppingcard.save()
        else:
            shoppingcard = ShoppingCard(good=good, numbers=1,store=store)
            shoppingcard.save()
        return self.render_to_response({'shoppingcard':shoppingcard.id},request)

class MinusShoppingCardView(StatusWrapMixin, APIView):
    def post(self,request):
        if not self.check_token(self.request):
            return self.render_to_response({},self.request)
        data1 = request.body
        data = json.loads(data1.decode('utf-8'))
        print 'data--', data
        store_id = data.get('store_id')
        good_id = data.get('good_id')
        good = Good.objects.get(id=int(good_id))
        store = Store.objects.get(id=int(store_id))
        shoppingcard = ShoppingCard.objects.filter(good=good, store=store).first()
        if shoppingcard:
            if shoppingcard.numbers > 0:
                shoppingcard.numbers -= 1
                shoppingcard.save()
                return self.render_to_response({}, request)
            else:
                return Response({'body': {}, 'status': ERROR_PARAMETER, 'msg': 'number is less than one'})
        else:
            return Response({'body': {}, 'status': ERROR_PARAMETER, 'msg': 'no shoppingcard'})


# 删除购物车
class DeleteShoppingCardView(StatusWrapMixin, APIView):
    def post(self, request):
        if not self.check_token(self.request):
            return self.render_to_response({},self.request)
        data1 = request.body
        data = json.loads(data1.decode('utf-8'))
        print 'data--', data
        sc_list = data.get('sc_list')
        for sc_id in sc_list:
            ShoppingCard.objects.get(id=int(sc_id)).delete()
        return self.render_to_response({},request)





#修改商品信息
class ChangeInventoryView(StatusWrapMixin,APIView):
    def post(self, request):
        if not self.check_token(self.request):
            return self.render_to_response({},self.request)
        data1 = request.body
        data = json.loads(data1.decode('utf-8'))
        print 'data--', data
        good_id = data.get('good_id')
        current_nums = int(data.get('current_nums'))
        good = Good.objects.get(id=int(good_id))
        good.current_nums = current_nums
        good.save()
        return self.render_to_response({}, request)


# 增加商品信息
class AddGoodView(StatusWrapMixin,APIView):
    def post(self, request):
        if not self.check_token(self.request):
            return self.render_to_response({},self.request)

        data1 = request.body
        data = json.loads(data1.decode('utf-8'))
        # data1 = request.POST
        # data = json.loads(data1.decode('utf-8'))
        print 'data--', data
        name = data.get('name')
        picture = request.FILES.get('picture')
        current_nums = int(data.get('current_nums'))
        unit = data.get('unit')
        price = round(float(data.get('price')),2)
        classification_id = data.get('classification_id')

        if not all([name, current_nums,unit,price,classification_id]):
            return Response({'body': {}, 'status': ERROR_PARAMETER, 'msg': 'param loss'})
        if picture:
            Good(name=name,picture=picture,unit=unit,price=price,current_nums=current_nums,
                 classification=Classification.objects.get(id=int(classification_id))).save()
        else:
            Good(name=name, unit=unit, price=price, current_nums=current_nums,
                 classification=Classification.objects.get(id=int(classification_id))).save()
        from django.shortcuts import render,redirect
        # return redirect('http://shop-xj.chafanbao.com/store/stock/add',{'header':})
        # return self.render_to_response({}, request)

class AddPictureView(StatusWrapMixin,APIView):
    def post(self, request):
        a = request.FILES.get('picture_url')
        print a
        print request.POST
        good_id = request.POST.get('good_id')
        print good_id
        good = Good.objects.get(id=int(good_id))
        good.picture_url=a
        good.save()
        return self.render_to_response({}, request)





class CreateSelleruser(StatusWrapMixin,APIView):
    def post(self,request):
        if not self.check_token(self.request):
            return self.render_to_response({},self.request)
        data1 = request.body
        data = json.loads(data1.decode('utf-8'))
        print 'data--', data
        if SellerUser.objects.filter(account=data.get('account')):
            return Response({'body': {}, 'status': ERROR_PARAMETER, 'msg': 'account repeat'})
        SellerUser(**data).save()
        return self.render_to_response({}, request)


class DownloadOrderExcelView(StatusWrapMixin,APIView):
    def get(self,request):
        # if not self.check_token(self.request):
        #     return self.render_to_response({},self.request)
        data = request.GET
        oid = data.get('oid')
        order = Order.objects.get(id=oid)
        create_time = order.create_time
        order_datetime = create_time.strftime("%Y-%m-%d")
        store_username = order.store_belong.name
        store_name = order.store_belong.store_name
        selleruser_name = order.check_user.name
        t = str(int(time.time()))
        response = HttpResponse(content_type='application/msexcel')
        response['Content-Disposition'] = 'attachment; filename='+t+'.xls'

        import xlwt
        workbook = xlwt.Workbook(encoding='utf-8')
        worksheet = workbook.add_sheet('My Worksheet')

        style1 = xlwt.XFStyle()
        al = xlwt.Alignment()
        al.horz = 0x02  # 设置水平居中
        al.vert = 0x01  # 设置垂直居中
        style1.alignment = al
        font = xlwt.Font()
        font.bold = True
        font.height = 0x00E8
        style1.font = font

        style2 = xlwt.XFStyle()
        al = xlwt.Alignment()
        al.horz = 0x02  # 设置水平居中
        al.vert = 0x01  # 设置垂直居中
        style2.alignment = al

        worksheet.write_merge(0, 0, 0, 5, u'新疆润滑油分公司促销品申请单', style1)
        worksheet.write(1, 4, u'编号')
        worksheet.write(1, 5, u'01')
        worksheet.write(2, 0, u'申请人')
        worksheet.write(2, 1, store_username)
        worksheet.write(2, 2, u'日期')
        worksheet.write(2, 3, order_datetime)
        worksheet.write(2, 4, u'销售组')
        worksheet.write(3, 0, u'申请事由')
        worksheet.write_merge(3, 3, 1, 5, u' ')
        worksheet.write_merge(4, 17, 0, 5, u' ',)
        worksheet.write(18, 0, u'促销品领取名称')
        worksheet.write(18, 1, u'单位')
        worksheet.write(18, 2, u'类型')
        worksheet.write(18, 3, u'数量')
        worksheet.write_merge(18, 18, 4, 5, u'领取人签名')
        worksheet.write_merge(19, 20, 4, 5, store_username,style2)
        orderitem = order.belong_orderitem.all()
        datalist = OrderItemSerializers(orderitem,many=True)


        num = 19
        sum = 0
        for i in datalist.data:
            worksheet.write(num, 0, i.get('good').get('name'))
            worksheet.write(num, 1, store_name)
            worksheet.write(num, 2, i.get('good').get('classification').get('name'))
            worksheet.write(num, 3, str(i.get('numbers')))
            num+=1
            sum+=i.get('numbers')

        worksheet.write(num, 0, u'走访单位名称/个人')
        worksheet.write(num, 1, u'电话')
        worksheet.write(num, 2, u'发放类型')
        worksheet.write(num, 3, u'发放数量')
        worksheet.write(num+1, 2, u'促销品')
        worksheet.write(num+1, 3, str(sum))

        worksheet.write(num+4, 0, u'部门领导签字')
        worksheet.write(num+4, 3, u'销售经理签字')
        worksheet.write(num + 5, 3, selleruser_name)
        workbook.save(response)
        return response


from xjmallapp.tasks import send
class TestView(APIView):

    #获取用户ip
    def get_client_ip(self,request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def get(self,request):
        data = self.request.GET
        get_uri = request.build_absolute_uri.im_self.path  #获取请求的接口最后的/后面的内容
        end_uri = get_uri.split('/')[-1]
        print end_uri
        print self.get_client_ip(request)
        phone = data.get('phone')
        # send.delay(phone=phone)
        return JsonResponse({'msg':'ok'})

#一对一查询
class TestGood(APIView):
    def get(self,request):
        data= request.GET
        id = data.get('id')
        good = Good.objects.get(id=int(id))
        # good.delete()  #删除连带着关联它的也删除

        print dir(good.code_good)
        print good.code_good.name  #因为就一个，所以没有.all()之类的
        print type(good.code_good)

        return JsonResponse({'msg':'ok'})

#多对多查询
class TestMany(APIView):
    def get(self,request):
        data = request.GET
        id = data.get('id')
        # category = Category.objects.get(id=id)
        # good_queryset = category.good.all()   #正向
        # print good_queryset
        good = Good.objects.get(id=id)
        category_queryset = good.category_good.all()      #反向
        print category_queryset
        return JsonResponse({'msg':'ok'})

#多对多增删
class GoodAdd(APIView):
    def get(self,request):

        good = Good.objects.first()
        # Category(name='车用品').save()   #保存不需要添加外健的字段

        # Category.objects.get(id=3).good.add(good)  #添加多对多"关系"
        # Category.objects.get(id=3).good.remove(good)  #删除多对多"关系"
        return JsonResponse({'msg':'ok'})






