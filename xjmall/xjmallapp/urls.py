# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import views
from rest_framework import routers
from django.conf.urls import url, include

router1 = routers.DefaultRouter()

router1.register(r'selleruser', views.SellerUserView)
router1.register(r'store', views.StoreView)
router1.register(r'good', views.GoodView)
router1.register(r'order', views.OrderView)
router1.register(r'search_order', views.SearchOrderView)
router1.register(r'item_order', views.OrderItemView)
router1.register(r'shopping_card', views.ShoppingCardView)
router1.register(r'deliveryaddresslist', views.DeliveryaddressListView)
router1.register(r'classificationlist', views.ClassificationView)

urlpatterns = [
    url(r'^', include(router1.urls)),
    url(r'^register', views.RegisterView.as_view(), name='register'),
    url(r'^send_ic', views.SendICView.as_view(), name='send_ic'),
    url(r'^login_store', views.LoginStoreView.as_view(), name='login_store'),
    url(r'^login_selleruser', views.LoginSellerUserView.as_view(), name='login_selleruser'),
    url(r'^change_password', views.ChangePasswordView.as_view(), name='change_password'),
    url(r'^create_deliveryaddress', views.CreateDeliveryAddressView.as_view(), name='create_deliveryaddress'),
    url(r'^change_deliveryaddress', views.ChangeDeliveryAddressView.as_view(), name='change_deliveryaddress'),
    url(r'^check_store', views.CheckStoreView.as_view(), name='check_store'),
    url(r'^revoke_store', views.RevokeStoreView.as_view(), name='revoke_store'),
    url(r'^send_order', views.SendOrderView.as_view(), name='send_order'),
    url(r'^check_order', views.CheckOrderView.as_view(), name='check_order'),
    url(r'^create_shoppingcard', views.CreateShoppingCardView.as_view(), name='create_shoppingcard'),
    url(r'^minus_shoppingcard', views.MinusShoppingCardView.as_view(), name='minus_shoppingcard'),
    url(r'^delete_shoppingcard', views.DeleteShoppingCardView.as_view(), name='delete_shoppingcard'),
    url(r'^change_inventory', views.ChangeInventoryView.as_view(), name='change_inventory'),
    url(r'^add_good', views.AddGoodView.as_view(), name='add_good'),
    url(r'^create_selleruser', views.CreateSelleruser.as_view(), name='create_selleruser'),
    url(r'^download_order', views.DownloadOrderExcelView.as_view(), name='download_order'),
    url(r'^retrieve_password', views.RetrievePasswordView.as_view(), name='retrieve_password'),
    url(r'^set_defaultaddress', views.SetDefaultAddressView.as_view(), name='set_defaultaddress'),
    url(r'^delete_deliveryaddress', views.DeleteDeliveryAddress.as_view(), name='delete_deliveryaddress'),
    url(r'^revoke_order', views.RevokeOrderView.as_view(), name='revoke_order'),
    url(r'^add_picture', views.AddPictureView.as_view(), name='add_picture'),
    url(r'^test', views.TestView.as_view(), name='test'),
    url(r'^tgood', views.TestGood.as_view(), name='tgood'),
    url(r'^tmany', views.TestMany.as_view(), name='tmany'),
    url(r'^goodadd', views.GoodAdd.as_view(), name='goodadd'),
]




