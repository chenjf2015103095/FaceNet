# -*- coding: utf-8 -*-
# Author :  chenjianfeng
# Time :    2021/4/22
# File:     rabbitmq_receive.py
# Software: PyCharm


import os
import cv2
import pika
import time
import random
from PIL import Image

Types={'jpg','JPG','PNG','png','JPEG','jpeg'}

class Rabbitmq(object):

    def __init__(self,
                 sUser,
                 sPwd,
                 sIP,
                 sPort,
                 sVHost,
                 sQueue_in,
                 sQueue_out,
                 sExchange,
                 sSave_dir):
        """
        初始rabbitmq服务配置参数

        :param sUser:
        :param sPwd:
        :param sIP:
        :param sPort:
        :param sHost:
        :param sQueeu_in:
        :param sQueue_out:
        :param sExchange:
        :param sSave_dir:
        """
        self.sUser = sUser
        self.sPwd = sPwd
        self.sIP = sIP
        self.sPort = sPort
        self.sVHost = sVHost
        self.sQueue_in = sQueue_in
        self.sQueue_out = sQueue_out
        self.sExchange = sExchange
        self.sSave_dir = sSave_dir
        self.afile_path = "/run/user/1000/gvfs/" \
                          "smb-share:server=192.168.0.180,share=capture/"



    def init_conn(self):
        """
        开始连接
        :return:
        """
        credentials = pika.PlainCredentials(self.sUser, self.sPwd)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.sIP,
                                                                       port=self.sPort,
                                                                       virtual_host=self.sVHost,
                                                                       credentials=credentials))
        channel = connection.channel()
        print(' [*] Waiting for messages. To exit press CTRL+C')
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
        ch.basic_ack(delivery_tag=method.delivery_tag)  # 向生产者发送确认消息
        body = bytes.decode(body)
        self.parse_body(body)
        print(type(body), len(body))
        time.sleep(0.1)
        print(" [x] Received %r" % (body,))


    def parse_body(self,body):
        """
        数据解析
        :param body:
        :return:
        """
        if body is not None:

            # try:
            #     res=body['url']
            #     image_id=res.split('/')[-1]
            #     image=cv2.imread(res)
            #     ran = random.randint(1000, 9999)
            #     if not os.path.exists(self.sSave_dir):
            #         os.mkdir(self.sSave_dir)
            #     cv2.imwrite(os.path.join(self.sSave_dir, '{0}.jpg'.format(image_id)),image)

            # except Exception as ex:
            #     print(ex)


            try:
                ext = body.split('\\')[-1].split('.')[-1]
                name = body.split('\\')[-1]
                if not os.path.exists(self.sSave_dir):
                    os.mkdir(self.sSave_dir)
                if ext in Types:
                    # afile_path= "/run/user/1000/gvfs/smb-share:server=192.168.0.180,share=capture/" + name
                    afile_path = self.afile_path + name
                    print(afile_path)
                    image = cv2.imread(afile_path)
                    print(image)
                    cv2.imwrite(os.path.join(self.sSave_dir, '{0}.jpg'.format(name)),image)

            except Exception as ex:
                print(ex)





    def start_conn(self):
        """
        开始连接
        :return:
        """
        channel=self.init_conn()
        channel.basic_consume(queue=self.sQueue_out,
                              on_message_callback=self.callback,
                              auto_ack=False)
        channel.basic_qos(prefetch_count=1) #公平调度
        channel.start_consuming()


if __name__=="__main__":

    sUser = 'ai.transport'
    sPwd = 'slife@123'
    sIP = '192.168.0.22'
    sPort = 5672
    sVHost = 'slife'
    sQueue_in = 'ai.transport.source'
    sQueue_out = 'ai.transport.result'
    sExchange = 'ai.transport'
    sSave_dir='/media/IMAGE/'

    rabbitmq=Rabbitmq(sUser = sUser,
                      sPwd = sPwd,
                      sIP = sIP,
                      sPort = sPort,
                      sVHost = sVHost,
                      sQueue_in = sQueue_in,
                      sQueue_out = sQueue_out,
                      sExchange = sExchange,
                      sSave_dir = sSave_dir)

    rabbitmq.start_conn()



# credentials = pika.PlainCredentials('ai.transport', 'slife@123')
# connection = pika.BlockingConnection(pika.ConnectionParameters(host = '192.168.0.22',
#                                                                port = 5672,
#                                                                virtual_host = 'slife',
#                                                                credentials = credentials))
# channel = connection.channel()
# print (' [*] Waiting for messages. To exit press CTRL+C')
#
# # 申明消息队列，消息在这个队列传递，如果不存在，则创建队列
# # channel.queue_declare(queue ='ai.transport.source')
# # 定义一个回调函数来处理消息队列中的消息，这里是打印出来
# def callback(ch, method, properties, body):
#     print(" [x] Received %r" % (body,))
#
# # 告诉rabbitmq，用callback来接收消息
# # channel.basic_consume('python-test',callback)
# channel.basic_consume(queue='ai.transport.source',
#                       on_message_callback=callback,
#                       auto_ack=True)
# # 开始接收信息，并进入阻塞状态，队列里有信息才会调用callback进行处理
# channel.start_consuming()