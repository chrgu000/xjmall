# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.response import Response
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse,JsonResponse

class TokenVerify(MiddlewareMixin):
    def process_request(self,request):
        self.token = request.META.get("HTTP_SPL_TOKEN")
        print 'usertoken--', self.token
        if not self.token:
            return JsonResponse({'body': {}, 'status': 2, 'msg': 'login no'})

    # def process_response(self,request,response):
    #     print response
    #






