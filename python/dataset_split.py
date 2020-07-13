# -*- coding: utf-8 -*-
# @Time    : 2020/6/9 8:45 下午
# @Author  : Learning
# 为了自己划分验证集和测试集
import os
import csv


def createdata1():  # 生成10-fold普通形式数据表
    path = "/Users/dashabi/Desktop/final_data"
    path_dataset = "/Users/dashabi/Desktop/dataset_codesmell"
    headers = ['id', 'method_name', 'parametes_method', 'return_method', 'field_access', 'methods_method',
               'contain_class_name', 'attributes_contain_class', 'methods_contain_class',
               'target_class_name', 'attributes_target_class', 'methods_target_class', 'tag', 'move_tag']
    data_names = os.listdir(path)
    file_content = []
    file_file = []
    count_rows = 0
    count_files = 0
    count_datafile = 0
    tag = 1

    # for i2 in range(3):
    #     test1 = [[1, 2, 3]]
    #     test2 = [[4,5,6]]
    #     test3 = test1 + test2
    #     print(test3)
    #     with open("/Users/dashabi/Desktop/final_data/test_1.csv", "w") as f:  # newline参数控制行之间是否空行
    #         f_csv = csv.writer(f)
    #         f_csv.writerow(headers)  # 表头
    #         f_csv.writerows(test3)  # 每一行的数据

    # # 计算总共多少条数据
    # for item in data_names:
    #     if item.split(".")[-1] == 'csv':
    #         count_files = count_files + 1
    #         file_name = path + '/' + item
    #         data = open(file_name)
    #         data = csv.reader(data)
    #         # print(len(list(data)),item)
    #         count_rows = count_rows + len(list(data))
    # print(count_rows-count_files)

    for item in data_names:
        if item.split(".")[-1] == 'csv':
            file_name = path + '/' + item
            data = open(file_name)
            data = csv.reader(data)
            for row in data:
                if row[0] == 'id':
                    continue
                else:
                    if count_rows < 938:
                        count_rows = count_rows + 1
                        row = row[1:]
                        row.insert(0, count_rows)
                        file_content.append(row)
                    elif count_rows == 938:
                        count_rows = 0
                        file_file.append(file_content)
                        file_content = []
                        count_rows = count_rows + 1
                        row = row[1:]
                        row.insert(0, count_rows)
                        file_content.append(row)
        if len(file_content) == 938:
            file_file.append(file_content)

    for i in range(len(file_file)):
        count = i + 1
        mid_store = []
        test_dataset = path_dataset + '/test_' + str(count) + ".csv"
        train_dataset = path_dataset + '/train_' + str(count) + ".csv"
        with open(test_dataset, "w") as f:  # newline参数控制行之间是否空行
            f_csv = csv.writer(f)
            f_csv.writerow(headers)  # 表头
            f_csv.writerows(file_file[i])  # 每一行的数据
        for i2 in range(len(file_file)):
            if i2 != i:
                if len(mid_store) == 0:
                    mid_store = file_file[i2]
                else:
                    mid_store = mid_store + file_file[i2]
        with open(train_dataset, "w") as f:  # newline参数控制行之间是否空行
            f_csv = csv.writer(f)
            f_csv.writerow(headers)  # 表头
            f_csv.writerows(mid_store)  # 每一行的数据


