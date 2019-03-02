# coding:utf-8

import json
import requests
import urllib
apikey = '81cadee3d99f15734ca02d65a4bfd78a'
template_id= '2737564'
url = 'https://sms.yunpian.com/v2/sms/tpl_single_send.json'

#终端店审核驳回
def send_revoke_store_message(phone):
    params =urllib.urlencode({'apikey': apikey,
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
    return json.loads(responsedata.encode('utf-8'))
