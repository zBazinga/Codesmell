# Codesmell-Extraction
A tool to extract some information from java  

最终版本为 java +python

1.依托论文中的代码生成csv文件以及挪动项目

2.java代码采用AST技术生成一个项目中所需类的信息txt文件（包含了方法信息）

3.python代码

>1.handleAST.py 文件依托csv文件生成data-pre.csv
>
>2.handleAST.py 处理所有txt文件，读取需要的信息
>
>3.handleAST.py文件 data-pre + 信息 = 最后的dataset.csv 文件
>
>4.text_handle处理dataset.csv文件生成可以放进神经网络的文件(分词)
>
>5.dataset_split.py 用于划分10-fold以及对信息组合的调整