def createdata2():  # 生成10-fold 方法+目标类+包含类为一句话的数据表
    path = "/Users/dashabi/Desktop/final_data"  # 读取数据文件
    path_dataset = "/Users/dashabi/Desktop/dataset_codesmell/data_all"  # 存储数据文件
    headers = ['id', 'content', 'tag', 'move_tag']  # 定义表头
    data_names = os.listdir(path)
    file_content = []
    file_file = []
    count_rows = 0

    for item in data_names:  # 读取所有项目对应的数据文件
        if item.split(".")[-1] == 'csv':
            file_name = path + '/' + item
            data = open(file_name)
            data = csv.reader(data)
            for row in data:
                if row[0] == 'id':
                    continue
                else:
                    if count_rows < 938:  # 因为是10-fold，计算好的是一个文件寸938个
                        mid = []
                        count_rows = count_rows + 1  # 计数
                        s = " ".join(row[1:-2])  # 把除最后的tag 和 move-tag外的变成一个字符串
                        mid.append(s)
                        mid.append(row[-2])
                        mid.append(row[-1])
                        # row = row[1:]
                        mid.insert(0, count_rows)  # 给前面插入技术行
                        file_content.append(mid)
                    elif count_rows == 938:
                        count_rows = 0
                        file_file.append(file_content)  # 把938个行作为一个List存进最终的list
                        file_content = []
                        count_rows = count_rows + 1
                        mid = []
                        s = " ".join(row[1:-2])
                        mid.append(s)
                        mid.append(row[-2])
                        mid.append(row[-1])
                        mid.insert(0, count_rows)
                        file_content.append(mid)
        if len(file_content) == 938:
            file_file.append(file_content)

    for i in range(len(file_file)):
        count = i + 1
        mid_store = []
        test_dataset = path_dataset + '/test_all' + str(count) + ".csv"
        train_dataset = path_dataset + '/train_all' + str(count) + ".csv"
        with open(test_dataset, "w") as f:  # newline参数控制行之间是否空行
            f_csv = csv.writer(f)
            f_csv.writerow(headers)  # 表头
            f_csv.writerows(file_file[i])  # 每一行的数据
        for i2 in range(len(file_file)):  # 把除已经写入train的其他文件放在一起准备写入test
            if i2 != i:
                if len(mid_store) == 0:
                    mid_store = file_file[i2]
                else:
                    mid_store = mid_store + file_file[i2]
        with open(train_dataset, "w") as f:  # newline参数控制行之间是否空行
            f_csv = csv.writer(f)
            f_csv.writerow(headers)  # 表头
            f_csv.writerows(mid_store)  # 每一行的数据


def createdata3():  # 生成10-fold  方法名字+其他元素+包含类+目标类/返回值形参（context)/两个tag
    path = "/Users/dashabi/Desktop/final_data"  # 读取数据文件
    path_dataset = "/Users/dashabi/Desktop/dataset_codesmell/10-fold-context"  # 存储数据文件
    headers = ['id', 'content', 'context', 'tag', 'move_tag']  # 定义表头
    data_names = os.listdir(path)
    file_content = []
    file_file = []
    count_rows = 0

    for item in data_names:  # 读取所有项目对应的数据文件
        if item.split(".")[-1] == 'csv':
            file_name = path + '/' + item
            data = open(file_name)
            data = csv.reader(data)
            for row in data:
                if row[0] == 'id':
                    continue
                else:
                    if count_rows < 938:  # 因为是10-fold，计算好的是一个文件寸938个
                        mid = []
                        count_rows = count_rows + 1  # 计数
                        handle = row[1:2] + row[4:-2]
                        s1 = " ".join(handle)
                        s2 = " ".join(row[2:4])
                        mid.append(s1)
                        mid.append(s2)
                        mid.append(row[-2])
                        mid.append(row[-1])
                        # row = row[1:]
                        mid.insert(0, count_rows)  # 给前面插入技术行
                        file_content.append(mid)
                    elif count_rows == 938:
                        count_rows = 0
                        file_file.append(file_content)  # 把938个行作为一个List存进最终的list
                        file_content = []
                        count_rows = count_rows + 1
                        mid = []
                        handle = row[1:2] + row[4:-2]
                        s1 = " ".join(handle)
                        s2 = " ".join(row[2:4])
                        mid.append(s1)
                        mid.append(s2)
                        mid.append(row[-2])
                        mid.append(row[-1])
                        mid.insert(0, count_rows)
                        file_content.append(mid)
        if len(file_content) == 938:
            file_file.append(file_content)

    for i in range(len(file_file)):
        count = i + 1
        mid_store = []
        test_dataset = path_dataset + '/test_all' + str(count) + ".csv"
        train_dataset = path_dataset + '/train_all' + str(count) + ".csv"
        with open(test_dataset, "w") as f:  # newline参数控制行之间是否空行
            f_csv = csv.writer(f)
            f_csv.writerow(headers)  # 表头
            f_csv.writerows(file_file[i])  # 每一行的数据
        for i2 in range(len(file_file)):  # 把除已经写入train的其他文件放在一起准备写入test
            if i2 != i:
                if len(mid_store) == 0:
                    mid_store = file_file[i2]
                else:
                    mid_store = mid_store + file_file[i2]
        with open(train_dataset, "w") as f:  # newline参数控制行之间是否空行
            f_csv = csv.writer(f)
            f_csv.writerow(headers)  # 表头
            f_csv.writerows(mid_store)  # 每一行的数据


