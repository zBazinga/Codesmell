# -*- coding: utf-8 -*-
# @Time    : 2020/5/10 10:18 上午
# @Author  : Learning

import csv
import os


# 依据csv文件，生成data-pre.csv文件

def creatcsv(filepath):  # 生成的dataset-pre会比原来的方法少，因为去掉了重复名字的方法（名字重复但是实体不重复，为了简便、精确，去除了重复）
    path1 = filepath
    path2 = filepath + '/classes.csv'
    path3 = filepath + '/methods.csv'
    path4 = filepath + '/moved-methods.csv'
    path5 = filepath + '/dataset-pre.csv'
    # 在读取表格前预先处理表格数据，生成一个满足读取要求的新表格
    with open(path2, 'r') as f:
        reader = csv.reader(f)
        store_class = []
        for row in reader:
            store_class.append(row)
        del store_class[0]
        # print store_class[0]

    with open(path3, 'r') as f:
        reader = csv.reader(f)
        store_methods = []
        for row in reader:
            store_methods.append(row)
        del store_methods[0]
        # print store_methods[0]

    with open(path4, 'r') as f:
        reader = csv.reader(f)
        store_moved_methods = []
        for row in reader:
            store_moved_methods.append(row)
        del store_moved_methods[0]
        # print store_moved_methods[0]
    # print len(store_methods)
    # print store_methods[77]
    store_methods_true = []  # 存储方法名
    store_class_contain = []  # 存储包含次方法名的类
    store_class_target = []  # 存储方法目标类
    store_contain_path = []  # 存储包含方法类的路径
    store_target_path = []  # 存储目标类的路径
    store_tag = []  # 存储是不是坏味
    move_tag = []  # 存储是不是真的移动了
    for i in range(0, len(store_methods)):
        mid_store_pre = store_methods[i][1]
        mid_store = mid_store_pre.split('.')
        # 存储方法名字
        store_methods_true.append(mid_store[len(mid_store) - 1])  # 存储这个方法名字
        # print store_methods_true
        # 存储包含这个方法的类及路径
        locate_class = store_class[int(store_methods[i][4])]  # 按照方法存储的目标、包含类转到class.csv
        contain_class_pre = locate_class[1]
        contain_class = contain_class_pre.split('.')  # 把class存储方法名的一列按照 . 分割开
        contain_class2 = contain_class[len(contain_class) - 1]  # 定位到包含的类
        store_class_contain.append(contain_class2)
        contain_class_path = locate_class[2]
        store_contain_path.append(contain_class_path)
        # print store_contain_path
        # print store_class_contain
        # 存储这个方法的目标类,要处理有多个目标类的情况
        if len(store_methods[i][5]) > 2:  # 处理多个目标类的情况
            mid_handle = store_methods[i][5].split()
            for i2 in range(0, len(mid_handle)):
                locate_class2 = store_class[int(mid_handle[i2])]
                # print mid_handle[i2]
                target_class_pre = locate_class2[1]
                target_class = target_class_pre.split('.')  # 把class存储方法名的一列按照 . 分割开
                target_class2 = target_class[len(target_class) - 1]  # 定位到目标的类
                # store_class_target.append(target_class2)
                target_class_path = locate_class2[2]
                # store_target_path.append(target_class_path)

                # 如果有多个目标类，就加一行
                if i2 == 0:  # (如果这个是目标类的第一个，就存进前面存的一行，这行已经把方法名字、包含类信息存进去了，并且立即生成一个相反的)
                    store_class_target.append(target_class2)
                    store_target_path.append(target_class_path)
                    store_tag.append('0')
                    move_tag.append('0')
                    store_methods_true.append(mid_store[len(mid_store) - 1])  # 存储这个方法名字
                    store_class_contain.append(target_class2)
                    store_contain_path.append(target_class_path)
                    store_class_target.append(contain_class2)
                    store_target_path.append(contain_class_path)
                    store_tag.append('1')
                    move_tag.append('0')
                else:  # （如果这个不是目标类的第一个，就新创建一行，并且立即生成一个相反的）
                    store_methods_true.append(mid_store[len(mid_store) - 1])  # 存储这个方法名字
                    store_class_contain.append(contain_class2)
                    store_contain_path.append(contain_class_path)
                    store_class_target.append(target_class2)
                    store_target_path.append(target_class_path)
                    store_tag.append('0')
                    move_tag.append('0')
                    store_methods_true.append(mid_store[len(mid_store) - 1])  # 存储这个方法名字
                    store_class_contain.append(target_class2)
                    store_contain_path.append(target_class_path)
                    store_class_target.append(contain_class2)
                    store_target_path.append(contain_class_path)
                    store_tag.append('1')
                    move_tag.append('0')
        else:
            locate_class2 = store_class[int(store_methods[i][5])]  # 按照方法存储的目标、包含类转到class.csv
            target_class_pre = locate_class2[1]
            target_class = target_class_pre.split('.')  # 把class存储方法名的一列按照 . 分割开
            target_class2 = target_class[len(target_class) - 1]  # 定位到目标的类
            store_class_target.append(target_class2)
            target_class_path = locate_class2[2]
            store_target_path.append(target_class_path)
            store_tag.append('0')
            move_tag.append('0')
            store_methods_true.append(mid_store[len(mid_store) - 1])  # 存储这个方法名字
            store_class_contain.append(target_class2)
            store_contain_path.append(target_class_path)
            store_class_target.append(contain_class2)
            store_target_path.append(contain_class_path)
            store_tag.append('1')
            move_tag.append('0')

    # 开始读取moved-method数据，进行坏味标注
    for i in range(0, len(store_moved_methods)):
        method_name_pre = store_moved_methods[i][1]
        method_name = method_name_pre.split('.')
        method_name2 = method_name[len(method_name) - 1]
        locate_class = store_class[int(store_moved_methods[i][4])]  # 按照方法存储的目标、包含类转到class.csv
        contain_class_pre = locate_class[1]
        contain_class = contain_class_pre.split('.')  # 把class存储方法名的一列按照 . 分割开
        contain_class2 = contain_class[len(contain_class) - 1]  # 定位到包含的类
        # print("contain:", contain_class2)
        locate_class_2 = store_class[int(store_moved_methods[i][5])]  # 按照方法存储的目标、包含类转到class.csv
        # print("id",store_moved_methods[i][5])
        target_class_pre = locate_class_2[1]
        # print(target_class_pre)
        target_class = target_class_pre.split('.')  # 把class存储方法名的一列按照 . 分割开
        target_class2 = target_class[len(target_class) - 1]  # 定位到包含的类
        # print("target:", target_class2)
        store_index = []
        for index, nums in enumerate(store_methods_true):
            if nums == method_name2:
                store_index.append(index)
        for locate_number in store_index:
            if store_class_contain[locate_number] == target_class2 and store_class_target[
                locate_number] == contain_class2:
                move_tag[locate_number] = '1'

    # 开始创建需要的csv表格
    headers = ['id', 'method-name', 'contain-class-name', 'contain-class-path', 'target-class-name',
               'target-class-path', 'tag', 'move-tag']
    result = []
    str_result = []
    # mid_method = ""  # 解决一张表中出现多个同名方法，那么我只取一个
    i = 0
    # print(store_methods_true[15],store_class_contain[15],store_class_target[15])

    for count in range(0, len(store_methods_true)):
        str_result = []
        if store_methods_true[count]:  # != mid_method:
            str_result.append(str(i))
            i = i + 1
            str_result.append(store_methods_true[count])
            mid_method = store_methods_true[count]
            str_result.append(store_class_contain[count])
            str_result.append(store_contain_path[count])
            str_result.append(store_class_target[count])
            str_result.append(store_target_path[count])
            str_result.append(store_tag[count])
            str_result.append(move_tag[count])
            result.append(str_result)
        else:
            continue
    with open(path5, "w") as f:  # newline参数控制行之间是否空行
        f_csv = csv.writer(f)
        f_csv.writerow(headers)  # 表头
        f_csv.writerows(result)  # 每一行的数据


