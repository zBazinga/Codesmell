# -*- coding: utf-8 -*-
# @Time    : 2020/4/29 2:36 下午
# @Author  : Learning


import os
import re
import csv

def text_handle(text):
    mid = ""
    result = []

    # 先把所有的数字以及非'_'去除掉
    for i in range(len(text)):
        if not (text[i].isdigit()):
            if text[i].isalpha():
                mid = mid + text[i]
            elif text[i] == '_':
                mid = mid + text[i]

    if '_' in mid or mid.isupper():  # 现在就是字母+'_'(大小写+_,大小写，大写)，先把全是大写的处理一下
        mid = mid.lower()
        result_mid = mid.split('_')
        for i in result_mid:
            if i != '':
                result.append(i)
        # print(test)
    else:
        #  现在处理不是全部大写的，即 大小写字母混合
        mid_str = ""
        mid_handle = re.split('([A-Z])', mid)  # 用正则表达式按照大写字母分割
        for i in mid_handle:
            if i != "":  # 因为正则分后会把那个大写字母从单词中分开，所以拼接处理一下
                if i.isupper():
                    if mid_str != '':
                        result.append(mid_str)
                        mid_str = ""
                    mid_str = mid_str + i
                else:
                    if mid_str == '':
                        result.append(i)
                    else:
                        mid_str = mid_str + i
        if mid_str != '':
            result.append(mid_str)

    return result


def text_handle_final(text):
    result = []
    for i in text:
        result.append(text_handle(i))

    return result




def handle_list(item):   # 把一个列表变成一个字符串形式，为了表格易读
    st = ""
    for i in range(0, len(item)):
        if i == 0:
            st = st + item[i]
        else:
            st = st + "  " + item[i]
    return st


def file_handle(file_path2, dataset_path2):


    final_result = []
    headers = ['id', 'method-name', 'parametes-method', 'return-method', 'field-access', 'methods-method',
               'contain-class-name', 'attributes-class', 'methods-class', 'contain-class-context',
               'target-class-name', 'attributes-class', 'methods-class', 'target-class-context', 'tag', 'move-tag']
    with open(file_path2, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            final_result_pre = []
            if row[0] == 'id':
                continue
            else:
                for i in range(len(row)):
                    if i == 0 or i == len(row)-1 or i == len(row)-2:
                        final_result_pre.append(row[i])
                    else:
                        text_mid = []
                        text = row[i].split("  ")
                        text2 = text_handle_final(text)
                        for i in text2:
                            text_mid.append(handle_list(i))
                            # print(text_mid)
                        final_result_pre.append(handle_list(text_mid))
            final_result.append(final_result_pre)
        # print(final_result[0])

    with open(dataset_path2, "w") as f:  # newline参数控制行之间是否空行
        f_csv = csv.writer(f)
        f_csv.writerow(headers)  # 表头
        f_csv.writerows(final_result)  # 每一行的数据

project_name = 'traccar-master'
dataset_path = '/Users/dashabi/Desktop/MoveMethodGenerator-master/data/' + project_name + '/dataset.csv'  # 具体存储dataset.csv的文件夹
dataset_path2 = '/Users/dashabi/Desktop/MoveMethodGenerator-master/data/' + project_name+ '/dataset2.csv'   # 存储包含类上下文的文件
final_data_path = '/Users/dashabi/Desktop/final_data/' + project_name + '.csv' # 具体存储最终可输入神经网络的数据的文件夹
final_data_path2 = '/Users/dashabi/Desktop/final_data_context/' + project_name + '.csv'  # 存储包含上下文的最终文件的文件
file_handle(dataset_path2, final_data_path2)