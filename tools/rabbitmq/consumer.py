# coding=utf-8
# __project__ = " "
# __author__ = "Nicksphere"
# __time__ = 2018/10/10 19:50
# __description__ = "订阅者1"


import pika

username = 'rabbitfg'   #指定远程rabbitmq的用户名密码
pwd = '123'
user_pwd = pika.PlainCredentials(username, pwd)
connection = pika.BlockingConnection(pika.ConnectionParameters(host='39.104.161.3', credentials=user_pwd))
channel = connection.channel()
channel.exchange_declare(exchange='direct_test')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

severities = ['error', 'info', ]  # 绑定队列，并发送关键字error，info
for severity in severities:
    channel.queue_bind(exchange='direct_test',
                       queue=queue_name,
                       routing_key=severity)

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))


channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()