# 读取txt下所有文件，完成一个项目中类以及内部元素的存储,以及一个项目中所有方法以及相关属性
def read_txt(file_txt):
    fileList = os.listdir(file_txt)  # 用于遍历文件夹,这里是进入到project的存储txt内部
    class_store = []  # 存储一个项目下所有类以及类中元素 【【【类名字】【类属性】【类方法】】【【类名字】【类属性】【类方法】【】】
    method_store = []  # 存储一个项目下所有方法以及方法内部的方法调用、参数类型、返回值类型、属性调用，用字典，因为不同类中方法名字可能一样
    # [[[方法名][所属类名字][返回值类型][参数类型][属性调用][方法调用]] [[方法名][所属类名字][返回值类型][参数类型][属性调用][方法调用]]]
    # print(fileList）
    empty_file = []
    for name in fileList:  # 这里的name是一个txt名字
        if 'txt' not in name:
            continue
        else:
            path = file_txt + '/' + name  # 读取文件夹下的某个project下的某个txt文件
            # print path

            size = os.path.getsize(path)  # 判断一种 enum 的非类声明
            if size == 0:
                name = name.split(".")
                name = name[0]
                empty_file.append(name)
                print("Error--txt--null", path, "------")
            else:  # 如果不是空，就打开这个txt
                with open(path, 'r') as f:
                    reader = csv.reader(f)
                    store_class = []  # 把每行都存储在这里，并且是处理好的，一个行是一个list，一个完整体是list中一个元素
                    store_class_mid = []  # 存储一个类及元素，【【类名】，【属性名字】，【方法名字】,【上下文】】
                    store_class_mid_method = []  # 存储一个类中的方法名，一会放到store_class_mid
                    store_class_mid_field = []  # 存储一个类中的属性名，一会放到store_class_mid
                    store_class_mid_context = []  # 存储一个类中的上下文，一会放到store_class_mid
                    store_method_mid = []  # 存储一个方法以及元素 [[方法名][所属类名字][返回值类型][参数类型][属性调用][方法调用]]
                    store_method_mid_return = []  # 存储方法返回值类型
                    store_method_mid_field = []  # 存储方法形参
                    store_method_mid_field_access = []  # 存储方法里的属性调用
                    store_method_mid_method_invocation = []  # 存储方法里的方法调用
                    for row in reader:  # 下面是对每行的处理
                        store_mid = []
                        mid = str(row)
                        mid = mid.strip("[,]")
                        mid = mid.split(":")
                        for name in mid:
                            name = name.strip("[,],'")
                            name = name.split(",")
                            for name2 in name:
                                name2 = name2.strip("' '")
                                store_mid.append(name2)
                        # mid = mid.split(":")
                        # for name in mid:
                        #     name.strip("[ ]")
                        #     store_mid.append(name)
                        store_class.append(store_mid)
                    # print(store_class[10])

                    # 下面是对已经存好的每一行进行读取分类
                    store_class_mid.append(store_class[0][1])  # 这里只存储第一行的class-name，因为class里面还会声明class，当作属性处理
                    for item in store_class:
                        if item[0] == "Field":
                            store_class_mid_field.append(item[1])  # 把变量存储进去
                        if item[0] == "Class" and item[1] != store_class[0][1]:  # 把类里面声明的类也作为属性存储
                            store_class_mid_field.append(item[1])
                        if item[0] == "Method-name":
                            store_class_mid_method.append(item[1])
                        if item[0] == "Method-returnType" or item[0] == "Method-parameters":
                            # store_class_mid_context.append(item[1])
                            str_mid = ""  # 为了处理ImmutableMap<RepositoryName,RepositoryName> repositoryMapping被分开的情况
                            if item[1] != "":  # 有可能没有参数，即为空
                                for i in range(1, len(item)):  # 存储形参
                                    handle_mid = item[i].split(" ")
                                    if str_mid == "" and len(handle_mid) != 1:
                                        store_class_mid_context.append(handle_mid[-2])
                                        # store_method_mid_field.append(handle_mid[-2])
                                        # final_method_field.append(handle_mid[-2])
                                    if str_mid != "" and len(handle_mid) == 1:
                                        str_mid = str_mid + ',' + str(item[i])

                                    if str_mid == "" and item[i].count("<") != item[i].count(">"):
                                        str_mid = item[i]

                                    if str_mid != "" and len(handle_mid) != 1:
                                        str_mid = str_mid + ',' + handle_mid[-2]
                                        # store_method_mid_field.append(str_mid)
                                        # final_method_field.append(str_mid)
                                        store_class_mid_context.append(handle_mid[-2])
                                        str_mid = ""
                    store_class_mid.append(store_class_mid_field)  # 把这个类中的属性放进类中
                    store_class_mid.append(store_class_mid_method)  # 把这个类中的方法放进类中
                    store_class_mid.append(store_class_mid_context)  # 把这个类的上下文放进类中
                    class_store.append(store_class_mid)

                    # 下面是按照存储好的每一行进行方法的存储
                    tag_method_name = ""  # 虽然是存储的方法名字，但是作用是为了作为标志位，判断是不是进入下一个方法
                    class_name = store_class[0][1]
                    tag = 0  # 有一种情况是 类下面直接出现methodInvocation，就是还没method name呢，做这个标志位是为了处理这个
                    final_method = []  # 是为了处理最后一个method-name根据下面的逻辑不会被存储的办法
                    final_method_name = ""
                    final_method_class = ""
                    final_method_return = []
                    final_method_field = []
                    final_method_field_access = []
                    final_method_method_invocation = []
                    for item in store_class:
                        if item[0] == "Method-name":  # 方法名
                            if item[1] != tag_method_name:
                                if tag_method_name == "":  # 如果读取到方法名并且原来为空，则赋值,且把方法名字和所属类名字存进去
                                    tag_method_name = item[1]
                                    tag = 1
                                    store_method_mid.append(tag_method_name)
                                    store_method_mid.append(class_name)

                                else:
                                    store_method_mid.append(store_method_mid_return)
                                    store_method_mid.append(store_method_mid_field)
                                    store_method_mid.append(store_method_mid_field_access)
                                    store_method_mid.append(store_method_mid_method_invocation)
                                    final_method_return = []
                                    final_method_field = []
                                    final_method_field_access = []
                                    final_method_method_invocation = []

                                    method_store.append(
                                        store_method_mid)  # 读取到方法名字且原来不为空，则把元素放入，重新赋值方法名字，且把该置空的置空,该赋值的赋值
                                    tag_method_name = item[1]
                                    store_method_mid = []  # 存储一个方法以及元素 [[方法名][所属类名字][返回值类型][参数类型][属性调用][方法调用]]
                                    store_method_mid_return = []  # 存储方法返回值类型
                                    store_method_mid_field = []  # 存储方法形参
                                    store_method_mid_field_access = []  # 存储方法里的属性调用
                                    store_method_mid_method_invocation = []  # 存储方法里的方法调用
                                    store_method_mid.append(tag_method_name)
                                    store_method_mid.append(class_name)
                                    final_method_name = ""
                                    final_method_class = ""
                                    final_method_name = tag_method_name
                                    final_method_class = class_name
                            else:
                                store_method_mid.append(store_method_mid_return)
                                store_method_mid.append(store_method_mid_field)
                                store_method_mid.append(store_method_mid_field_access)
                                store_method_mid.append(store_method_mid_method_invocation)
                                final_method_return = []
                                final_method_field = []
                                final_method_field_access = []
                                final_method_method_invocation = []

                                method_store.append(store_method_mid)  # 读取到方法名字且原来不为空，则把元素放入，重新赋值方法名字，且把该置空的置空,该赋值的赋值
                                tag_method_name = item[1]
                                store_method_mid = []  # 存储一个方法以及元素 [[方法名][所属类名字][返回值类型][参数类型][属性调用][方法调用]]
                                store_method_mid_return = []  # 存储方法返回值类型
                                store_method_mid_field = []  # 存储方法形参
                                store_method_mid_field_access = []  # 存储方法里的属性调用
                                store_method_mid_method_invocation = []  # 存储方法里的方法调用
                                store_method_mid.append(tag_method_name)
                                store_method_mid.append(class_name)
                                final_method_name = ""
                                final_method_class = ""
                                final_method_name = tag_method_name
                                final_method_class = class_name

                        if item[0] == "Method-returnType" and tag == 1:  # 存储方法返回值
                            store_method_mid_return.append(item[1])
                            final_method_return.append(item[1])

                        if item[0] == "Method-parameters" and tag == 1:
                            str_mid = ""  # 为了处理ImmutableMap<RepositoryName,RepositoryName> repositoryMapping被分开的情况
                            if item[1] != "":  # 有可能没有参数，即为空
                                for i in range(1, len(item)):  # 存储形参
                                    handle_mid = item[i].split(" ")
                                    # print handle_mid
                                    # if item[i].count("<") != item[i].count(">"):
                                    #     # 比如Method-parameters:[String absName, boolean defaultToMain, ImmutableMap<RepositoryName,RepositoryName> repositoryMapping]
                                    #     # 前面按照,分割，那么ImmutableMap<RepositoryName,RepositoryName> repositoryMapping 变成了
                                    #     # ImmutableMap<RepositoryName和RepositoryName> repositoryMapping
                                    #     # 所以如果是长度为1,那么得加上下面那个
                                    #     str_mid = item[i]
                                    #     #continue
                                    if str_mid == "" and len(handle_mid) != 1:
                                        store_method_mid_field.append(handle_mid[-2])
                                        final_method_field.append(handle_mid[-2])
                                    if str_mid != "" and len(handle_mid) == 1:
                                        str_mid = str_mid + ',' + str(item[i])

                                    if str_mid == "" and item[i].count("<") != item[i].count(">"):
                                        str_mid = item[i]

                                    if str_mid != "" and len(handle_mid) != 1:
                                        str_mid = str_mid + ',' + handle_mid[-2]
                                        store_method_mid_field.append(str_mid)
                                        final_method_field.append(str_mid)
                                        str_mid = ""

                        if item[0] == "MethodInvocation" and tag == 1:  # 存储方法调用
                            store_method_mid_method_invocation.append(item[1])
                            final_method_method_invocation.append(item[1])
                        if item[0] == "FieldAccess" and tag == 1:  # 存储变量调用
                            store_method_mid_field_access.append(item[1])
                            final_method_field_access.append(item[1])
                    final_method.append(final_method_name)
                    final_method.append(final_method_class)
                    final_method.append(final_method_return)
                    final_method.append(final_method_field)
                    final_method.append(final_method_field_access)
                    final_method.append(final_method_method_invocation)
                    method_store.append(final_method)
                    # print ("finale_method",final_method)
    # for i in method_store:
    #     if i[0] == "save":
    #         print(i[0],i[1],i[2],i[3],i[4],i[5])

    return class_store, method_store, empty_file
    # print (len(class_store))
    # print (class_store[0])
    # print (len(method_store))
    # #print (method_store[1200])

    # print(method_store[index])


