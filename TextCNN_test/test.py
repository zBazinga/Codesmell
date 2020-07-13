# -*- coding: utf-8 -*-
# @Time    : 2020/6/17 8:53 下午
# @Author  : Learning

import torch.nn.functional as F
import torch as t
a = t.rand(128, 10)
b = t.rand(128)
loss = F.cross_entropy(a, b)
print(loss.item())
def result(pred,tag):
    TN, TP, FN, FP = 0
    for i in range(tag.shape[0]):
        if pred[i] == 0 and tag[i] == 0:
                TN += 1
        if pred[i] == 1 and tag[i] == 0:
                FN += 1
        if pred[i] == 0 and tag[i] == 1:
                FP += 1
        if pred[i] == 1 and tag[i] == 1:
                TP += 1
    precision = TP/(TP+FP)
    recall = TP/(TP+FN)
    f1 = 2*precision*recall/(precision+recall)
    return precision,recall,f1

