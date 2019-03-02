# -*- coding: utf-8 -*-

from models import Order,SellerUserToken,StoreToken
from datetime import datetime

#自动收货
def corn_auto_delivery():
    for order in Order.objects.filter(order_status=1):
        dt = datetime.now()
        interval_time = dt - order.modify_time
        print 'ordernum-{0},nowtime-{1},orderchecktime-{2},intervaltime-{3},' \
              'intervaldays-{4}'.format(order.order_num,datetime.now(),order.modify_time,
                                        interval_time, interval_time.days)
        if interval_time.days >= 7:
            order.order_status = 3
            order.save()
            print '订单{0}收货完成'.format(order.order_num)

def corn_clear_token():
    for usertoken in StoreToken.objects.all():
        dt = datetime.now()
        interval_time = dt - usertoken.create_time
        print 'storetoken-{0},nowtime-{1},tokentime-{2},intervaltime-{3},' \
              'intervaldays-{4}'.format(usertoken.token, datetime.now(), usertoken.create_time,
                                        interval_time, interval_time.days)
        if interval_time.days >= 10:
            usertoken.delete()
            print '清除'
    for usertoken in SellerUserToken.objects.all():
        dt = datetime.now()
        interval_time = dt - usertoken.create_time
        print 'sellerusertoken-{0},nowtime-{1},tokentime-{2},intervaltime-{3},' \
              'intervaldays-{4}'.format(usertoken.token, datetime.now(), usertoken.create_time,
                                        interval_time, interval_time.days)
        if interval_time.days >= 10:
            usertoken.delete()
            print '清除'


