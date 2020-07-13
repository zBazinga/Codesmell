import torch
import torch.nn as nn
import torch.nn.functional as F


class TextCNN(nn.Module):
    def __init__(self,
                 class_num,  # 最后输出的种类数
                 filter_sizes,  # 卷积核的长也就是滑动窗口的长
                 filter_num,  # 卷积核的数量
                 vocabulary_size,  # 词表的大小
                 embedding_dimension,  # 词向量的维度
                 vectors,  # 词向量
                 dropout):  # dropout率
        super(TextCNN, self).__init__()  # 继承nn.Module

        chanel_num = 1  # 通道数，也就是一篇文章一个样本只相当于一个feature map

        self.embedding = nn.Embedding(vocabulary_size, embedding_dimension)  # 嵌入层
        self.embedding = self.embedding.from_pretrained(vectors)  # 嵌入层加载预训练词向量
        self.convs = nn.ModuleList(
            [nn.Conv2d(chanel_num, filter_num, (fsz, embedding_dimension)) for fsz in [3,4]])  # 卷积层
        self.convs2 = nn.ModuleList(
            [nn.Conv2d(chanel_num, filter_num, (fsz, embedding_dimension)) for fsz in filter_sizes])  # 卷积层
        self.convs3 = nn.ModuleList(
            [nn.Conv2d(chanel_num, filter_num, (fsz, embedding_dimension)) for fsz in filter_sizes])  # 卷积层
        self.convs4 = nn.ModuleList(
            [nn.Conv2d(chanel_num, filter_num, (fsz, embedding_dimension)) for fsz in [3,4]])  # 卷积层
        self.convs5 = nn.ModuleList(
            [nn.Conv2d(chanel_num, filter_num, (fsz, embedding_dimension)) for fsz in filter_sizes])  # 卷积层
        self.convs6 = nn.ModuleList(
            [nn.Conv2d(chanel_num, filter_num, (fsz, embedding_dimension)) for fsz in[3,4]])  # 卷积层
        self.convs7 = nn.ModuleList(
            [nn.Conv2d(chanel_num, filter_num, (fsz, embedding_dimension)) for fsz in filter_sizes])  # 卷积层
        self.dropout = nn.Dropout(dropout)  # dropout
        self.fc = nn.Linear(288, class_num)# nn.Linear(len(filter_sizes) * filter_num*12, class_num)  # 全连接层  比初始的多乘了一个2  后来又改成固定算出来的336

    def forward(self, content_method, context_method,access_method, content_class_contain, context_class_contain, content_class_target, context_class_target):
        # x维度[句子长度,一个batch中所包含的样本数] 例:[3451,128]
        # 7个输入先都经过嵌入层 x2 = self.embedding(x2)
        content_method = self.embedding(content_method)  # 经过嵌入层之后x的维度，[句子长度,一个batch中所包含的样本数,词向量维度] 例：[3451,128,300]
        context_method = self.embedding(context_method)
        access_method = self.embedding(access_method)
        content_class_contain = self.embedding(content_class_contain)
        context_class_contain = self.embedding(context_class_contain)
        content_class_target = self.embedding(content_class_target)
        context_class_target = self.embedding(context_class_target)

        # x = x.permute(1, 0, 2) x2 = x2.permute(1, 0, 2)  # permute函数将样本数和句子长度换一下位置，[一个batch中所包含的样本数,句子长度,词向量维度] 例：[128,3451,300]
        # 交换维度
        content_method = content_method.permute(1, 0, 2)
        context_method = context_method.permute(1, 0, 2)
        access_method = access_method.permute(1, 0, 2)
        content_class_contain = content_class_contain.permute(1, 0, 2)
        context_class_contain = context_class_contain.permute(1, 0, 2)
        content_class_target = content_class_target.permute(1, 0, 2)
        context_class_target = context_class_target.permute(1, 0, 2)

        # x = x.unsqueeze(1)  # conv2d需要输入的是一个四维数据，所以新增一维feature map数 unsqueeze(1)表示在第一维处新增一维，[一个batch中所包含的样本数,一个样本中的feature map数，句子长度,词向量维度] 例：[128,1,3451,300]
        # x2 = x2.unsqueeze(1)
        # 新增维度
        content_method = content_method.unsqueeze(1)
        context_method = context_method.unsqueeze(1)
        access_method = access_method.unsqueeze(1)
        content_class_contain = content_class_contain.unsqueeze(1)
        context_class_contain = context_class_contain.unsqueeze(1)
        content_class_target = content_class_target.unsqueeze(1)
        context_class_target = context_class_target.unsqueeze(1)

        # x = [conv(x) for conv in self.convs]  # 与卷积核进行卷积，输出是[一个batch中所包含的样本数,卷积核数，句子长度-卷积核size+1,1]维数据,因为有[3,4,5]三张size类型的卷积核所以用列表表达式 例：[[128,16,3459,1],[128,16,3458,1],[128,16,3457,1]]
        # x2 =  [conv2(x2) for conv2 in self.convs2]
        content_method = [conv(content_method) for conv in self.convs]
        context_method = [conv2(context_method) for conv2 in self.convs2]
        access_method = [conv3(access_method) for conv3 in self.convs3]
        content_class_contain = [conv4(content_class_contain) for conv4 in self.convs4]
        context_class_contain = [conv5(context_class_contain) for conv5 in self.convs5]
        content_class_target = [conv6(content_class_target) for conv6 in self.convs6]
        context_class_target = [conv7(context_class_target) for conv7 in self.convs7]

        # x = [sub_x.squeeze(3) for sub_x in x]  # squeeze(3)判断第三维是否是1，如果是则压缩，如不是则保持原样 例：[[128,16,3459],[128,16,3458],[128,16,3457]]
        # x2 = [sub_x2.squeeze(3) for sub_x2 in x2]
        # 压缩维度
        content_method =[sub_x.squeeze(3) for sub_x in content_method]
        context_method = [sub_x.squeeze(3) for sub_x in context_method]
        access_method =[sub_x.squeeze(3) for sub_x in access_method]
        content_class_contain = [sub_x.squeeze(3) for sub_x in content_class_contain]
        context_class_contain =[sub_x.squeeze(3) for sub_x in context_class_contain]
        content_class_target = [sub_x.squeeze(3) for sub_x in content_class_target]
        context_class_target = [sub_x.squeeze(3) for sub_x in context_class_target]


        # x = [F.relu(sub_x) for sub_x in x]  # ReLU激活函数激活，不改变x维度
        # x2 = [F.relu(sub_x2) for sub_x2 in x2]
        # ReLU激活
        content_method = [F.relu(sub_x) for sub_x in content_method]
        context_method = [F.relu(sub_x) for sub_x in context_method]
        access_method = [F.relu(sub_x) for sub_x in access_method]
        content_class_contain = [F.relu(sub_x) for sub_x in content_class_contain]
        context_class_contain = [F.relu(sub_x) for sub_x in context_class_contain]
        content_class_target = [F.relu(sub_x) for sub_x in content_class_target]
        context_class_target = [F.relu(sub_x) for sub_x in context_class_target]


        # x = [F.max_pool1d(sub_x, sub_x.size(2)) for sub_x in x]  # 池化层，根据之前说的原理，max_pool1d要取出每一个滑动窗口生成的矩阵的最大值，因此在第二维上取最大值 例：[[128,16,1],[128,16,1],[128,16,1]]
        # x2 = [F.max_pool1d(sub_x2, sub_x2.size(2)) for sub_x2 in x2]
        # 池化层
        content_method = [F.max_pool1d(sub_x, sub_x.size(2)) for sub_x in content_method]
        context_method = [F.max_pool1d(sub_x, sub_x.size(2)) for sub_x in context_method]
        access_method = [F.max_pool1d(sub_x, sub_x.size(2)) for sub_x in access_method]
        content_class_contain = [F.max_pool1d(sub_x, sub_x.size(2)) for sub_x in content_class_contain]
        context_class_contain = [F.max_pool1d(sub_x, sub_x.size(2)) for sub_x in context_class_contain]
        content_class_target = [F.max_pool1d(sub_x, sub_x.size(2)) for sub_x in content_class_target]
        context_class_target = [F.max_pool1d(sub_x, sub_x.size(2)) for sub_x in context_class_target]


        # x = [sub_x.squeeze(2) for sub_x in x]  # 判断第二维是否为1，若是则压缩 例：[[128,16],[128,16],[128,16]]
        # x2 = [sub_x2.squeeze(2) for sub_x2 in x2]
        # 压缩维度
        content_method = [sub_x.squeeze(2) for sub_x in content_method]
        context_method = [sub_x.squeeze(2) for sub_x in context_method]
        access_method = [sub_x.squeeze(2) for sub_x in access_method]
        content_class_contain = [sub_x.squeeze(2) for sub_x in content_class_contain]
        context_class_contain = [sub_x.squeeze(2) for sub_x in context_class_contain]
        content_class_target = [sub_x.squeeze(2) for sub_x in content_class_target]
        context_class_target = [sub_x.squeeze(2) for sub_x in context_class_target]

        # x = torch.cat(x, 1)  # 进行拼接，例：[128,48]
        # x2 = torch.cat(x2, 1)
        # 进行拼接
        content_method = torch.cat(content_method, 1)
        context_method = torch.cat(context_method, 1)
        access_method = torch.cat(access_method, 1)
        content_class_contain = torch.cat(content_class_contain, 1)
        context_class_contain = torch.cat(context_class_contain, 1)
        content_class_target = torch.cat(content_class_target, 1)
        context_class_target = torch.cat(context_class_target, 1)

        # 方法名、上下文、调用拼接成一个向量、类和自己的上下文拼接成一个向量 (加attention应该在此之前）
        method = torch.cat((content_method, context_method, access_method), 1)    # [128, 96]
        class_contain = torch.cat((content_class_contain,context_class_contain), 1)             # [128, 96]
        class_target = torch.cat((content_class_target,context_class_target), 1)       # [128, 96]

        # 三者合成一个向量送入全联接层
        x = torch.cat((method, class_contain, class_target), 1)    # 最终把这个content 和  context 拼接成   改成： [128,96*3]
        x = self.dropout(x)  # 去除掉一些神经元防止过拟合，注意dropout之后x的维度依旧是[128,48]，并不是说我dropout的概率是0.5，去除了一半的神经元维度就变成了[128,
        # 24]，而是把x中的一些神经元的数据根据概率全部变成了0，维度依旧是[128,48]
        logits = self.fc(x)  # 全接连层 例：输入x是[128,48] 输出logits是[128,10]   改成了[128,96] 又改成了[128,96*3]
        return logits
