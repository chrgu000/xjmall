define({ "api": [  {    "version": "1.0.0",    "type": "get",    "url": "/api/v1/good",    "title": "商品接口",    "name": "get_good",    "group": "good",    "description": "<p>获得商品列表</p>",    "parameter": {      "examples": [        {          "title": "Request (example):",          "content": "/api/v1/good",          "type": "json"        }      ]    },    "success": {      "examples": [        {          "title": "Success-Response (example):",          "content": "HTTP/1.1 200 OK\n{\n\"body\": [\n    {\n    \"id\": 15,\n    \"order_num\": \"453453242\",\n    \"is_check\": true,\n    \"express_num\": \"12345\",\n    \"express_cost\": 12,\n    \"store_belong\": {\n        \"id\": 1,\n        \"name\": \"小王\",\n        \"store_name\": \"某某门店\",\n        \"virtual_coin_limit\": 1,\n        \"virtual_coin_canuse\": 49948,\n        \"is_check\": true,\n        \"account\": \"152011931491\",\n        \"selleruser_info\": \"销售1\",\n        \"create_time\": \"2019-01-30 10:42:00\",\n        \"address\": null\n    },]\n}",          "type": "json"        }      ]    },    "filename": "xjmallapp/views.py",    "groupTitle": "good",    "sampleRequest": [      {        "url": "http://127.0.0.1:8000/api/v1/good"      }    ]  },  {    "version": "1.0.0",    "type": "get",    "url": "/api/v1/order",    "title": "订单接口",    "group": "order",    "description": "<p>获得订单列表</p>",    "parameter": {      "fields": {        "Parameter": [          {            "group": "Parameter",            "type": "Int",            "optional": false,            "field": "store_id",            "description": "<p>终端店id,可不填</p>"          },          {            "group": "Parameter",            "type": "Int",            "optional": false,            "field": "selleruser_id",            "description": "<p>销售代表id，可不填</p>"          }        ]      },      "examples": [        {          "title": "Request (example):",          "content": "/api/v1/order?store_id=1",          "type": "json"        }      ]    },    "success": {      "examples": [        {          "title": "Success-Response (example):",          "content": "HTTP/1.1 200 OK\n{\n\"body\": [\n    {\n    \"id\": 15,\n    \"order_num\": \"453453242\",\n    \"is_check\": true,\n    \"express_num\": \"12345\",\n    \"express_cost\": 12,\n    \"store_belong\": {\n        \"id\": 1,\n        \"name\": \"小王\",\n        \"store_name\": \"某某门店\",\n        \"virtual_coin_limit\": 1,\n        \"virtual_coin_canuse\": 49948,\n        \"is_check\": true,\n        \"account\": \"152011931491\",\n        \"selleruser_info\": \"销售1\",\n        \"create_time\": \"2019-01-30 10:42:00\",\n        \"address\": null\n    },]\n}",          "type": "json"        }      ]    },    "filename": "xjmallapp/views.py",    "groupTitle": "order",    "name": "GetApiV1Order",    "sampleRequest": [      {        "url": "http://127.0.0.1:8000/api/v1/order"      }    ]  }] });
