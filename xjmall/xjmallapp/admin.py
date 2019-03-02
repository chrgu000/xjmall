# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import *


# Register your models here.

@admin.register(SellerUser)
class SellerUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone','area','user_type')


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'store_name','virtual_coin_limit', 'virtual_coin_canuse', 'selleruser', 'is_check')
    list_filter = ('create_time', 'virtual_coin_limit', 'is_check')
    search_fields = ('name',)


@admin.register(DeliveryAddress)
class DeliveryAddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'store','phone','area_address','detail_address','is_default')


@admin.register(Good)
class GoodAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'current_nums', 'price', 'priority','picture')
    ordering = ('-priority','id')

@admin.register(GoodCode)
class GoodCodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code')
    ordering = ('id',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    ordering = ('id',)


@admin.register(Classification)
class ClassificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_num', 'express_num', 'store_belong', 'total_price','express_cost',
                    'check_user', 'create_time','order_status')
    list_filter = ('create_time',)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'good', 'numbers', 'belong','total_price')
    list_filter = ('create_time',)


@admin.register(ShoppingCard)
class ShoppingCardAdmin(admin.ModelAdmin):
    list_display = ('id', 'good', 'numbers', 'store','total_price')
    list_filter = ('create_time',)


# @admin.register(Message)
# class MessageAdmin(admin.ModelAdmin):
#     list_display = ('id', 'sendee', 'sender','create_time')
#     list_filter = ('create_time',)

@admin.register(SellerUserToken)
class SellerUserTokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'token', 'selleruser','create_time')
    list_filter = ('create_time',)

@admin.register(StoreToken)
class StoreTokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'token', 'store','create_time')
    list_filter = ('create_time',)
