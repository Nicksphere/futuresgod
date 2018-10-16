# coding=utf-8
# __project__ = " "
# __author__ = "Nicksphere"
# __time__ = 2018/10/10 19:28
# __description__ = "rabbitmq 生产者 "

import pika

username = 'rabbitfg'   #指定远程rabbitmq的用户名密码
pwd = '123'
user_pwd = pika.PlainCredentials(username, pwd)
connection = pika.BlockingConnection(pika.ConnectionParameters(host='39.104.161.3', credentials=user_pwd))
channel = connection.channel()

channel.exchange_declare(exchange='direct_test')

severity = 'login'  # 设置一个key,
severity = 'error'
message = 'xyz'
channel.basic_publish(exchange='direct_test',
                      routing_key=severity,
                      body=message)
print(" [x] Sent %r:%r" % (severity, message))
connection.close()
