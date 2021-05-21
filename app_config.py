# -*- coding: utf-8 -*-
import os
import time

class Config(object):

    base_dir=(os.path.abspath(os.curdir))
    #inception模型
    model_file = "/media/yolov3_crop/model/inceptionv3/inceptionv3_classify.pb"
    #inception标签
    label_file = "/media/yolov3_crop/model/inceptionv3/inceptionv3_labels.txt"
    #inception节点
    INCEPTION_V3 = "InceptionV3/Predictions/Reshape_1:0"
    #yolo模型
    pb_file = "/media/yolov3_crop/model/yolov3/yolov3_plate.pb"
    #yolo标签
    classes_file = "/media/yolov3_crop/model/yolov3/yolov3_plate.names"
    #yolo节点
    return_elements = ["input/input_data:0", "pred_sbbox/concat_2:0",
                       "pred_mbbox/concat_2:0", "pred_lbbox/concat_2:0"]
    #ocr配置文件
    config_file = "/media/yolov3_crop/model_config.yml"
    #初始化图片
    test_img = "/media/yolov3_crop/ppocr/img/225.jpg"
    #日志记录
    log_dir = '/media/yolov3_crop/log/'




    class ConstError(TypeError):
        pass

    class ConstCaseError(ConstError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
          raise self.ConstError("can't change const %s" % name)
        if not name.isupper():
          raise self.ConstCaseError('const name "%s" is not all uppercase' % name)
        self.__dict__[name] = value



