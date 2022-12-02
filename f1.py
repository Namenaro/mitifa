from sampler import *
from context import *

import random
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import f1_score


def binarization(true_class_train, contrast_class_train, test_sample):
    bin_edges_true = np.histogram(true_class_train)
    count_true, bins_true = np.histogram(true_class_train, bins=bin_edges_true[1],
                                         weights=np.ones_like(true_class_train) / len(true_class_train))
    bin_edges_contrast = np.histogram(contrast_class_train)
    count_contrast, bins_contrast = np.histogram(contrast_class_train, bins=bin_edges_contrast[1],
                                                 weights=np.ones_like(contrast_class_train) / len(contrast_class_train))

    test_binary = []
    for i in test_sample:
        bin_true = np.digitize(i, bins_true) - 1
        bin_contrast = np.digitize(i, bins_contrast) - 1

        if bins_true[0] <= i <= bins_true[-1] and bins_contrast[0] <= i <= bins_contrast[-1]:
            if i == bins_true[-1]:
                bin_true = -1
            count_true = list(count_true)
            true_height = count_true[bin_true]
            if i == bins_contrast[-1]:
                bin_contrast = -1
            count_contrast = list(count_contrast)
            contrast_height = count_contrast[bin_contrast]
            if contrast_height > true_height:
                i = 0
            else:
                i = 1
        elif bins_true[0] <= i <= bins_true[-1]:
            i = 1
        elif bins_contrast[0] <= i <= bins_contrast[-1]:
            i = 0
        elif i <= bins_true[0] or i >= bins_true[-1] and i <= bins_contrast[0] or i >= bins_contrast[-1]:
            if (abs(i - bins_true[0]) or abs(i - bins_true[-1])) <= (
                    abs(i - bins_contrast[0]) or abs(i - bins_contrast[-1])):
                i = 1
            else:
                i = 0
        test_binary.append(i)

    return test_binary


def evaluate_F1(true_class_train, contrast_class_train, true_class_test, contrast_class_test):
    #     # Построение гистограммы для трейна
    #     plt.hist(true_class_train, edgecolor="black", weights=np.ones_like(true_class_train) / len(true_class_train),
    #              alpha=0.5, label='true_class_train', color='green')
    #     plt.hist(contrast_class_train, edgecolor="black",
    #              weights=np.ones_like(contrast_class_train) / len(contrast_class_train),
    #              alpha=0.5, label='contrast_class_train', color='red')
    #     plt.legend()
    #     plt.show()

    #     # Построение гистограммы для теста
    #     plt.hist(true_class_test, edgecolor="black", weights=np.ones_like(true_class_test) / len(true_class_test),
    #              alpha=0.5, label='true_class_test', color='green')
    #     plt.hist(contrast_class_test, edgecolor="black", weights=np.ones_like(contrast_class_test) / len(contrast_class_test),
    #              alpha=0.5, label='contrast_class_test', color='red')
    #     plt.legend()
    #     plt.show()

    true_class_test_binary_classifier = binarization(true_class_train, contrast_class_train, true_class_test)
    contrast_class_test_binary_classifier = binarization(true_class_train, contrast_class_train, contrast_class_test)

    true_class_test_binary_input = []
    for i in true_class_test:
        i = 1
        true_class_test_binary_input.append(i)

    contrast_class_test_binary_input = []
    for i in contrast_class_test:
        i = 0
        contrast_class_test_binary_input.append(i)

    test_classifier = true_class_test_binary_classifier + contrast_class_test_binary_classifier
    test_input = true_class_test_binary_input + contrast_class_test_binary_input

    F1_score = f1_score(test_input, test_classifier)
    return F1_score


def eval_struct_f1(basic_struct, context):
    true_class_train = sample_non_triviality_values_for_basic_struct(basic_struct, context.train_maps)
    contrast_class_train = sample_non_triviality_values_for_basic_struct(basic_struct, context.contrast_maps)
    true_class_test =sample_non_triviality_values_for_basic_struct(basic_struct, context.test_maps)
    test_contrast = context.get_more_contrast(num_cogmaps=30)
    contrast_class_test = sample_non_triviality_values_for_basic_struct(basic_struct, test_contrast)

    F1_score = evaluate_F1(true_class_train, contrast_class_train, true_class_test, contrast_class_test)
    return F1_score