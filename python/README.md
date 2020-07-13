# Codesmell-Extraction
A tool to extract some information from java  

最终版本为 java +python

1.依托论文中的代码生成csv文件以及挪动项目

2.java代码采用AST技术生成一个项目中所需类的信息txt文件（包含了方法信息）

3.python代码(弃用extract.py 只使用 handleAST.py以及text_handle.py)

>1.依托csv文件生成data-pre.csv
>
>2.处理所有txt文件，读取需要的信息
>
>3.data-pre + 信息 = 最后的dataset.csv 文件
>
>4.text_handle处理dataset.csv文件生成可以放进神经网络的文件

