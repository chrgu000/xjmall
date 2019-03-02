# coding:utf-8

import json
import requests
import urllib
from func import create_ic
apikey = '81cadee3d99f15734ca02d65a4bfd78a'
template_id= '2734758'
url = 'https://sms.yunpian.com/v2/sms/tpl_single_send.json'
import redis

#发放验证码
def save_redis_ic(phone):
    ic = create_ic()
    r = redis.StrictRedis(host='localhost',port=6379,db=7)
    r.set(phone,ic,300)
    res = send_identifying_code(phone,ic)
    if res==200:
        return ic
    return False



def send_identifying_code(phone,ic):
    params =urllib.urlencode({ 'tpl_value':urllib.urlencode({'#code#':ic}),
                               'apikey': apikey,
                               'tpl_id': template_id,
                               'mobile': phone
                             })
    requestJSONdata = str(params).replace("+", "%2B")
    requestdata = requestJSONdata.encode("utf-8")
    head = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", 'Connection': 'close'}
    print 'client-server', requestdata
    r = requests.post(url, data=requestdata, headers=head)
    responsedata = r.text
    print 'server-client', responsedata
    print "get the status: ", r.status_code
    print json.loads(responsedata.encode('utf-8'))
    return r.status_code







