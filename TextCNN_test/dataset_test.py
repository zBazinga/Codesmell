# -*- coding: utf-8 -*-
# @Time    : 2020/6/7 9:56 上午
# @Author  : Learning
from torchtext import data
import jieba
import logging
from config import Config
import torchtext
import torch
TEXT = torchtext.data.Field(sequential=True, lower=True)
LABEL = torchtext.data.LabelField(sequential=False, dtype=torch.int64)

train_dataset, test_dataset= torchtext.data.TabularDataset.splits(
    path="/Users/dashabi/Desktop/dataset_codesmell/10-fold-onesentence",  # 文件存放路径
    format="csv",  # 文件格式
    skip_header=True,
    train="train_all1.csv",
    # validation="data_test3.csv",
    test="test_all1.csv",
    fields = [('id',None), ('content', TEXT), ('tag', LABEL), ("move_tag", LABEL)]
    # fields=[('name', TEXT), ('label', None)]  # 定义数据对应的表头
)

vectors = torchtext.vocab.Vectors(name="word2vecNocopy.200d.txt", cache="./data/wordVectors")
TEXT.build_vocab(train_dataset,test_dataset, vectors=vectors)
LABEL.build_vocab(train_dataset,test_dataset)
print("train", len(TEXT.vocab))
print(len(LABEL.vocab))
#
# train_iter = data.BucketIterator(
#     train_dataset, 5, sort_key=lambda x: len(x.content))
# print(train_iter.__sizeof__())
test_iter = data.BucketIterator(
    test_dataset, 5)   # , sort_key=lambda x: len(x.content)

for batch in test_iter:
    print(len(batch))
    print(batch.dataset[0].content)
    print(batch.dataset[0].content)
    # print(batch.dataset[1].content)
    print(batch.dataset)
    a = batch.content
    print(a.size())
    print(TEXT.vocab.itos[4], TEXT.vocab.itos[116],)

    break




# TEXT2 = torchtext.data.Field(sequential=True, lower=True)  # tokenize=cut
# LABEL2 = torchtext.data.LabelField(sequential=False, dtype=torch.int64)
# train_dataset,  test_dataset = torchtext.data.TabularDataset.splits(
#         path="/Users/dashabi/Desktop/dataset_codesmell/10-fold-onesentence",  # 文件存放路径
#         format="csv",  # 文件格式
#         skip_header=True,  # 是否跳过表头，我这里数据集中没有表头，所以不跳过
#         train="train_all1.csv",
#         # validation=config.dev_name,
#         test="test_all1.csv",
#         fields=[('id', None), ('content', TEXT2), ('tag', LABEL2), ('move_tag', LABEL2)]  # 定义数据对应的表头
#     )
# vectors = torchtext.vocab.Vectors(name="word2vecNocopy.200d.txt", cache="./data/wordVectors")
#
# TEXT2.build_vocab(train_dataset,  test_dataset, vectors=vectors)
# LABEL2.build_vocab(train_dataset, test_dataset)
# print("train", len(TEXT2.vocab))
# print("LABEL.vocab:", len(LABEL2.vocab))




