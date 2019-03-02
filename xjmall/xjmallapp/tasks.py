# coding:utf-8
# Create your tasks here
# from __future__ import absolute_import, unicode_literals
#
# from celery import shared_task
#
# from core.send_message import client_post_formurlencodeddata_requests
#
# @shared_task()
# def send_message(phone):
#     client_post_formurlencodeddata_requests(phone)
#     return 1

from celery import task

# celery1 = Celery("abc", backend='redis://localhost:6379/2', broker='redis://localhost:6379/2')
#
# from core.send_message import client_post_formurlencodeddata_requests
# import time
# @celery1.task()
# def send_message(phone):
#     time.sleep(10)
#     client_post_formurlencodeddata_requests(phone)
#     return 1
from core.send_message import client_post_formurlencodeddata_requests
import time


from celery.utils.log import get_task_logger
logger = get_task_logger('myapp')


@task
def send(phone):
    time.sleep(2)
    # logger.error("1111111")
    client_post_formurlencodeddata_requests(phone)
    return True



# 命令行执行nohup python manage.py celery worker -c 4 --loglevel=info 生成一个nohup.out可查看日志
# 或者指定celery的输出文件nohup python manage.py celery worker -c 4 --loglevel=info >> celery.log

