# -*- coding: utf-8 -*-
# @Time    : 2020/5/12 9:33 上午
# @Author  : Learning

import csv
import os

def createdata2():  # 生成10-fold 方法+目标类+包含类为一句话的数据表
    path = "/Users/dashabi/Desktop/实验网络/"  # 读取数据文件
    data_names = os.listdir(path)
    len = 0
    count = 0
    for item in data_names:  # 读取所有项目对应的数据文件
        if item.split(".")[-1] == 'csv':
            file_name = path + '/' + item
            data = open(file_name)
            data = csv.reader(data)
            len+=1
            num_file = 0
            for item2 in data:
                num_file = num_file +1
                count = count + 1
            # print("item",item,"----",num_file)
            # num_file = num_file + len(data)
    print("len:",len,"count",count-len)

createdata2()