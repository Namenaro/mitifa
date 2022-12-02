from utils import *

import numpy as np
import random
import torchvision.datasets as datasets
import matplotlib.pyplot as plt

def get_train_test_contrast(class_num, contrast_sample_len):
    ominset = datasets.Omniglot(root='./data_om', download=True, transform=None)
    res = []
    for i in range(len(ominset)):
        if class_num == ominset[i][1]:
            res.append(ominset[i][0])
    contrast = []
    indexes = random.sample(range(0, len(ominset)), contrast_sample_len)

    for i in indexes:
        if class_num != ominset[i][1]:
            contrast.append(ominset[i][0])
    return res[:10], res[11:], contrast



def get_train_test_contrast_BIN(class_num, contrast_sample_len):
    train_pics, test_pics, contrast = get_train_test_contrast(class_num, contrast_sample_len)
    for i in range(len(train_pics)):
        train_pics[i]=binarise_img(train_pics[i])
    for i in range(len(test_pics)):
        test_pics[i]=binarise_img(test_pics[i])
    for i in range(len(contrast)):
        contrast[i]=binarise_img(contrast[i])
    return train_pics, test_pics, contrast


def get_all_pics_for_training(class_num, contrast_sample_len):
    all_train_pics, test_pics, contrast_pics = get_train_test_contrast_BIN(class_num, contrast_sample_len)
    etalon_pic = all_train_pics[0]
    train_pics = all_train_pics[1:]
    return etalon_pic, train_pics, test_pics, contrast_pics

def get_contrast(class_num, sample_len):
    ominset = datasets.Omniglot(root='./data_om', download=True, transform=None)
    indexes = random.sample(range(0, len(ominset)), sample_len)
    contrast = []
    for i in indexes:
        if class_num != ominset[i][1]:
            contrast.append(binarise_img(ominset[i][0]))
    return contrast