def createdata4():  # 生成10-fold  方法名字+其他元素+包含类+目标类/返回值形参（context)/两个tag
    path = "/Users/dashabi/Desktop/final_data"  # 读取数据文件
    path_dataset = "/Users/dashabi/Desktop/dataset_codesmell/10-fold-4-context"  # 存储数据文件
    headers = ['id', 'content_method', 'context_method', 'access_method', 'content_class_contain',
               'context_class_contain', 'content_class_target', 'context_class_target', 'tag', 'move_tag']  # 定义表头
    data_names = os.listdir(path)
    file_content = []
    file_file = []
    count_rows = 0

    for item in data_names:  # 读取所有项目对应的数据文件
        if item.split(".")[-1] == 'csv':
            file_name = path + '/' + item
            data = open(file_name)
            data = csv.reader(data)
            for row in data:
                if row[0] == 'id':
                    continue
                else:
                    if count_rows < 938:  # 因为是10-fold，计算好的是一个文件寸938个
                        mid = []
                        count_rows = count_rows + 1  # 计数
                        method_name = " ".join(row[1:2])
                        method_context = " ".join(row[2:4])  # 返回值和形参
                        method_access = " ".join(row[4:6])  # 方法和属性调用
                        class_contain_name = " ".join(row[6:7])
                        class_contain_context = " ".join(row[7:9])
                        class_target_name = " ".join(row[9:10])
                        class_target_context = " ".join(row[10:12])
                        mid.append(method_name)
                        mid.append(method_context)
                        mid.append(method_access)
                        mid.append(class_contain_name)
                        mid.append(class_contain_context)
                        mid.append(class_target_name)
                        mid.append(class_target_context)
                        mid.append(row[-2])
                        mid.append(row[-1])
                        # row = row[1:]
                        mid.insert(0, count_rows)  # 给前面插入计数行
                        file_content.append(mid)
                    elif count_rows == 938:
                        count_rows = 0
                        file_file.append(file_content)  # 把938个行作为一个List存进最终的list
                        file_content = []
                        count_rows = count_rows + 1
                        mid = []
                        # handle = row[1:2] + row[4:-2]
                        # s1 = " ".join(handle)
                        # s2 = " ".join(row[2:4])
                        # mid.append(s1)
                        # mid.append(s2)
                        method_name = " ".join(row[1:2])
                        method_context = " ".join(row[2:4])  # 返回值和形参
                        method_access = " ".join(row[4:6])  # 方法和属性调用
                        class_contain_name = " ".join(row[6:7])
                        class_contain_context = " ".join(row[7:9])
                        class_target_name = " ".join(row[9:10])
                        class_target_context = " ".join(row[10:12])
                        mid.append(method_name)
                        mid.append(method_context)
                        mid.append(method_access)
                        mid.append(class_contain_name)
                        mid.append(class_contain_context)
                        mid.append(class_target_name)
                        mid.append(class_target_context)
                        mid.append(row[-2])
                        mid.append(row[-1])
                        mid.insert(0, count_rows)
                        file_content.append(mid)
        if len(file_content) == 938:
            file_file.append(file_content)

    for i in range(len(file_file)):
        count = i + 1
        mid_store = []
        test_dataset = path_dataset + '/test_all' + str(count) + ".csv"
        train_dataset = path_dataset + '/train_all' + str(count) + ".csv"
        with open(test_dataset, "w") as f:  # newline参数控制行之间是否空行
            f_csv = csv.writer(f)
            f_csv.writerow(headers)  # 表头
            f_csv.writerows(file_file[i])  # 每一行的数据
        for i2 in range(len(file_file)):  # 把除已经写入train的其他文件放在一起准备写入test
            if i2 != i:
                if len(mid_store) == 0:
                    mid_store = file_file[i2]
                else:
                    mid_store = mid_store + file_file[i2]
        with open(train_dataset, "w") as f:  # newline参数控制行之间是否空行
            f_csv = csv.writer(f)
            f_csv.writerow(headers)  # 表头
            f_csv.writerows(mid_store)  # 每一行的数据


createdata4()
