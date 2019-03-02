##新疆终端店项目
###启动项目：
python manage.py makemigrations
python manage.py migrate
python manage.py crontab add
进入uconf，执行uwsgi --ini uwsgi.ini

#如果用到celery
命令行执行nohup python manage.py celery worker -c 4 --loglevel=info 生成一个nohup.out可查看日志
或者指定celery的输出文件nohup python manage.py celery worker -c 4 --loglevel=info >> celery.log


###如果需要前后端联调apidoc：
apidoc -i myapp/ -o apidoc/ 生成apidoc目录
将api-doc.py里面的--monitor_path 默认改为项目的app目录
执行python api-doc.py  开始监听10777端口