def handle(item):  # 一个可以把列表处理一下，变成元素形式的函数，用于处理表格
    st = ""
    for i in range(0, len(item)):
        # print item
        # print len(item)
        # print i
        if i == 0:
            st = st + item[i]
        else:
            st = st + "  " + item[i]
    return st


# 依据data-pre.csv和已经有的一个项目中所有类、方法生成最终数据集：
def dataset(filepath_csv, class_store, method_store,
            empty_file):  # 生成的数据集文件会比dataset-pre少，因为有一些文件的类是enum声明，我们ast识别会没有内容，所以目标、包含类为这些类的方法直接过滤
    path_csv = filepath_csv + "/dataset-pre.csv"
    path_dataset2 = filepath_csv + "/dataset2.csv"    #这是生成类的上下文的新路径
    path_dataset = filepath_csv + "/dataset.csv"
    headers = ['id', 'method-name', 'parametes-method', 'return-method', 'field-access', 'methods-method',
               'contain-class-name', 'attributes-class', 'methods-class', 'contain-class-context',
               'target-class-name', 'attributes-class', 'methods-class', 'target-class-context', 'tag', 'move-tag']
    result_final = []  # 【【一行】【一行】】
    handle_dataset_final = []
    handle_methodname = []
    handle_method_empty = []
    # for i in method_store:
    #     if i[0] == "isRootDirectory":
    #         print(i[0],i[1],i[2],i[3],i[4],i[5])
    with open(path_csv, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            handle_dataset = []  # 用于解决读取指定类中指定方法的问题
            if row[0] == "id":  # 去除第一行
                continue
            else:
                target_name = row[4]
                if row[2] in empty_file or target_name in empty_file:
                    handle_method_empty.append(row[1])
                    continue
                else:
                    # print("row6", row[6], "row7", row[7])
                    if row[7] == '1' and row[6] == '1':  # 记录确实已经挪动的方法
                        handle_methodname.append(row[1])
                        handle_dataset.append(row[1])  # 加方法名字
                        handle_dataset.append(row[2])  # 加方法包含类（真正的包含类）
                        handle_dataset.append(row[4])  # 加方法目标类
                        handle_dataset_final.append(handle_dataset)
                        continue
    with open(path_csv, 'r') as f:
        reader = csv.reader(f)
        id = 0
        for row in reader:
            result_final_pre = []  # 把一行的东西存储起来，最后作为一个列表也就是一行放进result_final
            if row[0] == "id":  # 去除第一行
                # print ("suc")
                continue
                # [方法名][所属类名字][返回值类型][参数类型][属性调用][方法调用]
            else:  # [[[方法名][所属类名字][返回值类型][参数类型][属性调用][方法调用]] 【【【类名字】【类属性】【类方法】】【【类名字】【类属性】【类方法】【】】
                # 一开始先判断目标类、包含类属于空文件的，直接舍弃
                # target_class = row[4].split(",")  # 为了处理多个目标类的状况
                target_name = row[4]
                contain_name = row[2]
                method_name = row[1]
                tag = row[6]
                move_tag = row[7]
                if row[1] in handle_method_empty:
                    continue
                else:
                    result_final_pre.append(id)  # 加id
                    id = id + 1
                    result_final_pre.append(row[1])  # 加方法名字
                    # print("method-name:",row[1])
                    # print("row6", row[6], "row7", row[7])
                    if method_name in handle_methodname:
                        for item in handle_dataset_final:
                            if method_name in item:
                                if tag == '0' and contain_name == item[2] and target_name == item[1] and len(
                                        result_final_pre) == 2:  # 确保是同一个方法并且是移动前的
                                    # print("进入判断1")
                                    for i in method_store:
                                        if i[0] == row[1] and i[1] == target_name:
                                            # print("in 00-11")
                                            st3 = handle(i[3])
                                            st2 = handle(i[2])
                                            st4 = handle(i[4])
                                            st5 = handle(i[5])
                                            result_final_pre.append(st3)  # 加方法中参数
                                            result_final_pre.append(st2)  # 加方法中返回值类型
                                            # if i[0] == "save":
                                            #     print st2
                                            #     print i[2]
                                            # print("return-type:",i[2])
                                            result_final_pre.append(st4)  # 加方法中属性调用
                                            result_final_pre.append(st5)  # 加方法中方法调用
                                            break
                                if tag == '1' and contain_name == item[1] and target_name == item[2] and len(
                                        result_final_pre) == 2:  # 确保是已经被移动的
                                    # print("进入判断2")
                                    for i in method_store:
                                        if i[0] == row[1] and i[1] == contain_name:
                                            # print("in 11")
                                            st3 = handle(i[3])
                                            st2 = handle(i[2])
                                            st4 = handle(i[4])
                                            st5 = handle(i[5])
                                            result_final_pre.append(st3)  # 加方法中参数
                                            result_final_pre.append(st2)  # 加方法中返回值类型
                                            # if i[0] == "save":
                                            #     print st2
                                            #     print i[2]
                                            # print("return-type:",i[2])
                                            result_final_pre.append(st4)  # 加方法中属性调用
                                            result_final_pre.append(st5)  # 加方法中方法调用
                                            break
                                if len(result_final_pre) == 2 and tag == '0' and contain_name == item[2]:
                                    #  print("进入判断5")
                                    for i in method_store:
                                        if i[0] == row[1] and i[1] == item[1]:
                                            # print("in 11")
                                            st3 = handle(i[3])
                                            st2 = handle(i[2])
                                            st4 = handle(i[4])
                                            st5 = handle(i[5])
                                            result_final_pre.append(st3)  # 加方法中参数
                                            result_final_pre.append(st2)  # 加方法中返回值类型
                                            # if i[0] == "save":
                                            #     print st2
                                            #     print i[2]
                                            # print("return-type:",i[2])
                                            result_final_pre.append(st4)  # 加方法中属性调用
                                            result_final_pre.append(st5)  # 加方法中方法调用
                                            break
                                if len(result_final_pre) == 2 and tag == '1' and target_name == item[2]:
                                    # print("进入判断5-2")
                                    for i in method_store:
                                        if i[0] == row[1] and i[1] == item[1]:
                                            # print("in 11")
                                            st3 = handle(i[3])
                                            st2 = handle(i[2])
                                            st4 = handle(i[4])
                                            st5 = handle(i[5])
                                            result_final_pre.append(st3)  # 加方法中参数
                                            result_final_pre.append(st2)  # 加方法中返回值类型
                                            # if i[0] == "save":
                                            #     print st2
                                            #     print i[2]
                                            # print("return-type:",i[2])
                                            result_final_pre.append(st4)  # 加方法中属性调用
                                            result_final_pre.append(st5)  # 加方法中方法调用
                                            break
                            # break
                    if len(result_final_pre) == 2:
                        if tag == '0':
                            # print("进入判断3")
                            for i in method_store:
                                # if i[0] == 'initHeaders':
                                #     print(i[1],i[2])
                                if i[0] == row[1] and i[1] == contain_name:
                                    # print("in 00-10")
                                    st3 = handle(i[3])
                                    st2 = handle(i[2])
                                    st4 = handle(i[4])
                                    st5 = handle(i[5])
                                    result_final_pre.append(st3)  # 加方法中参数
                                    result_final_pre.append(st2)  # 加方法中返回值类型
                                    # if i[0] == "save":
                                    #     print st2
                                    #     print i[2]
                                    # print("return-type:",i[2])
                                    result_final_pre.append(st4)  # 加方法中属性调用
                                    result_final_pre.append(st5)  # 加方法中方法调用
                                    break
                        if tag == '1':
                            # print("进入判断4")
                            for i in method_store:
                                if i[0] == row[1] and i[1] == target_name:
                                    # print("in 10")
                                    st3 = handle(i[3])
                                    st2 = handle(i[2])
                                    st4 = handle(i[4])
                                    st5 = handle(i[5])
                                    result_final_pre.append(st3)  # 加方法中参数
                                    result_final_pre.append(st2)  # 加方法中返回值类型
                                    # if i[0] == "save":
                                    #     print st2
                                    #     print i[2]
                                    # print("return-type:",i[2])
                                    result_final_pre.append(st4)  # 加方法中属性调用
                                    result_final_pre.append(st5)  # 加方法中方法调用
                                    break
                    result_final_pre.append(row[2])  # 加包含类的名字
                    for i2 in class_store:
                        if i2[0] == row[2]:
                            c1 = handle(i2[1])
                            c3 = handle(i2[3])
                            c2_pre = []
                            tag_pre = 0
                            for item in i2[2]:  # 为了消除方法名字自己
                                if item == result_final_pre[1] and tag_pre == 0:
                                    # c2_pre.append(item)
                                    tag_pre = 1
                                    continue
                                else:
                                    c2_pre.append(item)

                            c2 = handle(c2_pre)
                            result_final_pre.append(c1)  # 加类的属性
                            result_final_pre.append(c2)  # 加类的方法
                            result_final_pre.append(c3)  # 加类的上下文
                    result_final_pre.append(target_name)  # 加目标类的名字
                    for i3 in class_store:
                        if i3[0] == target_name:
                            t1 = handle(i3[1])
                            t3 = handle(i3[3])
                            # t2 = handle(i3[2])
                            t2_pre = []
                            tag_pre2 = 0
                            for item in i3[2]:  # 为了消除方法名字自己
                                if item == result_final_pre[1] and tag_pre2 == 0:
                                    tag_pre2 = 1
                                    continue
                                else:
                                    t2_pre.append(item)

                            t2 = handle(t2_pre)
                            result_final_pre.append(t1)  # 加目标类的属性
                            result_final_pre.append(t2)  # 加目标类的方法
                            result_final_pre.append(t3) # 加目标类的上下文
                    result_final_pre.append(row[6])  # 加tag
                    result_final_pre.append(row[7])
                    # if result_final_pre[1] == "save":
                    #     print result_final_pre
                    if len(result_final_pre) == 16:
                        result_final.append(result_final_pre)  # 在最终结果里面放进一行

    with open(path_dataset2, "w") as f:  # newline参数控制行之间是否空行
        f_csv = csv.writer(f)
        f_csv.writerow(headers)  # 表头
        f_csv.writerows(result_final)  # 每一行的数据


project_name = 'traccar-master'
filepath_csv = '/Users/dashabi/Desktop/MoveMethodGenerator-master/data/' + project_name  # 具体存储csv的文件夹
filepath_txt = '/Users/dashabi/Desktop/data-text/' + project_name  # 具体存储txt的文件夹
creatcsv(filepath_csv)
class_store, method_store, empty_file = read_txt(filepath_txt)
dataset(filepath_csv, class_store, method_store, empty_file)
