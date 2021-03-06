# coding=utf-8
# __project__ = " "
# __author__ = "Nicksphere"
# __time__ = 2018/10/10 19:55
# __description__ = "订阅者2"

# !/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

channel = connection.channel()

channel.exchange_declare(exchange='direct_test',
                         type='direct')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

severities = ['error', ]
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
