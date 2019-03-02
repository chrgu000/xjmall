# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.response import Response
from xjmallapp.models import *

INFO_SUCCESS = 1  # 成功
ERROR_LOGIN = 2  # 登录错误
ERROR_PARAMETER = 3  # post请求参数错误
ERROR_INFO = 4  # 信息错误
ERROR_NOCHECK = 5  # 终端店未被审核
ERROR_ACCOUNTREPEAT = 6  # 重复注册


class StatusWrapMixin(object):
    status_code = INFO_SUCCESS
    message = 'success'

    def render_to_response(self, context,request,page_sum=None,total_data = None):
        data_context = self.wrapper(context,request,page_sum,total_data)
        return Response(data_context)

    def wrapper(self, context,request,page_sum,total_data):
        return_data = dict()
        return_data['body'] = context
        if page_sum:
            return_data['page_sum'] =page_sum
        if page_sum:
            return_data['total_data'] =total_data
        return_data['status'] = self.status_code
        return_data['msg'] = self.message
        if not self.check_token(request):
            return_data['status'] = ERROR_LOGIN
            return_data['body'] = {}
            return_data['msg'] = 'not login'
        return return_data

    def check_token(self, request):
        self.token = request.META.get("HTTP_SPL_TOKEN")
        print 'usertoken--',self.token
        sellerUsertokens = SellerUserToken.objects.filter(token=self.token).first()
        storetokens = StoreToken.objects.filter(token=self.token).first()
        if (not storetokens and not sellerUsertokens) or not self.token:
            return True
        return True
