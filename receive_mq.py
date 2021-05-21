# -*- coding: utf-8 -*-
# Author :  chenjianfeng
# Time :    2021/4/22
# File:     receive_mq.py
# Software: PyCharm

import os
import cv2
import pika
import time

Types={'jpg','JPG','PNG','png','JPEG'}

class Receive(object):

    def __init__(self):

        pass

    def init_conn(self):
        """
        建立连接
        :return:
        """

        connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='localhost'))
        channel = connection.channel()

        channel.queue_declare(queue='hello2',durable=True)

        print (' [*] Waiting for messages. To exit press CTRL+C')

        return channel


    def callback(self,ch, method, properties, body):
        """
        回调函数
        :param ch:
        :param method:
        :param properties:
        :param body:
        :return:
        """
        body_list=[]
        print (" [x] Received %r" % (body,))
        body=bytes.decode(body)
        ch.basic_ack(delivery_tag=method.delivery_tag)  #向生产者发送确认消息
        body_list.append(body)
        print(type(body_list), len(body_list))
        self.parse_body(body_list)


    def parse_body(self,body_list):
        """
        解析数据
        :param body_list:
        :return:
        """
        # body_list=[]
        save_dir='/media/car/0425'
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        if body_list is not None:
            for body in body_list:
                print(len(body),type(body))
                try:
                    name,ext=body.split('/')[-1].split('.')
                    if ext in Types:
                        jpg=body
                        img=cv2.imread(jpg)
                        cv2.imwrite(os.path.join(save_dir,'{0}'.format(name)+'.jpg'),img)

                except Exception as ex:
                    print(ex)



    def strat_conn(self):
        """
        开始接收
        :return:
        """
        channel=self.init_conn()
        channel.basic_consume(queue='hello2',
                              on_message_callback=self.callback,
                              auto_ack=False)

        channel.start_consuming()


if __name__=="__main__":
   receive= Receive()
   receive.strat_conn()


# connection = pika.BlockingConnection(pika.ConnectionParameters(
#         host='localhost'))
# channel = connection.channel()
#
# channel.queue_declare(queue='hello2',durable=True)
#
# print (' [*] Waiting for messages. To exit press CTRL+C')
#
# def callback(ch, method, properties, body):
#     """
#
#     :param ch:
#     :param method:
#     :param properties:
#     :param body:
#     :return:
#     """
#     print (" [x] Received %r" % (body,))
#     body=bytes.decode(body)
#     # time.sleep(0.2)
#     ch.basic_ack(delivery_tag=method.delivery_tag)  #向生产者发送确认消息
#     parse_body(body)
#
#
# def parse_body(body):
#     """
#
#     :param body:
#     :return:
#     """
#     body_list=[]
#     save_dir='/media/car/0425'
#     if not os.path.exists(save_dir):
#         os.makedirs(save_dir)
#     if body is not None:
#         print(len(body),type(body))
#         ext=body.split('/')[-1].split('.')[-1]
#         name=body.split('/')[-1].split('.')[0]
#         if ext in Types:
#             jpg=body
#             img=cv2.imread(jpg)
#             cv2.imwrite(os.path.join(save_dir,'{0}'.format(name)+'.jpg'),img)
#
#
# channel.basic_consume(queue='hello2',
#                       on_message_callback=callback,
#                       auto_ack=False)
#
# channel.start_consuming()
