# -*- coding:utf-8 -*-
# Author:  zhousf
# Date:    2019-02-15
# Description: MTCNN 人脸检测、对齐、裁剪
import config

if __name__ == '__main__':
    input_dir = '/media/ubutnu/fc1a3be7-9b03-427e-9cc9-c4b242cefbff/tf_facenet/facenet-master/src/align/data/lfw/lfw'
    output_dir = '/media/ubutnu/fc1a3be7-9b03-427e-9cc9-c4b242cefbff/tf_facenet/facenet-master/src/align/data/lfw/lfw_160'
    config.TRAIN_MODEL.align_dataset_mtcnn(input_dir=input_dir, output_dir=output_dir)
