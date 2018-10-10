# coding=utf-8
# __project__ = " "
# __author__ = "Nicksphere"
# __time__ = 2018/10/10 19:50
# __description__ = "订阅者1"


import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

channel = connection.channel()

channel.exchange_declare(exchange='direct_test',
                         type='direct')

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
